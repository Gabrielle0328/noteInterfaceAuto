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

@class_case_log
class UploadNotesContentHandle(unittest.TestCase):
    envConfig = YamlRead().env_config()
    host = envConfig['host']
    userid1 = envConfig['userId1']
    wps_sid1 = envConfig['wps_sid1']
    userid2 = envConfig['userId2']
    wps_sid2 = envConfig['wps_sid2']
    userId1_error = envConfig['userId1_error']
    wps_sid1_error = envConfig['wps_sid1_error']
    userId1_overdue = envConfig['userId1_overdue']
    wps_sid1_overdue = envConfig['wps_sid1_overdue']

    expect = {"responseTime": int, "webNotes": [
        {"noteId": "d54930427dd4ebd9679002c584b0787f", "createTime": int, "star": 0, "remindTime": 0,
         "remindType": 0, "infoVersion": 1, "infoUpdateTime": int, "groupId": None,
         "title": "75u8dlZyTLqWCm/b2PLNlg==", "summary": "pIDnRrCwq8sUW3gyWpo7iw==", "thumbnail": None,
         "contentVersion": 3, "contentUpdateTime": int}]}

    def setUp(self) -> None:
        Clear().note_clear(self.userid1, self.wps_sid1)

    # Cookie
    # 校验(required)Cookie:字段缺失
    def testCase01_input(self):
        """校验(required)Cookie:字段缺失"""
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            # 'Cookie': self.wps_sid1,
            'X-user-key': self.userid1
        }
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=headers, body=content_data)  # json=body,body=data
        expect = {"errorCode": -2009, "errorMsg": ""}
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())

    # 校验(required)Cookie:值为 空字符/None >>>>>>>>>>>>
    @parameterized.expand([' ', None])
    def testCase02_input(self, cookie):
        """校验(required)Cookie:字段缺失"""

        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)

        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': cookie,
            'X-user-key': self.userid1
        }
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=headers, body=content_data)  # json=body,body=data
        expect = {"errorCode": -2009, "errorMsg": ""}
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())

    # 校验(required)Cookie:错误的、过期的
    @parameterized.expand([wps_sid1_error, wps_sid1_overdue])
    def testCase02_input(self, C):
        """校验(required)Cookie:错误的、过期的"""
        # 前置
        step('用户A新增一条便签数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1)
        # 操作
        step('用户A请求获取首页便签接口')
        startindex = 0
        rows = 10
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        headers = {
            'Cookie': C
        }
        res = requests.get(url=self.host + path, headers=headers, timeout=3)
        print(res.json(), res.status_code)
        expect = {'errorCode': -2010, 'errorMsg': ''}
        self.assertEqual(401, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())

    # userId
    # 必填--校验(required)userId:字段缺失
    def testCase03_input(self):
        """校验(required)userId:字段缺失"""
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': self.wps_sid1,
            # 'X-user-key': self.userid1
        }
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=headers, body=content_data)  # json=body,body=data
        expect = {"errorCode": -1011, "errorMsg": "X-user-key header Requested!"}
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())

    # 必填--校验(required)userId:空字符串''、传入空值None  >>>>>>>>>>>>>>>>>>>>>>
    @parameterized.expand([' ', None])
    def testCase04_input(self, X_user_key):
        """校验(required)Cookie:字段缺失"""
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': self.wps_sid1,
            'X-user-key': X_user_key
        }
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=headers, body=content_data)  # json=body,body=data
        expect = {"errorCode": -1011, "errorMsg": "X-user-key header Requested!"}
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())

    # 数据类型int检验--校验(required)userId:符合长度的字符串形式('你好abc'
    def testCase05_input(self):
        """校验(required)Cookie:字段缺失"""
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': self.wps_sid1,
            'X-user-key': 'asdfghjkl'
        }
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=headers, body=content_data)  # json=body,body=data
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())

    # 数据类型int检验--校验(required)userId:符合长度的字符串形式'!!!!')
    def testCase06_input(self):
        """校验(required)Cookie:字段缺失"""
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': self.wps_sid1,
            'X-user-key': '!!!!!'
        }
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=headers, body=content_data)  # json=body,body=data
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())

    # 数据类型int检验--校验(required)userId:超过长度 范围超过的值9999999999999999999999999999999999999999999999999999999999999999999999)
    def testCase07_input(self):
        """校验(required)userId:超过长度范围的值999999999999999999"""
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': self.wps_sid1,
            'X-user-key': '99999999999999999999999999999999999999999999999999999999'
        }
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=headers, body=content_data)  # json=body,body=data
        expect = {"errorCode": -7, "errorMsg": "参数类型错误！"}
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())

    # 数据类型int检验--校验(required)userId:int最值范围 2147483649)
    def testCase08_input(self):
        """校验(required)userId:int的最大值 9223372036854775807"""
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': self.wps_sid1,
            'X-user-key': '9223372036854775807'
        }
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=headers, body=content_data)  # json=body,body=data
        expect = {"errorCode": -1011, "errorMsg": "user change!"}
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())

    # 数据类型int检验--校验(required)userId:int最值范围 -2147483649)
    def testCase09_input(self):
        """校验(required)userId:超过长度范围的值999999999999999999"""
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': self.wps_sid1,
            'X-user-key': '-9223372036854775807'
        }
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=headers, body=content_data)  # json=body,body=data
        expect = {"errorCode": -1011, "errorMsg": "user change!"}
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())

    # 数据类型int检验--校验(required)userId:特殊值 0, -1,                 >>>>>>>>>>>>>>>>>>>>>>>>>
    @parameterized.expand([0, -1])
    def testCase10_input(self, X_user_key):
        """ 数据类型int检验--校验(required)userId:特殊值 0, -1 """
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': self.wps_sid1,
            'X-user-key': X_user_key
        }
        content_data = {
            'noteId': cb_res,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=headers, body=content_data)  # json=body,body=data
        expect = {"errorCode": -1011, "errorMsg": "user change!"}
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())

    # 必填--校验(required)noteId:字段缺失
    def testCase11_input(self):
        """校验(required)userId:字段缺失"""
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': self.wps_sid1,
            # 'X-user-key': self.userid1
        }
        content_data = {
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=headers, body=content_data)  # json=body,body=data
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        self.assertEqual(500, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())

    # 必填--校验(required)noteId:空字符串''、传入空值None  >>>>>>>>>>>>>>>>>>>>>>
    @parameterized.expand([' ', None])
    def testCase12_input(self, noteid):
        """校验(required)Cookie:空字符串''、传入空值None"""
        # 前置
        step('用户A新增一条 首页便签 主体')
        cb_res = CreateBody().note_body_create()[0]
        print(cb_res)
        # 操作
        step('用户A请求"3.上传/更新便签内容"接口')
        path = '/v3/notesvr/set/notecontent'
        headers = {
            'Content-Type': 'application/json',
            'Cookie': self.wps_sid1,
            'X-user-key': self.userid1
        }
        content_data = {
            'noteId': noteid,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=headers, body=content_data)  # json=body,body=data
        expect = {"errorCode": -1011, "errorMsg": "参数不合法！"}
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())
