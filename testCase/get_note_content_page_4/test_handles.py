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

    # 状态限制:已创建好的便签
    # 状态限制:已创建好一条 首页便签 ，获取便签内容
    def testCase01_handle(self):
        """
        状态限制:已创建好一条首页便签，获取便签内容
        """
        step('用户A新增一条 首页便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1)
        # 操作--上传便签内容
        step('用户A请求"获取 首页便签 内容"接口')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)

    # 状态限制:已创建好一条 分组便签 ，获取便签内容
    def testCase02_handle(self):
        """
        状态限制:已创建好一条首页便签，获取便签内容
        """
        step('用户A新增一条 首页便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1)
        # 操作--上传便签内容
        step('用户A请求"获取 首页便签 内容"接口')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)

    # 状态限制:已创建好一条 日历便签 ，获取便签内容
    def testCase03_handle(self):
        """
        状态限制:已创建好一条首页便签，获取便签内容
        """
        # 前置
        step('用户A新增一条 首页便签 数据')
        remindTime_set = int(time.time())
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, remindTime=remindTime_set)
        # 操作--上传便签内容
        step('用户A请求"获取 首页便签 内容"接口')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)

    # 状态限制:已创建好的便签删除到回收站
    # 状态限制:将已经创建的 首页便签 删除到回收站中，获取便签内容
    def testCase04_handle(self):
        """
        状态限制:已创建好一条首页便签，获取便签内容
        """
        # 前置1
        step('用户A新增一条 首页便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1)
        # 前置2
        step('用户A删除刚才创建的 首页便签 数据')
        InterfaceCall().delete_note_5(self.userid1, self.wps_sid1, noteid=c_res[0]["noteId"])
        step('请求接口"11.查看回收站便签"可见被删除的便签')
        expect11 = {"noteId": c_res[0]["noteId"], "createTime": int, "star": 0,
                    "remindTime": int, "remindType": 0, "infoVersion": 2, "infoUpdateTime": int,
                    "groupId": None, "title": c_res[0]["title"], "summary": c_res[0]["summary"],
                    "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int
                    }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 操作--上传便签内容
        step('用户A请求"获取 首页便签 内容"接口')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 0}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)

    # 状态限制:将已经创建的 分组便签 删除到回收站中，获取便签内容
    def testCase05_handle(self):
        """
        状态限制:已创建好一条分组便签，获取便签内容
        """
        # 前置1
        step('用户A新增一条 分组便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, groupId='A')
        # 前置2
        step('用户A删除刚才创建的 分组便签 数据')
        InterfaceCall().delete_note_5(self.userid1, self.wps_sid1, noteid=c_res[0]["noteId"])
        step('请求接口"11.查看回收站便签"可见被删除的便签')
        expect11 = {"noteId": c_res[0]["noteId"], "createTime": int, "star": 0,
                    "remindTime": int, "remindType": 0, "infoVersion": 2, "infoUpdateTime": int,
                    "groupId": 'A', "title": c_res[0]["title"], "summary": c_res[0]["summary"],
                    "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int
                    }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 操作--上传便签内容
        step('用户A请求"获取便签内容"接口')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 0}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)

    # 状态限制:将已经创建的 日历便签 删除到回收站中，获取便签内容
    def testCase06_handle(self):
        """
        状态限制:已创建好一条日历便签，获取便签内容
        """
        # 前置1
        step('用户A新增一条 日历便签 数据')
        remindTime_set = int(time.time())
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, remindTime=remindTime_set)
        # 前置2
        step('用户A删除刚才创建的 日历便签 数据')
        InterfaceCall().delete_note_5(self.userid1, self.wps_sid1, noteid=c_res[0]["noteId"])
        step('请求接口"11.查看回收站便签"可见被删除的便签')
        expect11 = {"noteId": c_res[0]["noteId"], "createTime": int, "star": 0,
                    "remindTime": remindTime_set, "remindType": 0, "infoVersion": 2, "infoUpdateTime": int,
                    "groupId": None, "title": c_res[0]["title"], "summary": c_res[0]["summary"],
                    "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int
                    }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 操作--上传便签内容
        step('用户A请求"获取便签内容"接口')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 0}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)

    # 状态限制:将在回收站的便签恢复， 获取便签内容
    # 状态限制:将在回收站的 首页便签 恢复， 获取便签内容
    def testCase07_handle(self):
        """
        状态限制:已创建好一条首页便签，获取便签内容
        """
        # 前置1
        step('用户A新增一条 首页便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1)
        # 前置2
        step('用户A删除刚才创建的 首页便签 数据')
        InterfaceCall().delete_note_5(self.userid1, self.wps_sid1, noteid=c_res[0]["noteId"])
        step('请求接口"11.查看回收站便签"可见被删除的便签')
        expect11 = {"noteId": c_res[0]["noteId"], "createTime": int, "star": 0,
                    "remindTime": int, "remindType": 0, "infoVersion": 2, "infoUpdateTime": int,
                    "groupId": None, "title": c_res[0]["title"], "summary": c_res[0]["summary"],
                    "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int
                    }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 前置3
        step('用户A恢复刚才删除的 首页便签 数据')
        InterfaceCall().Recyclebin_note_recover_12(self.userid1, self.wps_sid1, noteid=c_res[0]["noteId"])
        step('请求接口"11.查看回收站便签"可见便签恢复，不在回收站')
        expect11 = {"responseTime": 0, "webNotes": []}
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 操作--上传便签内容
        step('用户A请求"获取 首页便签 内容"接口')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)

    # 状态限制:将在回收站的 分组便签 恢复， 获取便签内容
    def testCase08_handle(self):
        """
        状态限制:已创建好一条分组便签，获取便签内容
        """
        # 前置1
        step('用户A新增一条 分组便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, groupId='A')
        # 前置2
        step('用户A删除刚才创建的 首页便签 数据')
        InterfaceCall().delete_note_5(self.userid1, self.wps_sid1, noteid=c_res[0]["noteId"])
        step('请求接口"11.查看回收站便签"可见被删除的便签')
        expect11 = {"noteId": c_res[0]["noteId"], "createTime": int, "star": 0,
                    "remindTime": int, "remindType": 0, "infoVersion": 2, "infoUpdateTime": int,
                    "groupId": 'A', "title": c_res[0]["title"], "summary": c_res[0]["summary"],
                    "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int
                    }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 前置3
        step('用户A恢复刚才删除的 首页便签 数据')
        InterfaceCall().Recyclebin_note_recover_12(self.userid1, self.wps_sid1, noteid=c_res[0]["noteId"])
        step('请求接口"11.查看回收站便签"可见便签恢复，不在回收站')
        expect11 = {"responseTime": 0, "webNotes": []}
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 操作--上传便签内容
        step('用户A请求"获取 首页便签 内容"接口')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)

    # 状态限制:将在回收站的 日历便签 恢复， 获取便签内容
    def testCase09_handle(self):
        """
        状态限制:已创建好一条日历便签，获取便签内容
        """
        # 前置1
        step('用户A新增一条 日历便签 数据')
        remindTime_set = int(time.time())
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, remindTime=remindTime_set)
        # 前置2
        step('用户A删除刚才创建的 日历便签 数据')
        InterfaceCall().delete_note_5(self.userid1, self.wps_sid1, noteid=c_res[0]["noteId"])
        step('请求接口"11.查看回收站便签"可见被删除的便签')
        expect11 = {"noteId": c_res[0]["noteId"], "createTime": int, "star": 0,
                    "remindTime": remindTime_set, "remindType": 0, "infoVersion": 2, "infoUpdateTime": int,
                    "groupId": None, "title": c_res[0]["title"], "summary": c_res[0]["summary"],
                    "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int
                    }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 前置3
        step('用户A恢复刚才删除的 首页便签 数据')
        InterfaceCall().Recyclebin_note_recover_12(self.userid1, self.wps_sid1, noteid=c_res[0]["noteId"])
        step('请求接口"11.查看回收站便签"可见便签恢复，不在回收站')
        expect11 = {"responseTime": 0, "webNotes": []}
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 操作--上传便签内容
        step('用户A请求"获取 首页便签 内容"接口')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)

    # 状态限制:将在回收站的便签彻底删除， 获取便签内容
    # 状态限制:将在回收站的 首页便签 彻底删除， 获取便签内容
    def testCase10_handle(self):
        """
        状态限制:已创建好一条首页便签，获取便签内容
        """
        # 前置1
        step('用户A新增一条 首页便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1)
        # 前置2
        step('用户A删除刚才创建的 首页便签 数据')
        InterfaceCall().delete_note_5(self.userid1, self.wps_sid1, noteid=c_res[0]["noteId"])
        step('请求接口"11.查看回收站便签"可见被删除的便签')
        expect11 = {"noteId": c_res[0]["noteId"], "createTime": int, "star": 0,
                    "remindTime": int, "remindType": 0, "infoVersion": 2, "infoUpdateTime": int,
                    "groupId": None, "title": c_res[0]["title"], "summary": c_res[0]["summary"],
                    "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int
                    }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 前置3
        step('用户A将刚才删除的 首页便签 从回收站彻底删除')
        InterfaceCall().Recyclebin_note_delete_13(self.userid1, self.wps_sid1)
        step('请求接口"11.查看回收站便签"可见便签不在回收站')
        expect11 = {"responseTime": 0, "webNotes": []}
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 操作--上传便签内容
        step('用户A请求"获取 首页便签 内容"接口')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 2}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)

    # 状态限制:将在回收站的 分组便签 彻底删除， 获取便签内容
    def testCase11_handle(self):
        """
        状态限制:已创建好一条分组便签，获取便签内容
        """
        # 前置1
        step('用户A新增一条 分组便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, groupId='A')
        # 前置2
        step('用户A删除刚才创建的 分组便签 数据')
        InterfaceCall().delete_note_5(self.userid1, self.wps_sid1, noteid=c_res[0]["noteId"])
        step('请求接口"11.查看回收站便签"可见被删除的便签')
        expect11 = {"noteId": c_res[0]["noteId"], "createTime": int, "star": 0,
                    "remindTime": int, "remindType": 0, "infoVersion": 2, "infoUpdateTime": int,
                    "groupId": 'A', "title": c_res[0]["title"], "summary": c_res[0]["summary"],
                    "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int
                    }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 前置3
        step('用户A将刚才删除的 首页便签 从回收站彻底删除')
        InterfaceCall().Recyclebin_note_delete_13(self.userid1, self.wps_sid1)
        step('请求接口"11.查看回收站便签"可见便签不在回收站')
        expect11 = {"responseTime": 0, "webNotes": []}
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 操作--上传便签内容
        step('用户A请求"获取 首页便签 内容"接口')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 2}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)

    # 状态限制:将在回收站的 日历便签 彻底删除， 获取便签内容
    def testCase12_handle(self):
        """
        状态限制:已创建好一条日历便签，获取便签内容
        """
        # 前置1
        step('用户A新增一条 日历便签 数据')
        remindTime_set = int(time.time())
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, remindTime=remindTime_set)
        # 前置2
        step('用户A删除刚才创建的 日历便签 数据')
        InterfaceCall().delete_note_5(self.userid1, self.wps_sid1, noteid=c_res[0]["noteId"])
        step('请求接口"11.查看回收站便签"可见被删除的便签')
        expect11 = {"noteId": c_res[0]["noteId"], "createTime": int, "star": 0,
                    "remindTime": remindTime_set, "remindType": 0, "infoVersion": 2, "infoUpdateTime": int,
                    "groupId": None, "title": c_res[0]["title"], "summary": c_res[0]["summary"],
                    "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int
                    }
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 前置3
        step('用户A将刚才删除的 首页便签 从回收站彻底删除')
        InterfaceCall().Recyclebin_note_delete_13(self.userid1, self.wps_sid1)
        step('请求接口"11.查看回收站便签"可见便签不在回收站')
        expect11 = {"responseTime": 0, "webNotes": []}
        InterfaceCall().Recyclebin_note_get_11(self.userid1, self.wps_sid1, c_res[0]["noteId"],
                                               expect11)
        # 操作--上传便签内容
        step('用户A请求"获取 首页便签 内容"接口')
        expect4 = {"summary": c_res[0]["summary"], "noteId": c_res[0]["noteId"],
                   "infoNoteId": c_res[0]["noteId"], "bodyType": 0, "body": c_res[0]["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": c_res[0]["title"],
                   "valid": 2}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, c_res[0]["noteId"], c_res[0],
                                          expect4)

    # 越权:‘用户B’获取‘用户A’的便签
    # 状态限制:"用户A"已创建好一条 首页便签 ，"用户B"获取创建的便签内容
    def testCase13_handle(self):
        """
        状态限制:已创建好一条首页便签，获取便签内容
        """
        step('用户A新增一条 首页便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1)
        # 操作--上传便签内容
        step('用户B请求"获取 首页便签 内容"接口')
        expect4 = {
            "responseTime": int, "noteBodies": []
        }
        InterfaceCall().normal_note_get_4(self.userid2, self.wps_sid2, c_res[0]["noteId"], c_res[0],
                                          expect4)

    # 状态限制:"用户A"已创建好一条 分组便签 ，"用户B"获取创建的便签内容
    def testCase14_handle(self):
        """
        状态限制:已创建好一条分组便签，获取便签内容
        """
        step('用户A新增一条 分组便签 数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, groupId='A')
        # 操作--上传便签内容
        step('用户B请求"获取 分组便签 内容"接口')
        expect4 = {
            "responseTime": int, "noteBodies": []
        }
        InterfaceCall().normal_note_get_4(self.userid2, self.wps_sid2, c_res[0]["noteId"], c_res[0],
                                          expect4)

    # 状态限制:"用户A"已创建好一条 日历便签 ，"用户B"获取创建的便签内容
    def testCase15_handle(self):
        """
        状态限制:已创建好一条日历便签，获取便签内容
        """
        step('用户A新增一条 日历便签 数据')
        remindTime_set = int(time.time())
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, remindTime=remindTime_set)
        # 操作--上传便签内容
        step('用户B请求"获取 日历便签 内容"接口')
        expect4 = {
            "responseTime": int, "noteBodies": []
        }
        InterfaceCall().normal_note_get_4(self.userid2, self.wps_sid2, c_res[0]["noteId"], c_res[0],
                                          expect4)
