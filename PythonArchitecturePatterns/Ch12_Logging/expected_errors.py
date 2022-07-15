import logging
import requests


URL = "https://httpbin.org/status/500"

response = requests.get(URL)
status_code = response.status_code
if status_code != 200:
    logging.error(f"Error accessing {URL} status code {status_code}")
