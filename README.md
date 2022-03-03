# Cloudflare Dynamic DNS Update

Python script that allows users to update their Cloudflare DNS entries when their IPs change.

## Getting started

**1. Clone the Repo**
`git clone `

**2. Install Python Requirements**
`pip install -r requirements.txt`

**3. Edit Script Variables**
Open the script in an editor of your choice and make sure to replace the following variables with the correct data.
```python
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
```
**4. Setup Records**
Add any records you would like to update to the `RECORDS` variable.
```python
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

RECORDS  = [
    {
        'name': 'my.domain.com',
    },
    {
        'name': 'another.example.com',
        'proxied': False,
    },
    {
        'name': 'final.example.com',
        'ip': '10.10.1.1',
        'ttl': 3600,
        'proxied': False
    },
]
```

**5. Add A Cronjob**
Make sure the script is saved and executable. `chmod +x cloud-update.py` and then add it to your crontab with something like the following entry.

Example: `*/2 * * * * /full/path/cloud-update.py >/dev/null 2>&1`

**That's it!**

## License

Copyright 2022 J. Newing

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
