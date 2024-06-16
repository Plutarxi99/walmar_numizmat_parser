import datetime
import time

import requests

from config import settings

proxy_ip = settings.PROXIES_IP
proxy_port = settings.PROXIES_PORT
proxy_user = settings.PROXIES_EMAIL
proxy_pass = settings.PROXIES_PASS
proxy_ip_def = settings.PROXIES_IP_DEF
proxy_port_def = settings.PROXIES_PORT_DEF

proxies = {
    "http": f"http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}/",
    "https": f"http://{proxy_user}:{proxy_pass}@{proxy_ip}:{proxy_port}/"
}

proxies_def = {
   'http': f'http://{proxy_ip_def}:{proxy_port_def}',
   'https': f'http://{proxy_ip_def}:{proxy_port_def}'
}

url = 'https://api.ipify.org'

try:
    response = requests.get(url, proxies=proxies_def)
    print(response.text)
    assert response.text == proxy_ip
except:
    print("Proxy does not work")

timestamp = int(time.time())
print(timestamp)
