import requests
from requests.exceptions import HTTPError

class CardocAPI:
    def __init__(self):
        self.reqeust_url = "https://dev.mycar.cardoc.co.kr/v1/trim/"
        self.timeout     = 2

    def get_trim_data(self, trim_id):
        try:
            response = requests.get(self.reqeust_url + str(trim_id), timeout = self.timeout)
            response.raise_for_status()
            return response.json()

        except HTTPError:
            return None

