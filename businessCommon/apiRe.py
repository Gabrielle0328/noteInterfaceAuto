import requests
import json
from common.logCreate import info, error


class ApiRe:
    @staticmethod
    def post(url, body, wps_sid, userId, headers=None):
        if headers is None:  # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            headers = {
                'Content-Type': 'application/json',
                'Cookie': wps_sid,
                'X-user-key': str(userId)
            }
        info(f're url: {url}')
        info(f're headers: {json.dumps(headers)}')
        info(f're body: {json.dumps(body)}')
        try:
            res = requests.post(url=url, headers=headers, json=body, timeout=3)
        except TimeoutError:
            error(f'{url} api requests timeout!')
            return 'timeout'

        info(f'res code: {res.status_code}')
        info(f'res body: {res.text}')
        return res

    @staticmethod  #因为以下没有用到self属性，可标为静态方法并去掉self
    def get(url, wps_sid, headers=None):
        if headers is None:  # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            headers = {
                'Cookie': wps_sid
            }
        info(f're url:{url}')
        info(f're headers:{json.dumps(headers)}')
        # info(f're body: {json.dumps(body)}')  # get请求没有body
        try:
            res = requests.get(url=url, headers=headers, timeout=3)
        except TimeoutError:
            error(f'{url} api requests timeout!')
            return 'timeout'
        info(f'res code:{res.status_code}')
        info(f'res body{res.text}')
        return res
