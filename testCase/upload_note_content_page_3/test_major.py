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
class UploadNotesContentMajor(unittest.TestCase):
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

    # expect = {"noteId": "123--123--123", "title": "test11", "summary": "test111",
    #           "body": "test1111", "localContentVersion": 1, "BodyType": 0}

    def setUp(self) -> None:
        Clear().note_clear(self.userid1, self.wps_sid1)

    def testCase01_major(self):
        """
        上传/更新便签内容
        """
        # 前置--新建便签主体
        path_info = '/v3/notesvr/set/noteinfo'
        info_body = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',  # 只是创建普通便签，其他optional不填
            "star": 0,
            "remindTime": None,
            "remindType": None,
            "groupId": None
        }
        res_info = ApiRe().post(url=self.host + path_info, userId=self.userid1, wps_sid=self.wps_sid1,
                                headers=self.headers, body=info_body)  # json=body,body=data
        infoVersion = res_info.json()["infoVersion"]
        # 操作--上传便签内容
        step('用户A请求"上传传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        data = {
            'noteId': info_body["noteId"],
            'title': 'title_test',
            'summary': 'summary_test',
            'body': 'body_test',
            'localContentVersion': infoVersion,
            'BodyType': 0
        }
        # res = requests.post(url=self.host + path, headers=self.headers, json=data)
        # info(self.host + path)
        # info(headers)
        # res = requests.get(url=self.host + path, headers=headers)
        # info(res.status_code)
        # info(res.text)
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())
        # 调用接口“4.获取便签内容”查看返回体对齐内容
        # 检查改动的title、summary、body、localContentVersion、BodyType
        path_note_get = '/v3/notesvr/get/notebody'
        data_note_get = {
            'noteIds': [data["noteId"]],
        }
        res4 = ApiRe().post(url=self.host + path_note_get, userId=self.userid1, wps_sid=self.wps_sid1,
                            headers=self.headers, body=data_note_get)  # json=body,body=data
        expect = {"summary": data["summary"], "noteId": data["noteId"],
                  "infoNoteId": data["noteId"], "bodyType": 0, "body": data["body"], "contentVersion": 1,
                  "contentUpdateTime": int, "title": data["title"], "valid": 1}
        for i in res4.json()["noteBodies"]:
            if i["noteId"] == data["noteId"]:
                CheckMethod().output_check(expect, i)
