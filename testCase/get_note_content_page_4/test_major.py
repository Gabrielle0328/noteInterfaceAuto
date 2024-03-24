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
class GetNotesContentMajor(unittest.TestCase):
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
        4.获取便签内容
        """
        # 前置
        step('用户A新增一条 首页便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, groupId='A')
        # 操作
        step('用户A请求"4.获取 首页便签 内容"接口')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"],c_res[0],
                                          expect4)

