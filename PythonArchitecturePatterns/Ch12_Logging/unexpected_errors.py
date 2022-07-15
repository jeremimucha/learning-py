import logging
from urllib import response
import requests


URL = "https://httpbin.org/status/500"

logging.info(f"GET {URL}")
# deliberate typo, resulting in an exception
# if we don't handle it, we're done.
response = requests.ge(URL)
status_code = response.status_code
if status_code != 200:
    logging.error(f"Error accessing {URL} status code {status_code}")
