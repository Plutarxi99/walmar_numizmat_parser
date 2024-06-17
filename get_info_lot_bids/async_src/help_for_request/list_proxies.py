import random



async def get_proxies():
    list_proxies_id_port = ['http://176.126.104.126:8085', 'http://194.70.234.241:8085', 'http://193.163.92.114:8085',
                            'http://193.163.92.108:8085', 'http://193.163.92.124:8085', 'http://185.212.115.158:8085',
                            'http://194.70.234.21:8085', 'http://62.233.39.43:8085', 'http://146.19.78.90:8085',
                            'http://193.163.207.127:8085', 'http://185.68.152.247:8085', 'http://146.19.78.185:8085',
                            'http://185.68.154.187:8085', 'http://185.68.154.236:8085', 'http://91.246.51.65:8085',
                            'http://185.212.115.205:8085', 'http://193.163.92.159:8085', 'http://91.247.163.183:8085',
                            'http://62.233.39.202:8085', 'http://193.163.92.128:8085', 'http://146.19.91.220:8085',
                            'http://94.154.113.60:8085', 'http://185.68.155.169:8085', 'http://185.68.154.125:8085',
                            'http://83.97.119.202:8085', 'http://212.18.113.56:8085', 'http://185.68.152.47:8085',
                            'http://193.163.207.65:8085', 'http://146.19.44.32:8085', 'http://146.19.39.84:8085',
                            'http://185.68.153.253:8085', 'http://176.126.104.169:8085', 'http://185.212.115.128:8085',
                            'http://91.247.163.109:8085', 'http://146.19.78.251:8085', 'http://193.163.207.215:8085',
                            'http://94.154.113.191:8085', 'http://91.247.163.51:8085', 'http://212.18.127.125:8085',
                            'http://193.163.207.101:8085', 'http://185.68.153.215:8085', 'http://185.212.115.105:8085',
                            'http://146.19.78.31:8085', 'http://212.18.113.201:8085', 'http://212.18.127.157:8085',
                            'http://146.19.39.99:8085', 'http://212.18.113.35:8085', 'http://146.19.44.53:8085',
                            'http://62.204.49.59:8085', 'http://185.68.155.105:8085', 'http://91.246.51.62:8085',
                            'http://185.68.155.59:8085', 'http://193.163.92.169:8085', 'http://185.68.153.20:8085',
                            'http://185.212.115.141:8085', 'http://94.154.113.127:8085', 'http://91.246.51.210:8085',
                            'http://62.233.39.85:8085', 'http://185.68.155.51:8085', 'http://146.19.44.74:8085',
                            'http://212.18.127.238:8085', 'http://212.18.113.143:8085', 'http://146.19.44.137:8085',
                            'http://185.68.153.149:8085', 'http://185.68.155.88:8085', 'http://146.19.44.70:8085',
                            'http://193.163.207.187:8085', 'http://91.247.163.37:8085', 'http://146.19.39.54:8085',
                            'http://91.246.51.224:8085', 'http://94.154.113.132:8085', 'http://193.163.207.149:8085',
                            'http://193.233.248.12:8085', 'http://185.212.115.248:8085', 'http://185.68.155.79:8085',
                            'http://185.68.152.208:8085', 'http://185.68.152.182:8085', 'http://146.19.44.244:8085',
                            'http://146.19.78.25:8085', 'http://193.163.207.18:8085', 'http://193.163.207.29:8085',
                            'http://62.204.49.55:8085', 'http://194.70.234.128:8085', 'http://193.233.248.11:8085',
                            'http://94.154.113.121:8085', 'http://62.233.39.106:8085', 'http://146.19.44.248:8085',
                            'http://146.19.91.145:8085', 'http://185.68.154.139:8085', 'http://146.19.91.211:8085',
                            'http://193.233.248.13:8085', 'http://91.247.163.133:8085', 'http://193.163.92.12:8085',
                            'http://212.18.127.184:8085', 'http://83.97.119.233:8085', 'http://91.247.163.204:8085',
                            'http://146.19.39.73:8085', 'http://94.154.113.109:8085', 'http://193.163.92.163:8085',
                            'http://185.68.154.239:8085']

    proxy = random.randint(0, len(list_proxies_id_port) - 1)
    pr = list_proxies_id_port[proxy]
    return pr
