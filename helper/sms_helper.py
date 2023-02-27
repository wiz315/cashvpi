import requests

url = "https://bms.syriatel.sy/API/SendSMS.aspx"


def send_msg(job_name,msg,to):
    payload = {
        "job_name": job_name,
        "user_name": "CASH SYRIA1",
        "password": "P@123456",
        "msg": msg,
        "sender": "CASH SYRIA",
        "to": to
    } 
    response = requests.get(url, params=payload, verify=False)
    print(response)

