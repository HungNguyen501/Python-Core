import requests
from config import Api

if __name__=='__main__':
    api = Api[0]
    headers = {}
    payload = {}

    response = requests.request(method=api['method'], url=api['url'], headers=headers, data=payload)
    print(response.status_code)
    print(response.content)
