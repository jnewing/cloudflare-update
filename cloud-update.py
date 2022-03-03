#!/usr/bin/env python3
import argparse
import requests


''' AUTH_EMAIL
The email used to login 'https://dash.cloudflare.com'
'''
AUTH_EMAIL="your@email.com"

''' AUTH_KEY
Your Cloudflare API Token
'''
AUTH_KEY="your-api_token"

''' ZONE_IDENTIFIER
Can be found in the "Overview" tab of your domain
'''
ZONE_IDENTIFIER="zone-id"

''' RECORDS
Holds all the host records we want to check for an ip change and update. 

Example Record
    {
        Domain name of the record we are checking. This is the only required entry for a record.
        * Required
        'name': 'your.domain.com',

        IP Address we want this record to reflect.
        If this is not specified it will default to your found external ip. ** See get_external_ip() function
        - Optional (Default: Your External IP)
        'ip': '0.0.0.0',
        
        TTL
        - Optional (Default: Auto)
        'ttl': 3600,

        Enable / Disab;e Proxied Requests
        - Optional (Default: True)
        'proxied': True,
    }
'''
RECORDS = [
    {
        'name': 'my.example.com',
    },
]


''' Attempts to get your current external IP by querying
https://api.ipify.org
'''
def get_external_ip():
    external_ip = requests.get('https://api.ipify.org').text
    
    return external_ip


''' Trys to find an existing record on your Cloudflare account matching
by record_name. 
'''
def get_record(record_name):
    # return resp_data
    r = requests.get(f"https://api.cloudflare.com/client/v4/zones/{ZONE_IDENTIFIER}/dns_records",
        params = {
            'type': 'A',
            'name': record_name
        },

        headers = {
            'X-Auth-Email': AUTH_EMAIL,
            'Authorization': 'Bearer ' + AUTH_KEY,
            'Content-Type': 'application/json'
        })
    
    return r.json() if r.ok else None


''' Attempts to update your Cloudflare DNS entry to the current found external IP if they don't
seem to match up or there is an override 'ip' field specified in the RECORD.
'''
def update_record(local_record, cloudflare_record, ext_ip):
    r = requests.patch(f"https://api.cloudflare.com/client/v4/zones/{ZONE_IDENTIFIER}/dns_records/{cloudflare_record[0].get('id')}",
        headers = {
            'X-Auth-Email': AUTH_EMAIL,
            'Authorization': 'Bearer ' + AUTH_KEY,
            'Content-Type': 'application/json'
        },

        json = {
            'type': 'A',
            'name': local_record.get('name'),
            'content': local_record.get('ip', ext_ip),
            'ttl': local_record.get('ttl', 1),
            'proxied': local_record.get('proxied', True),
        })

    return True if r.ok else False


''' EP
'''
def main(args):
    # get our external ip
    ip = get_external_ip()

    for local_record in RECORDS:
        print('\033[1m[\033[32m+\033[39m]\033[0m' + f" checking for record {local_record.get('name')} ... ", end='')
        record_data = get_record(local_record.get('name')).get('result')
        
        if record_data:
            print(f"found.")
            print('\033[1m[\033[32m+\033[39m]\033[0m' + f" \tchecking current ip: {ip} against record ip: {record_data[0].get('content')} ... ", end='')

            if ip != record_data[0].get('content') or local_record.get('ip'):
                if update_record(local_record, record_data, ip):
                    print("updated.")
                else:
                    print("failed to update?!")
            else:
                print("no update needed.")
        else:
            print(f"missing?!")
            print('\033[1m[\033[31m-\033[39m]\033[0m' + f" \tcheck record {local_record.get('name')} can't find matching entry.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='update', 
        description='Updates Cloudflare DNS records with your external IP.')

    arguments = parser.parse_args()
    main(arguments)