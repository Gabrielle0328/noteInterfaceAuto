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
from parameterized import parameterized
from businessCommon.createNotebody import CreateBody
from businessCommon.interfaceCall import InterfaceCall


@class_case_log
class UploadNotesContentHandle(unittest.TestCase):
    envConfig = YamlRead().env_config()
    host = envConfig['host']
    userid1 = envConfig['userId1']
    wps_sid1 = envConfig['wps_sid1']
    userid2 = envConfig['userId2']
    wps_sid2 = envConfig['wps_sid2']
    content_type = 'application/json'
    headers = {
        # 个人账
        'Cookie': wps_sid1,
        'X-User-Key': userid1,
        'Content-Type': content_type  # POST请求时需要
    }

    expect = {}

    def setUp(self) -> None:
        Clear().note_clear(self.userid1, self.wps_sid1)
        Clear().group_note_clear(self.userid1, self.wps_sid1)
        Clear().calendar_note_clear(self.userid1, self.wps_sid1)

    # 状态限制:软删除已创建好的便签
    # 状态限制:软删除已创建好一条 首页便签

    # 状态限制:软删除已创建好一条 分组便签
    def testCase01_major(self):
        """
        5.删除便签 (软删除)
        """
        # 前置
        step('用户A新增一条 分组便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, groupId='A')
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
            "groupId": 'A', "title": c_res[0]["title"], "summary": c_res[0]["summary"],
            "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int
        }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"], expect11)

    # 状态限制:软删除已创建好一条 日历便签
    def testCase02_major(self):
        """
        5.删除便签 (软删除)
        """
        # 前置
        step('用户A新增一条 日历便签 数据')
        remindTime_set = int(time.time())
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, remindTime=remindTime_set)
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
            "remindTime": remindTime_set, "remindType": 0, "infoVersion": 2, "infoUpdateTime": int,
            "groupId": None, "title": c_res[0]["title"], "summary": c_res[0]["summary"],
            "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int
        }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"], expect11)

    # 越权:‘用户B’获取‘用户A’的便签
    # 越权:"用户B"软删除A已创建好一条 首页便签(无效删除) ，"用户A"调用接口4.获取创建的便签内容、11.查看回收站下的标签
    def testCase03_major(self):
        """
        5.删除便签 (软删除)
        """
        # 前置
        step('用户A新增一条 首页便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1)
        # 操作--'用户B'删除刚才创建的便签(软删除)--实际无效
        step('用户B请求"5.删除便签(软删除)"接口')
        # expect5 = {"responseTime": int}
        InterfaceCall().delete_note_5(self.userid2, self.wps_sid2, c_res[0]["noteId"])
        # 验证1--'用户A'调用接口'4.获取便签内容'查看valid值，预期仍为1
        step('用户A请求接口"4.获取便签内容"')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)
        # 验证2--调用接口'11.查看回收站下的便签'查看软删除后的便签是否进入回收站
        step('用户A请求接口"11.查看回收站下的便签"')
        expect11 = {
            "responseTime": int, "webNotes": []
        }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"], expect11)

    # 越权:"用户B"软删除A已创建好一条 分组便签(无效删除) ，"用户A"调用接口4.获取创建的便签内容、11.查看回收站下的标签
    def testCase04_major(self):
        """
        5.删除便签 (软删除)
        """
        # 前置
        step('用户A新增一条 分组便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, groupId='A')
        # 操作--'用户B'删除刚才创建的便签(软删除)--实际无效
        step('用户B请求"5.删除便签(软删除)"接口')
        # expect5 = {"responseTime": int}
        InterfaceCall().delete_note_5(self.userid2, self.wps_sid2, c_res[0]["noteId"])
        # 验证1--'用户A'调用接口'4.获取便签内容'查看valid值，预期仍为1
        step('用户A请求接口"4.获取便签内容"')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)
        # 验证2--调用接口'11.查看回收站下的便签'查看软删除后的便签是否进入回收站
        step('用户A请求接口"11.查看回收站下的便签"')
        expect11 = {
            "responseTime": int, "webNotes": []
        }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"], expect11)

    # 越权:"用户B"软删除A已创建好一条 日历便签(无效删除) ，"用户A"调用接口4.获取创建的便签内容、11.查看回收站下的标签
    def testCase05_major(self):
        """
        5.删除便签 (软删除)
        """
        # 前置
        step('用户A新增一条 日历便签 数据')
        remindTime_set = int(time.time())
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, remindTime=remindTime_set)
        # 操作--'用户B'删除刚才创建的便签(软删除)--实际无效
        step('用户B请求"5.删除便签(软删除)"接口')
        # expect5 = {"responseTime": int}
        InterfaceCall().delete_note_5(self.userid2, self.wps_sid2, c_res[0]["noteId"])
        # 验证1--'用户A'调用接口'4.获取便签内容'查看valid值，预期仍为1
        step('用户A请求接口"4.获取便签内容"')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)
        # 验证2--调用接口'11.查看回收站下的便签'查看软删除后的便签是否进入回收站
        step('用户A请求接口"11.查看回收站下的便签"')
        expect11 = {
            "responseTime": int, "webNotes": []
        }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"], expect11)