import requests as r
import datetime
import certifi


last_update = datetime.datetime.now()

jwt = None
jwt_pro = None


def retrieve_jwt():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload='scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': '0ffb1e2b-115c-4dad-b965-f22973a47f78',
        'Authorization': 'Basic MGZmYjFlMmItMTE1Yy00ZGFkLWI5NjUtZjIyOTczYTQ3Zjc4OjA5NDI0MTE0LWRkOTQtNDIyNS05OGFkLWJjMmFlMjQ3NzZlZQ=='
    }

    response = r.request("POST", url, headers=headers, data=payload, verify=False)
    return response.json()

def retrieve_pro_jwt():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload='scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': 'b094cf70-ec2a-416b-967a-3a6fc012fc88',
        'Authorization': 'Basic YjA5NGNmNzAtZWMyYS00MTZiLTk2N2EtM2E2ZmMwMTJmYzg4OmYyNDk1ZmUzLTI4NjctNGJmZS04NWMyLTFjN2YyMzNhNjE2YQ=='
    }

    response = r.request("POST", url, headers=headers, data=payload, verify=False)
    return response.json()


def get_jwt():
    global jwt, last_update

    if jwt == None or datetime.datetime.now() - last_update >= datetime.timedelta(minutes=10):
        jwt = retrieve_jwt()
    return jwt


def get_jwt_pro():
    global jwt_pro, last_update
    if jwt_pro == None or datetime.datetime.now() - last_update >= datetime.timedelta(minutes=10):
        jwt_pro = retrieve_pro_jwt()
    return jwt_pro