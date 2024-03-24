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
        5.删除便签 (软删除)
        """
        # 前置
        step('用户A新增一条 首页便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1)
        # 操作--删除刚才创建的便签(软删除)
        step('用户A请求"5.删除便签(软删除)"接口')
        # expect5 = {"responseTime": int}
        InterfaceCall().delete_note_5(self.userid1, self.wps_sid1, c_res[0]["noteId"])
        # 验证1--调用接口'4.获取便签内容'查看valid值，预期为0
        step('用户A请求接口"4.获取便签内容"')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 0}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)
        # 验证2--调用接口'11.查看回收站下的便签'查看软删除后的便签是否进入回收站
        step('用户A请求接口"11.查看回收站下的便签"')
        expect11 = {
            "noteId": c_res[0]["noteId"], "createTime": int, "star": 0,
            "remindTime": int, "remindType": 0, "infoVersion": 2, "infoUpdateTime": int,
            "groupId": None, "title": c_res[0]["title"], "summary": c_res[0]["summary"],
            "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int
        }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"], expect11)
