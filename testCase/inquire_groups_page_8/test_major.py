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
        8.查看分组下便签
        """
        # 前置1
        step('用户A请求接口"7.新增分组"')
        res7 = InterfaceCall().Create_group_7(self.userid1, self.wps_sid1)
        print(res7["groupId"])
        # 前置2
        step('用户A请求接口"2新增分组便签主体"')
        noteid_body = InterfaceCall().create_note_body_2(self.userid1, self.wps_sid1, groupId=res7["groupId"])
        # 前置3
        step('用户A请求接口"3.新增分组便签内容"')
        noteid_content = InterfaceCall().create_note_content_3(self.userid1, self.wps_sid1, noteid_body["noteId"])
        # 操作
        step('用户A请求接口"8.查看分组下便签"')
        expect8 = {"noteId": noteid_content["noteId"], "createTime": int, "star": 0,
                   "remindTime": 0, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
                   "groupId": res7["groupId"], "title": noteid_content["title"],
                   "summary": noteid_content["summary"], "thumbnail": None,
                   "contentVersion": 1, "contentUpdateTime": int}
        InterfaceCall().group_note_get_8(self.userid1, self.wps_sid1, expect8,noteid_content["noteId"],
                                         res7["groupId"])

