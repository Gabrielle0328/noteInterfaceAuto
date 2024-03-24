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

@class_case_log
class GetPageNotesHandle(unittest.TestCase):
    envConfig = YamlRead().env_config()
    host = envConfig['host']
    userid1 = envConfig['userId1']
    wps_sid1 = envConfig['wps_sid1']
    userid2 = envConfig['userId2']
    wps_sid2 = envConfig['wps_sid2']

    expect = {"responseTime": int, "webNotes": [
        {"noteId": "d54930427dd4ebd9679002c584b0787f", "createTime": int, "star": 0, "remindTime": 0,
         "remindType": 0, "infoVersion": 1, "infoUpdateTime": int, "groupId": None,
         "title": "75u8dlZyTLqWCm/b2PLNlg==", "summary": "pIDnRrCwq8sUW3gyWpo7iw==", "thumbnail": None,
         "contentVersion": 3, "contentUpdateTime": int}]}

    def setUp(self) -> None:
        Clear().note_clear(self.userid1, self.wps_sid1)

    # 只存在1条首页便签，校验查询多行
    def testCase01_handle(self):
        """只存在1条首页便签，校验查询多行"""

        # 前置
        step('用户A新增一条便签数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1)

        # 操作
        step('用户A请求获取首页便签接口')
        startindex = 0
        rows = 10
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = ApiRe().get(url=self.host + path, wps_sid=self.wps_sid1)
        expect = deepcopy(self.expect)
        expect['webNotes'][0]['noteId'] = c_res[0]['noteId']
        expect['webNotes'][0]['title'] = c_res[0]['title']
        expect['webNotes'][0]['summary'] = c_res[0]['summary']
        expect['webNotes'][0]['contentVersion'] = c_res[0]['localContentVersion']
        CheckMethod().output_check(expect, res.json())

    # 只存在1条首页便签，校验 查询所在范围外区间
    def testCase02_handle(self):
        """只存在1条首页便签，校验 查询所在范围外区间"""
        # 前置
        step('用户A新增一条便签数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1)
        # 操作
        step('用户A请求获取首页便签接口')
        startindex = 1
        rows = 10
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = ApiRe().get(url=self.host + path, wps_sid=self.wps_sid1)
        # info(len(res.json()['webNotes']))
        expect = deepcopy(self.expect)
        expect['webNotes'] = []
        CheckMethod().output_check(expect, res.json())

    # 只存在1条分组便签，校验查询
    def testCase03_handle(self):
        """只存在1条 分组 便签，校验查询"""

        # 前置
        step('用户A新增一条分组数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1, groupId="group_1")

        # 操作
        step('用户A请求获取首页便签接口')
        startindex = 0
        rows = 1
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = ApiRe().get(url=self.host + path, wps_sid=self.wps_sid1)
        expect = deepcopy(self.expect)
        expect['webNotes'] = []
        CheckMethod().output_check(expect, res.json())

    # 只存在1条首页便签，校验删除后查询
    def testCase04_handle(self):
        """只存在1条 分组 便签，校验查询"""

        # 前置
        step('用户A新增一条首页便签')
        create_res = Create().note_create(self.userid1, self.wps_sid1, 1, groupId="group_1")
        step('用户A新增清除首页便签')
        clear_res = Clear().note_clear(self.userid1, self.wps_sid1)

        # 操作
        step('用户A请求获取首页便签接口')
        startindex = 0
        rows = 1
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = ApiRe().get(url=self.host + path, wps_sid=self.wps_sid1)
        expect = deepcopy(self.expect)
        expect['webNotes'] = []
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())

    # 越权:用户B查询用户A的首页便签
    def testCase05_handle(self):
        """越权:用户B查询用户A的首页便签"""
        # 前置
        step('用户A新增一条便签数据')
        c_res = Create().note_create(self.userid1, self.wps_sid1, 1)
        # 操作
        step('用户B请求获取首页便签接口')
        startindex = 0
        rows = 1
        path = f'/v3/notesvr/user/{self.userid1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = ApiRe().get(url=self.host + path, wps_sid=self.wps_sid2)
        expect = {"errorCode": -1011, "errorMsg": "user change!"}
        self.assertEqual(412, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        CheckMethod().output_check(expect, res.json())
