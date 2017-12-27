# Domain Scanner

A simple Python3 script for scanning domain availability.

**NOTE:** The `API_URL` is hidden intentionally in order to protect the domain search website.

This script is only for learning purpose. Do no use it to harass domain search websites.

# How to use

Supported command line parameters:

Name | Meaning | Default Value | Example
---|---|---|---
`--start`, `-s` | From which domain name to search | `a` | `--start=abc` starts the search from `abc.com` (`com` is default ending)
`--endings`, `-e` | A comma-separated list of Top Level Domains (TLD) you are interested in | `com` | `--endings=com,io` searches all domains ending with `.com` and `.io`
`--interval`, `-i` | The interval (in seconds) between each request | `1` | `--interval=2` sends requests every 2 seconds.
`--help`, `-h` | Display help message | | 

Example: `python domain-scanner.py --start=abc --endings=com,io --interval=2`

# License
See the [LICENSE](./LICENSE.md) file for license rights and limitations (MIT).