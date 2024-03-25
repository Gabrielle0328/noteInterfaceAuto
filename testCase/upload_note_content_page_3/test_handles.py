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

    # 状态限制: 已新建 首页便签 主体
    def testCase01_handle(self):
        """
        状态限制
        noteId不存在，首页便签 主体新增
        """
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())
        # 调用接口“4.获取便签内容”查看返回体对齐内容
        path_note_get = '/v3/notesvr/get/notebody'
        data_note_get = {
            'noteIds': [cb_res],
        }
        res4 = ApiRe().post(url=self.host + path_note_get, userId=self.userid1, wps_sid=self.wps_sid1,
                            headers=self.headers, body=data_note_get)  # json=body,body=data
        print(res4.json())
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        for i in res4.json()["noteBodies"]:
            # if i["noteId"] == content_data["noteId"]:
            if i["noteId"] == cb_res:
                CheckMethod().output_check(expect4, i)

    # 状态限制: 已新建 分组便签 主体
    def testCase02_handle(self):
        """
        状态限制
        noteId不存在，分组便签 主体新增
        """
        # 前置1
        step('用户A新增一个 分组')
        path7 = '/v3/notesvr/set/notegroup'
        data7 = {
            "groupId": "A",
            "groupName": "A",
            "order": 0
        }
        res7 = requests.post(url=self.host + path7, headers=self.headers, json=data7)
        # 前置2
        step('用户A新增一条 分组便签 主体')
        cb_res = CreateBody().note_body_create(groupId='A')[0]
        print(cb_res)
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())
        # 调用接口“4.获取便签内容”查看返回体对齐内容
        path_note_get = '/v3/notesvr/get/notebody'
        data_note_get = {
            'noteIds': [cb_res],
        }
        res4 = ApiRe().post(url=self.host + path_note_get, userId=self.userid1, wps_sid=self.wps_sid1,
                            headers=self.headers, body=data_note_get)  # json=body,body=data
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        for i in res4.json()["noteBodies"]:
            if i["noteId"] == content_data["noteId"]:
                CheckMethod().output_check(expect4, i)
        # 调用接口“8.查看分组下便签”查看返回体对齐内容
        path8 = '/v3/notesvr/web/getnotes/group'
        data8 = {
            "groupId": "A"
        }
        res8 = requests.post(url=self.host + path8, headers=self.headers, json=data8)
        expect8 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
                   "remindTime": 0, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
                   "groupId": "A", "title": "test", "summary": "test", "thumbnail": None,
                   "contentVersion": 1, "contentUpdateTime": int
                   }
        for i in res8.json()["webNotes"]:
            if i["noteId"] == content_data["noteId"]:
                CheckMethod().output_check(expect8, i)

    # 状态限制: 已新建 日历便签 主体
    def testCase03_handle(self):
        """
        状态限制
        noteId不存在，日历便签 主体新增
        """
        # 前置1
        step('用户A新增一条 日历便签 主体')
        remindTime = int(time.time())
        cb_res = CreateBody().note_body_create(remindTime=remindTime, remindType=0)[0]
        print(cb_res)
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())
        # 调用接口“4.获取便签内容”查看返回体对齐内容
        path_note_get = '/v3/notesvr/get/notebody'
        data_note_get = {
            'noteIds': [cb_res],
        }
        res4 = ApiRe().post(url=self.host + path_note_get, userId=self.userid1, wps_sid=self.wps_sid1,
                            headers=self.headers, body=data_note_get)  # json=body,body=data
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        for i in res4.json()["noteBodies"]:
            if i["noteId"] == content_data["noteId"]:
                CheckMethod().output_check(expect4, i)
        # 调用接口“10.查看日历下便签”查看返回体对齐内容  2024-01~2024-03
        path10 = '/v3/notesvr/web/getnotes/remind'
        data10 = {
            "remindStartTime": 1703952000, "remindEndTime": 1709136000, "startIndex": 0, "rows": 999
        }
        res10 = requests.post(url=self.host + path10, headers=self.headers, json=data10)
        expect10 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
                    "remindTime": remindTime, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
                    "groupId": None, "title": "test", "summary": "test", "thumbnail": None,
                    "contentVersion": 1, "contentUpdateTime": int
                    }
        for i in res10.json()["webNotes"]:
            if i["noteId"] == content_data["noteId"]:
                CheckMethod().output_check(expect10, i)

    # 重复数据: 已新建 首页便签 主体,上传一次内容，上传相同的内容
    def testCase04_handle(self):
        """
        状态限制
        noteId不存在，首页便签 主体新增
        """
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)
        # 操作1
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())
        # 验证1
        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)
        # path_note_get = '/v3/notesvr/get/notebody'
        # data_note_get = {
        #     'noteIds': [cb_res],
        # }
        # res4 = ApiRe().post(url=self.host + path_note_get, userId=self.userid1, wps_sid=self.wps_sid1,
        #                     headers=self.headers, body=data_note_get)  # json=body,body=data
        # print(res4.json())
        # for i in res4.json()["noteBodies"]:
        #     # if i["noteId"] == content_data["noteId"]:
        #     if i["noteId"] == cb_res:
        #         CheckMethod().output_check(expect4, i)
        # 操作2
        content_data["localContentVersion"] = 1
        res_1 = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                             headers=self.headers, body=content_data)  # json=body,body=data
        print(res_1.json())
        expect["contentVersion"] = 2
        CheckMethod().output_check(expect, res_1.json())
        # 验证2
        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4["contentVersion"] = 2
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)
        # res4_1 = ApiRe().post(url=self.host + path_note_get, userId=self.userid1, wps_sid=self.wps_sid1,
        #                       headers=self.headers, body=data_note_get)  # json=body,body=data
        # print(res4_1.json())
        # for i in res4_1.json()["noteBodies"]:
        #     # if i["noteId"] == content_data["noteId"]:
        #     if i["noteId"] == cb_res:
        #         CheckMethod().output_check(expect4, i)

    # 重复数据: 已新建 分组便签 主体上传一次内容，上传相同的内容
    def testCase05_handle(self):
        """
        状态限制
        noteId不存在，分组便签 主体新增
        """
        # 前置1
        step('用户A新增一个 分组')
        path7 = '/v3/notesvr/set/notegroup'
        data7 = {
            "groupId": "A",
            "groupName": "A",
            "order": 0
        }
        res7 = requests.post(url=self.host + path7, headers=self.headers, json=data7)
        # 前置2
        step('用户A新增一条 分组便签 主体')
        cb_res = CreateBody().note_body_create(groupId='A')[0]
        print(cb_res)
        # 操作1
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())

        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)
        # path_note_get = '/v3/notesvr/get/notebody'
        # data_note_get = {
        #     'noteIds': [cb_res],
        # }
        # res4 = ApiRe().post(url=self.host + path_note_get, userId=self.userid1, wps_sid=self.wps_sid1,
        #                     headers=self.headers, body=data_note_get)  # json=body,body=data
        # for i in res4.json()["noteBodies"]:
        #     if i["noteId"] == content_data["noteId"]:
        #         CheckMethod().output_check(expect4, i)

        step('调用接口“8.查看分组下便签”查看返回体对齐内容')
        expect8 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
                   "remindTime": 0, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
                   "groupId": "A", "title": "test", "summary": "test", "thumbnail": None,
                   "contentVersion": 1, "contentUpdateTime": int
                   }
        InterfaceCall().group_note_get_8(self.userid1, self.wps_sid1, content_data, expect8)
        # path8 = '/v3/notesvr/web/getnotes/group'
        # data8 = {
        #     "groupId": "A"
        # }
        # res8 = requests.post(url=self.host + path8, headers=self.headers, json=data8)
        # for i in res8.json()["webNotes"]:
        #     if i["noteId"] == content_data["noteId"]:
        #         CheckMethod().output_check(expect8, i)

        # 操作2
        step('用户A请求"3.上传/更新便签内容"接口')
        content_data["localContentVersion"] = 1
        res_1 = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                             body=content_data)  # json=body,body=data
        print(res_1.json())
        expect["contentVersion"] = 2
        CheckMethod().output_check(expect, res_1.json())

        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4["contentVersion"] = 2
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)
        # res4_1 = ApiRe().post(url=self.host + path_note_get, userId=self.userid1, wps_sid=self.wps_sid1,
        #                       headers=self.headers, body=data_note_get)  # json=body,body=data
        # print(res4_1.json())
        # for i in res4_1.json()["noteBodies"]:
        #     # if i["noteId"] == content_data["noteId"]:
        #     if i["noteId"] == cb_res:
        #         CheckMethod().output_check(expect4, i)

        step('调用接口“8.查看分组下便签”查看返回体对齐内容')
        expect8["contentVersion"] = 2
        InterfaceCall().group_note_get_8(self.userid1, self.wps_sid1, content_data, expect8)
        # res8_1 = requests.post(url=self.host + path8, headers=self.headers, json=data8)
        # for i in res8_1.json()["webNotes"]:
        #     if i["noteId"] == content_data["noteId"]:
        #         CheckMethod().output_check(expect8, i)

    # 重复数据: 已新建 日历便签 主体上传一次内容，上传相同的内容
    def testCase06_handle(self):
        """
        状态限制
        noteId不存在，日历便签 主体新增
        """
        # 前置1
        step('用户A新增一条 日历便签 主体')
        remindTime = int(time.time())
        cb_res = CreateBody().note_body_create(remindTime=remindTime, remindType=0)[0]
        print(cb_res)
        # 操作1
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())

        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)

        step('调用接口“10.查看日历下便签”查看返回体对齐内容  2024-01~2024-03')
        expect10 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
                    "remindTime": remindTime, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
                    "groupId": None, "title": "test", "summary": "test", "thumbnail": None,
                    "contentVersion": 1, "contentUpdateTime": int
                    }
        InterfaceCall().calendar_note_get_10(self.userid1, self.wps_sid1, remindTime, content_data, expect10)

        # 操作2
        step('用户A请求"3.上传/更新便签内容"接口')
        content_data["contentVersion"] = 1
        res_1 = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                             body=content_data)  # json=body,body=data
        expect["contentVersion"] = 2
        CheckMethod().output_check(expect, res_1.json())

        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4["contentVersion"] = 2
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)
        # res4_1 = ApiRe().post(url=self.host + path_note_get, userId=self.userid1, wps_sid=self.wps_sid1,
        #                       headers=self.headers, body=data_note_get)  # json=body,body=data
        # print(res4_1.json())
        # for i in res4_1.json()["noteBodies"]:
        #     # if i["noteId"] == content_data["noteId"]:
        #     if i["noteId"] == cb_res:
        #         CheckMethod().output_check(expect4, i)
        #
        step('调用接口“10.查看日历下便签”查看返回体对齐内容  2024-01~2024-03')
        expect10["contentVersion"] = 2
        InterfaceCall().calendar_note_get_10(self.userid1, self.wps_sid1, remindTime, content_data, expect10)
        # res10_1 = requests.post(url=self.host + path10, headers=self.headers, json=data10)
        # for i in res10_1.json()["webNotes"]:
        #     if i["noteId"] == content_data["noteId"]:
        #         CheckMethod().output_check(expect10, i)

    # 重复数据: 已新建 首页便签 主体,上传一次内容，更新内容
    def testCase07_handle(self):
        """
        状态限制
        noteId不存在，首页便签 主体新增
        """
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)

        # 操作1
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())
        # 验证1
        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)

        # 操作2
        content_data["localContentVersion"] = 1
        content_data["title"] = 'test1'
        content_data["summary"] = 'test1'
        content_data["body"] = 'test1'
        res_1 = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                             body=content_data)  # json=body,body=data
        print(res_1.json())
        expect["contentVersion"] = 2
        CheckMethod().output_check(expect, res_1.json())
        # 验证2
        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 2, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)

    # 重复数据: 已新建 分组便签 主体,上传一次内容，更新内容
    def testCase08_handle(self):
        """
        状态限制
        noteId不存在，分组便签 主体新增
        """
        # 前置1
        step('用户A新增一个 分组')
        path7 = '/v3/notesvr/set/notegroup'
        data7 = {
            "groupId": "A",
            "groupName": "A",
            "order": 0
        }
        res7 = requests.post(url=self.host + path7, headers=self.headers, json=data7)
        # 前置2
        step('用户A新增一条 分组便签 主体')
        cb_res = CreateBody().note_body_create(groupId='A')[0]
        print(cb_res)

        # 操作1
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())
        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)
        # 验证1
        step('调用接口“8.查看分组下便签”查看返回体对齐内容')
        expect8 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
                   "remindTime": 0, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
                   "groupId": "A", "title": "test", "summary": "test", "thumbnail": None,
                   "contentVersion": 1, "contentUpdateTime": int
                   }
        InterfaceCall().group_note_get_8(self.userid1, self.wps_sid1, content_data, expect8)

        # 操作2
        step('用户A请求"3.上传/更新便签内容"接口')
        content_data["localContentVersion"] = 1
        content_data["title"] = 'test1'
        content_data["summary"] = 'test1'
        content_data["body"] = 'test1'
        res_1 = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                             body=content_data)  # json=body,body=data
        print(res_1.json())
        expect["contentVersion"] = 2
        CheckMethod().output_check(expect, res_1.json())
        # 验证2
        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 2, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)
        step('调用接口“8.查看分组下便签”查看返回体对齐内容')
        expect8 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
                   "remindTime": 0, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
                   "groupId": "A", "title": "test1", "summary": "test1", "thumbnail": None,
                   "contentVersion": 2, "contentUpdateTime": int
                   }
        InterfaceCall().group_note_get_8(self.userid1, self.wps_sid1, content_data, expect8)

    # 重复数据: 已新建 日历便签 主体,上传一次内容，更新内容
    def testCase09_handle(self):
        """
        状态限制
        noteId不存在，日历便签 主体新增
        """
        # 前置1
        step('用户A新增一条 日历便签 主体')
        remindTime = int(time.time())
        cb_res = CreateBody().note_body_create(remindTime=remindTime, remindType=0)[0]
        print(cb_res)
        # 操作1
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())

        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)

        step('调用接口“10.查看日历下便签”查看返回体对齐内容  2024-01~2024-03')
        expect10 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
                    "remindTime": remindTime, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
                    "groupId": None, "title": "test", "summary": "test", "thumbnail": None,
                    "contentVersion": 1, "contentUpdateTime": int
                    }
        InterfaceCall().calendar_note_get_10(self.userid1, self.wps_sid1, remindTime, content_data, expect10)

        # 操作2
        step('用户A请求"3.上传/更新便签内容"接口')
        content_data["contentVersion"] = 1
        content_data["title"] = 'test1'
        content_data["summary"] = 'test1'
        content_data["body"] = 'test1'
        res_1 = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                             body=content_data)  # json=body,body=data
        expect["contentVersion"] = 2
        CheckMethod().output_check(expect, res_1.json())
        # 验证2
        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 2, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)
        step('调用接口“10.查看日历下便签”查看返回体对齐内容  2024-01~2024-03')
        expect10 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
                    "remindTime": remindTime, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
                    "groupId": None, "title": "test1", "summary": "test1", "thumbnail": None,
                    "contentVersion": 2, "contentUpdateTime": int
                    }
        InterfaceCall().calendar_note_get_10(self.userid1, self.wps_sid1, remindTime, content_data, expect10)

    # 越权:'用户A'已新增 主页便签 主体，使用'用户B'的账号 增加 首页便签的主体
    def testCase10_handle(self):
        """
        状态限制
        noteId不存在，首页便签 主体新增
        """
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)
        # 操作1
        step('"用户B"请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid2, wps_sid=self.wps_sid2,
                           body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())
        # 验证1
        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = []
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)

    # 越权:'用户A'已新增 分组便签 主体，使用'用户B'的账号 增加 分组便签的主体
    def testCase11_handle(self):
        """
        状态限制
        noteId不存在，分组便签 主体新增
        """
        # 前置1
        step('用户A新增一个 分组')
        path7 = '/v3/notesvr/set/notegroup'
        data7 = {
            "groupId": "A",
            "groupName": "A",
            "order": 0
        }
        res7 = requests.post(url=self.host + path7, headers=self.headers, json=data7)
        # 前置2
        step('用户A新增一条 分组便签 主体')
        cb_res = CreateBody().note_body_create(groupId='A')[0]
        print(cb_res)
        # 操作1
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid2, wps_sid=self.wps_sid2,
                           body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())

        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)

        step('调用接口“8.查看分组下便签”查看返回体对齐内容')
        expect8 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
                   "remindTime": 0, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
                   "groupId": "A", "title": "test", "summary": "test", "thumbnail": None,
                   "contentVersion": 1, "contentUpdateTime": int
                   }
        InterfaceCall().group_note_get_8(self.userid1, self.wps_sid1, content_data, expect8)

    # 越权:'用户A'已新增 日历便签 主体，使用'用户B'的账号 增加 分组便签的主体
    def testCase12_handle(self):
        """
        状态限制
        noteId不存在，日历便签 主体新增
        """
        # 前置1
        step('用户A新增一条 日历便签 主体')
        remindTime = int(time.time())
        cb_res = CreateBody().note_body_create(remindTime=remindTime, remindType=0)[0]
        print(cb_res)
        # 操作1
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid2, wps_sid=self.wps_sid2,
                           body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())

        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)

        step('调用接口“10.查看日历下便签”查看返回体对齐内容  2024-01~2024-03')
        expect10 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
                    "remindTime": remindTime, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
                    "groupId": None, "title": "test", "summary": "test", "thumbnail": None,
                    "contentVersion": 1, "contentUpdateTime": int
                    }
        InterfaceCall().calendar_note_get_10(self.userid1, self.wps_sid1, remindTime, content_data, expect10)

    # 越权:'用户A'已新增 首页便签 主体和内容，使用'用户B'的账号 更新 首页便签的主体
    def testCase13_handle(self):
        """
        状态限制
        noteId不存在，首页便签 主体新增
        """
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)

        # 操作1
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())
        # 验证1
        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)

        # 操作2
        content_data["localContentVersion"] = 1
        content_data["title"] = 'test1'
        content_data["summary"] = 'test1'
        content_data["body"] = 'test1'
        res_1 = ApiRe().post(url=self.host + path, userId=self.userid2, wps_sid=self.wps_sid2,
                             body=content_data)  # json=body,body=data
        print(res_1.json())
        expect["contentVersion"] = 1  # 使用'用户B'修改'用户A'便签的主体，相当于在'用户B'账户上直接新增主体，此时版本自然为1
        CheckMethod().output_check(expect, res_1.json())
        # 验证2
        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)

    # 越权:'用户A'已新增 分组便签 主体和内容，使用'用户B'的账号 更新 分组便签的主体
    def testCase14_handle(self):
        """
        状态限制
        noteId不存在，分组便签 主体新增
        """
        # 前置1
        step('用户A新增一个 分组')
        path7 = '/v3/notesvr/set/notegroup'
        data7 = {
            "groupId": "A",
            "groupName": "A",
            "order": 0
        }
        res7 = requests.post(url=self.host + path7, headers=self.headers, json=data7)
        # 前置2
        step('用户A新增一条 分组便签 主体')
        cb_res = CreateBody().note_body_create(groupId='A')[0]
        print(cb_res)

        # 操作1
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())
        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)
        # 验证1
        step('调用接口“8.查看分组下便签”查看返回体对齐内容')
        expect8 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
                   "remindTime": 0, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
                   "groupId": "A", "title": "test", "summary": "test", "thumbnail": None,
                   "contentVersion": 1, "contentUpdateTime": int
                   }
        InterfaceCall().group_note_get_8(self.userid1, self.wps_sid1, content_data, expect8)

        # 操作2
        step('用户A请求"3.上传/更新便签内容"接口')
        content_data["localContentVersion"] = 1
        content_data["title"] = 'test1'
        content_data["summary"] = 'test1'
        content_data["body"] = 'test1'
        res_1 = ApiRe().post(url=self.host + path, userId=self.userid2, wps_sid=self.wps_sid2,
                             body=content_data)  # json=body,body=data
        print(res_1.json())
        expect["contentVersion"] = 1  # 使用'用户B'修改'用户A'便签的主体，相当于在'用户B'账户上直接新增主体，此时版本自然为1
        CheckMethod().output_check(expect, res_1.json())
        # 验证2
        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)
        step('调用接口“8.查看分组下便签”查看返回体对齐内容')
        InterfaceCall().group_note_get_8(self.userid1, self.wps_sid1, content_data, expect8)

    # 越权:'用户A'已新增 日历便签 主体和内容，使用'用户B'的账号 更新 日历便签的主体
    def testCase15_handle(self):
        """
        状态限制
        noteId不存在，日历便签 主体新增
        """
        # 前置1
        step('用户A新增一条 日历便签 主体')
        remindTime = int(time.time())
        cb_res = CreateBody().note_body_create(remindTime=remindTime, remindType=0)[0]
        print(cb_res)
        # 操作1
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())

        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)

        step('调用接口“10.查看日历下便签”查看返回体对齐内容  2024-01~2024-03')
        expect10 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
                    "remindTime": remindTime, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
                    "groupId": None, "title": "test", "summary": "test", "thumbnail": None,
                    "contentVersion": 1, "contentUpdateTime": int
                    }
        InterfaceCall().calendar_note_get_10(self.userid1, self.wps_sid1, remindTime, content_data, expect10)

        # 操作2
        step('用户A请求"3.上传/更新便签内容"接口')
        content_data["contentVersion"] = 1
        content_data["title"] = 'test1'
        content_data["summary"] = 'test1'
        content_data["body"] = 'test1'
        res_1 = ApiRe().post(url=self.host + path, userId=self.userid2, wps_sid=self.wps_sid2,
                             body=content_data)  # json=body,body=data
        expect["contentVersion"] = 1 # 使用'用户B'修改'用户A'便签的主体，相当于在'用户B'账户上直接新增主体，此时版本自然为1
        CheckMethod().output_check(expect, res_1.json())
        # 验证2
        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, cb_res, content_data, expect4)
        step('调用接口“10.查看日历下便签”查看返回体对齐内容  2024-01~2024-03')
        InterfaceCall().calendar_note_get_10(self.userid1, self.wps_sid1, remindTime, content_data, expect10)

    # 时序:上传(首页、分组、日历)便签内容 之前没有先新增主体 -> 默认建立为首页便签
    def testCase16_handle(self):
        """
        状态限制
        noteId不存在，首页便签 主体新增
        """
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        content_data = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           body=content_data)  # json=body,body=data
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())
        # 验证
        step('调用接口“4.获取便签内容”查看返回体对齐内容')
        expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
                   "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
                   "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
                   "valid": 1}
        InterfaceCall().normal_note_get_4(self.userid1, self.wps_sid1, content_data["noteId"],
                                          content_data, expect4)
        step('调用接口“1.获取首页便签”查看返回体对齐内容')
        expect1 = {"noteId": content_data["noteId"], "createTime": int, "star": 0, "remindTime": 0,
                   "remindType": 0, "infoVersion": 1, "infoUpdateTime": int, "groupId": None,
                   "title": "test", "summary": "test", "thumbnail": None, "contentVersion": 1,
                   "contentUpdateTime": int}
        InterfaceCall().normal_note_get_1(self.userid1, self.wps_sid1, 0, 999, content_data, expect1)
