import requests
import time


class Create:
    host = 'http://note-api.wps.cn'
    def note_create(self, userid, wps_sid, num, groupId=None, remindTime=None):
        '''
        新建首页便签--2.新建便签主体/3.新建便签内容
        :param userid:
        :param wps_sid:
        :param num:
        :return:
        '''
        # 涉及url请求:2.新建便签主体/3.新建便签内容
        note_create_body_url = f'{self.host}/v3/notesvr/set/noteinfo'
        note_clear_content_url = f'{self.host}/v3/notesvr/set/notecontent'

        notes_list = []
        for i in range(num):
            # 个人账号
            headers = {
                'Cookie': wps_sid,
                'X-User-Key': userid,
                'Content-Type': 'application/json'  # POST请求时需要
            }
            # 新建便签主体
            noteId_set = f'{str(int(time.time() * 1000))}_noteId'
            info_body = {
                'noteId': noteId_set,  # required字段，如果只是创建首页便签，其他optional不填
                "star": 0,
                "remindTime": remindTime,
                "remindType": 0,
                'groupId': groupId
            }
            res = requests.post(note_create_body_url, headers=headers, json=info_body)
            infoVersion = res.json()["infoVersion"]

            # 新建便签内容
            content_body = {
            'noteId': noteId_set,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': infoVersion,
            'BodyType': 0
            }
            notes_list.append(content_body)
            res = requests.post(note_clear_content_url, headers=headers, json=content_body)
        return notes_list


if __name__ == "__main__":
    wps_sid1 = 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415'
    userId1 = '758797333'
    # Create().note_create(userId1, wps_sid1, 1)
    print(Create().note_create(userId1, wps_sid1, 1))
