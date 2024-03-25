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

@class_case_log
class UploadNotesHandle(unittest.TestCase):
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

    # 状态限制: noteId不存在，首页便签 主体新增
    @parameterized.expand([None, 0, 1])
    def testCase01_handle(self, star):
        """
        状态限制
        noteId不存在，首页便签 主体新增
        """
        # 前置
        # 操作
        step('用户A请求"传/更新便签主体"接口')
        path = '/v3/notesvr/set/noteinfo'
        data = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',
            'star': star,
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

    # 状态限制: noteId不存在，分组便签 主体新增
    @parameterized.expand([None, 0, 1])
    def testCase02_handle(self, star):
        """
        状态限制
        noteId不存在，首页便签 主体新增
        """
        # 前置
        # 操作
        step('用户A请求"传/更新便签主体"接口')
        path = '/v3/notesvr/set/noteinfo'
        data = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',
            'star': star,
            'remindTime': None,
            'remindType': None,
            'groupId': 'A',
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

    # 状态限制: noteId已存在，首页便签 主体做更新--重复数据
    @parameterized.expand([None, 0, 1])
    def testCase03_handle(self, star):
        """
        状态限制
        noteId不存在，首页便签 主体新增
        """
        # 前置
        step('前置:用户A新增一条便签主体数据')
        path = '/v3/notesvr/set/noteinfo'
        data = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',
            'star': star,
            'remindTime': None,
            'remindType': None,
            'groupId': None,
        }
        print(data)
        res1 = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        # 操作
        step('用户A请求"上传/更新便签主体"接口')
        print(data)  # 同data
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        expect = {"responseTime": int, "infoVersion": 2, "infoUpdateTime": int}
        CheckMethod().output_check(expect, res.json())

    # 状态限制: noteId已存在，分组便签 主体做更新--重复数据
    @parameterized.expand([None, 0, 1])
    def testCase04_handle(self, star):
        """
        状态限制
        noteId不存在，分组便签 主体新增
        """
        # 前置
        step('前置:用户A新增一条分组便签主体数据')
        path = '/v3/notesvr/set/noteinfo'
        data = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',
            'star': star,
            'remindTime': None,
            'remindType': None,
            'groupId': 'A',
        }
        res1 = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        # 操作
        step('用户A请求"上传/更新便签主体"接口')
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        expect = {"responseTime": int, "infoVersion": 2, "infoUpdateTime": int}
        CheckMethod().output_check(expect, res.json())

    # 状态限制: noteId已存在，首页便签 主体做更新--star改动(枚举值:None——>0, 1)
    @parameterized.expand([[{"star_c": 0, "infoversion_c": 2}],
                           [{"star_c": 1, "infoversion_c": 2}]])
    def testCase05_handle(self, star):
        """
        状态限制
        noteId不存在，分组便签 主体新增
        """
        # 前置
        step('前置:用户A新增一条首页便签主体数据')
        path = '/v3/notesvr/set/noteinfo'
        data = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',
            'star': None,
            'remindTime': None,
            'remindType': None,
            'groupId': None,
        }
        res1 = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        # 操作
        step('用户A请求"上传/更新便签主体"接口')
        data["groupId"] = star["star_c"]
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        expect = {"responseTime": int, "infoVersion": star["infoversion_c"], "infoUpdateTime": int}
        CheckMethod().output_check(expect, res.json())

    # 状态限制: noteId已存在，分组便签 主体做更新--star改动(枚举值:None, 0, 1)
    @parameterized.expand([[{"star_c": 0, "infoversion_c": 2}],
                           [{"star_c": 1, "infoversion_c": 2}]])
    def testCase06_handle(self, star):
        """
        状态限制
        noteId不存在，分组便签 主体新增
        """
        # 前置
        step('前置:用户A新增一条分组便签主体数据')
        path = '/v3/notesvr/set/noteinfo'
        data = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',
            'star': None,
            'remindTime': None,
            'remindType': None,
            'groupId': 'A',
        }
        res1 = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        # 操作
        step('用户A请求"上传/更新便签主体"接口')
        data["star"] = star["star_c"]
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        expect = {"responseTime": int, "infoVersion": star["infoversion_c"], "infoUpdateTime": int}
        CheckMethod().output_check(expect, res.json())

    # 状态限制: noteId已存在，分组便签 主体做更新--分组改动
    @parameterized.expand([[{"groupId_c": 0, "infoversion_c": 2}],
                           [{"groupId_c": 1, "infoversion_c": 2}]])
    def testCase07_handle(self, groupId):
        """
        状态限制
        noteId不存在，分组便签 主体新增
        """
        # 前置
        step('前置:用户A新增一条分组便签主体数据')
        path = '/v3/notesvr/set/noteinfo'
        data = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',
            'star': None,
            'remindTime': None,
            'remindType': None,
            'groupId': 'A',
        }
        res1 = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        # 操作
        step('用户A请求"上传/更新便签主体"接口')
        data["groupId"] = groupId["groupId_c"]
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        expect = {"responseTime": int, "infoVersion": groupId["infoversion_c"], "infoUpdateTime": int}
        CheckMethod().output_check(expect, res.json())

    # 状态限制: noteId已存在，首页便签 主体做更新--便签类型改动(首页——>分组)
    @parameterized.expand([[{"groupId_c": 'A', "infoversion_c": 2}],
                           [{"groupId_c": 'A', "infoversion_c": 2}]])
    def testCase08_handle(self, c):
        """
        状态限制
        noteId不存在，分组便签 主体新增
        """
        # 前置
        step('前置:用户A新增一条首页便签主体数据')
        path = '/v3/notesvr/set/noteinfo'
        data = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',
            'star': None,
            'remindTime': None,
            'remindType': None,
            'groupId': None,
        }
        res1 = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        # 操作
        step('用户A请求"上传/更新便签主体"接口')
        # data = {
        #     'noteId': data1["noteId"],
        #     'star': None,
        #     'remindTime': None,
        #     'remindType': None,
        #     'groupId': "groupId_c",
        # }
        data["groupId"] = c["groupId_c"]
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        expect = {"responseTime": int, "infoVersion": c["infoversion_c"], "infoUpdateTime": int}
        CheckMethod().output_check(expect, res.json())

    # 状态限制: noteId已存在，分组便签 主体做更新--便签类型改动(分组——>首页)
    @parameterized.expand([[{"groupId_c": None, "infoversion_c": 2}],
                           [{"groupId_c": None, "infoversion_c": 2}]])
    def testCase09_handle(self, c):
        """
        状态限制
        noteId不存在，分组便签 主体新增
        """
        # 前置
        step('前置:用户A新增一条首页便签主体数据')
        path = '/v3/notesvr/set/noteinfo'
        data = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',
            'star': None,
            'remindTime': None,
            'remindType': None,
            'groupId': 'A',
        }
        res1 = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        # 操作
        step('用户A请求"上传/更新便签主体"接口')
        # data = {
        #     'noteId': data1["noteId"],
        #     'star': None,
        #     'remindTime': None,
        #     'remindType': None,
        #     'groupId': c["groupId_c"],
        # }
        data["groupId"] = c["groupId_c"]
        res = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        expect = {"responseTime": int, "infoVersion": c["infoversion_c"], "infoUpdateTime": int}
        CheckMethod().output_check(expect, res.json())

    # 越权:
    @parameterized.expand([[{"groupId_1": None, "groupId_2": 'A', "infoversion_c": 1}],
                           [{"groupId_1": 'A', "groupId_2": None, "infoversion_c": 1}]])
    def testCas10_handle(self, groupId):
        """
        越权 (导致：操作失效)
        用户B 更新 用户A的首页便签主体
        """
        # 前置
        step('前置:用户A新增一条 首页/分组 便签主体数据')
        path = '/v3/notesvr/set/noteinfo'
        data = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',
            'star': None,
            'remindTime': None,
            'remindType': None,
            'groupId': groupId["groupId_1"],
        }
        print(self.headers)
        res1 = ApiRe().post(url=self.host + path, userId=self.userid1, wps_sid=self.wps_sid1,
                           headers=self.headers, body=data)  # json=body,body=data
        # 操作
        step('用户B请求"上传/更新便签主体"接口')
        # self.headers["Cookie"] = self.wps_sid2
        # self.headers["X-User-Key"] = self.userid2
        # print(self.headers)
        data["groupId"] = groupId["groupId_2"]
        res = ApiRe().post(url=self.host + path, userId=self.userid2, wps_sid=self.wps_sid2,
                           headers=None, body=data)  # json=body,body=data
        print(self.headers)
        expect = {"responseTime": int, "infoVersion": groupId["infoversion_c"], "infoUpdateTime": int}
        CheckMethod().output_check(expect, res.json())
