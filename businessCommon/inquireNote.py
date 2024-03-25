import requests
# import time


class Inqiure:
    host = 'http://note-api.wps.cn'
    userid = '758797333'  # 同X-User-Key
    wps_sid = 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415'
    content_type = 'application/json'  # POST请求时需要
    headers = {
        # 个人账号
        'Cookie': wps_sid,
        'X-User-Key': userid,
        'Content-Type': content_type  # POST请求时需要
    }

    def note_inquire(self):
        '''
        获取首页便签（单纯的 查询接口）
        :param userid:
        :param wps_sid:
        :param num:
        :return:
        '''
        # 前置  \
        startindex = 0
        rows = 50
        path = f'/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes'
        print(path)
        res = requests.get(url=self.host + path, headers=self.headers)
        print(res.status_code)
        print(res.text)

        return res

if __name__ == "__main__":
    wps_sid1 = 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415'
    userId1 = '758797333'
    Inqiure().note_inquire()
