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
from businessCommon.interfaceCall import InterfaceCall

@class_case_log  # 实现了类级别的日志装饰器
class CreateGroupMajor(unittest.TestCase):
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
        7.新增分组
        """
        # 前置
        # 操作
        step('用户A请求接口"7.新增分组"')
        res = InterfaceCall().Create_group_7(self.userid1, self.wps_sid1)
        print(res["groupId"])
        # 验证
        step('用户A请求接口"6.获取分组列表"')
        expect6 = {"userId": self.userid1, "groupId": res["groupId"], "groupName": res["groupName"],
                   "order": 0, "valid": 1, "updateTime": int}
        InterfaceCall().Get_groups_6(self.userid1, self.wps_sid1, res["groupId"], expect6)


