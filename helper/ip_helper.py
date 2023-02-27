import requests

class ip_helper():
    def userIP():
        r = requests.get("https://ipapi.co/json/", 
                 headers={'Accept': 'application/json'})
        ip = r.json()['ip']
        country = r.json()['country_name']
        return ip, country


a = ip_helper.userIP()
print(a)     