import unittest
import requests
from common.checkMethods import CheckMethod
from businessCommon.clearNote import Clear
from businessCommon.createNote import Create
from copy import deepcopy
from common.logCreate import info, step, error, class_case_log
from common.yamlRead import YamlRead
import time
from businessCommon.apiRe import ApiRe


@class_case_log  # 实现了类级别的日志装饰器
class CreateBody:
    envConfig = YamlRead().env_config()
    host = envConfig['host']
    userid1 = envConfig['userId1']
    wps_sid1 = envConfig['wps_sid1']
    content_type = 'application/json'
    headers = {
        # 个人账
        'Cookie': wps_sid1,
        'X-User-Key': userid1,
        'Content-Type': content_type  # POST请求时需要
    }

    def note_body_create(self, remindTime=None, remindType=None, groupId=None):
        """
        上传/更新便签主体
        """
        # 前置--新建便签主体
        path = '/v3/notesvr/set/noteinfo'
        info_body = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',  # 只是创建普通便签，其他optional不填
            "star": 0,
            "remindTime": remindTime,
            "remindType": remindType,
            "groupId": groupId
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=info_body)  # json=body,body=data
        infoVersion = res.json()["infoVersion"]
        return info_body["noteId"], infoVersion


if __name__ == "__main__":
    wps_sid1 = 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415'
    userId1 = '758797333'
    print(CreateBody().note_body_create())
