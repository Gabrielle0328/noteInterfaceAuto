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

    # 状态限制:新增一个分组,看分组valid值
    # 用户A查询用户A的新增分组
    def testCase01_major(self):
        """
        6.获取分组列表
        """
        # 前置1
        step('用户A请求接口"7.新增一个分组"')
        groupid_1 = InterfaceCall().Create_group_7(self.userid1, self.wps_sid1)
        # 操作--
        step('用户B请求接口"6.获取分组列表"')
        expect6_1 = {"userId": self.userid1, "groupId": groupid_1["groupId"],
                     "groupName": groupid_1["groupName"], "order": 0, "valid": 1,
                     "updateTime": int}
        InterfaceCall().Get_groups_6(self.userid1, self.wps_sid1, groupid_1["groupId"], expect6_1)

    # 状态限制:删除新增的一个分组，看分组valid值
    def testCase02_major(self):
        """
        6.获取分组列表
        """
        # 前置1
        step('用户A请求接口"7.新增一个分组"')
        groupid_1 = InterfaceCall().Create_group_7(self.userid1, self.wps_sid1)
        # 前置2
        step('用户A请求接口"9.删除分组"删除一个分组，使其valid=0无效')
        InterfaceCall().delete_group_9(self.userid1, self.wps_sid1, groupid_1["groupId"])
        # 操作--
        step('用户B请求接口"6.获取分组列表"')
        expect6_1 = {"userId": self.userid1, "groupId": groupid_1["groupId"],
                     "groupName": groupid_1["groupName"], "order": 0, "valid": 0,
                     "updateTime": int}
        InterfaceCall().Get_groups_6(self.userid1, self.wps_sid1, groupid_1["groupId"], expect6_1)

    # 状态限制:是否排除无效分组
    # 状态限制:排除无效分组excludeInvalid=false,显示所有分组
    def testCase03_major(self):
        """
        6.获取分组列表
        """
        # 前置1
        step('用户A请求接口"7.新增一个分组"')
        groupid_1 = InterfaceCall().Create_group_7(self.userid1, self.wps_sid1)
        groupid_2 = InterfaceCall().Create_group_7(self.userid1, self.wps_sid1)
        # 前置2
        step('用户A请求接口"9.删除分组"删除一个分组，使其valid=0无效')
        InterfaceCall().delete_group_9(self.userid1, self.wps_sid1, groupid_1["groupId"])
        # 操作--
        step('用户A请求接口"6.获取分组列表"')
        expect6_1 = {"userId": self.userid1, "groupId": groupid_1["groupId"],
                     "groupName": groupid_1["groupName"], "order": 0, "valid": 0,
                     "updateTime": int}
        InterfaceCall().Get_groups_6(self.userid1, self.wps_sid1, groupid_1["groupId"], expect6_1)
        expect6_2 = {"userId": self.userid1, "groupId": groupid_2["groupId"],
                     "groupName": groupid_2["groupName"], "order": 0, "valid": 1,
                     "updateTime": int}
        InterfaceCall().Get_groups_6(self.userid1, self.wps_sid1, groupid_2["groupId"], expect6_2)

    # 状态限制:是否排除无效分组
    # 状态限制:排除无效分组excludeInvalid=true:只显示有效的valid=1的分组>>>>>>>>>>>>>>>>>>>>>>>>>没生效
    def testCase04major(self):
        """
        6.获取分组列表
        """
        # 前置1
        step('用户A请求接口"7.新增一个分组"')
        groupid_1 = InterfaceCall().Create_group_7(self.userid1, self.wps_sid1)  # 后被删除
        # groupid_2 = InterfaceCall().Create_group_7(self.userid1, self.wps_sid1)
        # 前置2
        step('用户A请求接口"9.删除分组"删除新增的分组，使其valid=0无效')
        InterfaceCall().delete_group_9(self.userid1, self.wps_sid1, groupid_1["groupId"])
        # 操作
        step('用户A请求接口"6.获取分组列表"')
        expect6_1 = {"noteGroups": [], "requestTime": int}
        InterfaceCall().Get_groups_6(self.userid1, self.wps_sid1, groupid_1["groupId"], expect6_1, True)

    # 越权
    # 用户B查询用户A的新增分组
    def testCase05_major(self):
        """
        6.获取分组列表
        """
        # 前置1
        step('用户A请求接口"7.新增一个分组"')
        groupid_1 = InterfaceCall().Create_group_7(self.userid1, self.wps_sid1)
        # 操作--
        step('用户B请求接口"6.获取分组列表"')
        expect6_1 = {"noteGroups": [], "requestTime": int}
        InterfaceCall().Get_groups_6(self.userid2, self.wps_sid2, groupid_1["groupId"], expect6_1)

# 怎么判断没有，然后
