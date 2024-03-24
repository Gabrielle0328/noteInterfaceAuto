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
class UploadNotesMajor(unittest.TestCase):
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

    expect = {"responseTime": int, "webNotes": [
        {"noteId": "d54930427dd4ebd9679002c584b0787f", "createTime": int, "star": 0, "remindTime": 0,
         "remindType": 0, "infoVersion": 1, "infoUpdateTime": int, "groupId": None,
         "title": "75u8dlZyTLqWCm/b2PLNlg==", "summary": "pIDnRrCwq8sUW3gyWpo7iw==", "thumbnail": None,
         "contentVersion": 3, "contentUpdateTime": int}]}

    def setUp(self) -> None:
        Clear().note_clear(self.userid1, self.wps_sid1)

    def testCase01_major(self):
        """上传/更新便签主体"""
        # 前置
        # 操作
        step('用户A请求"传/更新便签主体"接口')
        path = '/v3/notesvr/set/noteinfo'
        data = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',
            'star': None,
            'remindTime': None,
            'remindType': None,
            'groupId': None,
        }
        # res = requests.post(url=self.host + path, headers=self.headers, json=data)
        # info(self.host + path)
        # info(headers)
        # res = requests.get(url=self.host + path, headers=headers)
        # info(res.status_code)
        # info(res.text)
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        expect = {"responseTime": int, "infoVersion": 1, "infoUpdateTime": int}
        CheckMethod().output_check(expect, res.json())

    # def testCase02_major(self):
    #     """获取首页主流程"""
    #     # 前置
    #     print('用户A新增一条便签数据')
    #     c_res = CreateNote().create_note(self.userid1, self.sid1, 1)
    #     # 操作
    #     print('用户A请求获取首页便签接口')
    #     startindex = 0
    #     rows = 10
    #     path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
    #     headers = {
    #         'Cookie': f'wps_sid={self.sid1}'
    #     }
    #     print(self.host + path)
    #     print(headers)
    #     res = requests.get(url=self.host + path, headers=headers)
    #     print(res.status_code)
    #     print(res.text)
    #     expect = deepcopy(self.expect)
    #     expect['webNotes'][0]['noteId'] = c_res[0]['noteId']
    #     expect['webNotes'][0]['title'] = c_res[0]['title']
    #     expect['webNotes'][0]['summary'] = c_res[0]['summary']
    #     expect['webNotes'][0]['contentVersion'] = c_res[0]['localContentVersion']
    #     CheckMethod().output_check(expect, res.json())

    # def testCase03_major(self):
    #     """获取首页主流程"""
    #     # 前置
    #     print('用户A新增一条便签数据')
    #     c_res = CreateNote().create_note(self.userid1, self.sid1, 1)
    #     # 操作
    #     print('用户A请求获取首页便签接口')
    #     startindex = 0
    #     rows = 10
    #     path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
    #     headers = {
    #         'Cookie': f'wps_sid={self.sid1}'
    #     }
    #     print(self.host + path)
    #     print(headers)
    #     res = requests.get(url=self.host + path, headers=headers)
    #     print(res.status_code)
    #     print(res.text)
    #     expect = deepcopy(self.expect)
    #     expect['webNotes'][0]['noteId'] = c_res[0]['noteId']
    #     expect['webNotes'][0]['title'] = c_res[0]['title']
    #     expect['webNotes'][0]['summary'] = c_res[0]['summary']
    #     expect['webNotes'][0]['contentVersion'] = c_res[0]['localContentVersion']
    #     CheckMethod().output_check(expect, res.json())
