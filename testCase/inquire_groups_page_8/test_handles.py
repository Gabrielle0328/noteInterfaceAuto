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
class InquireGroupsHandle(unittest.TestCase):
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

    # 状态限制:新建日历便签5条
    # startIndex起始索引:0，row=2
    def testCase01_major(self):
        """
        8.查看分组下便签
        """
        # 前置1
        step('用户A请求接口"7.新增分组"')
        res7 = InterfaceCall().Create_group_7(self.userid1, self.wps_sid1)
        print(res7["groupId"])
        g_n = []  # 存放某组的noteid
        g_n_c = []  # 存放某组的notei的content
        n = 3  # 新增n条便签的主体和内容
        for i in range(n):
            # 前置2
            step('用户A请求接口"2新增分组便签主体"')
            noteid_body = InterfaceCall().create_note_body_2(self.userid1, self.wps_sid1, groupId=res7["groupId"])
            # 前置3
            step('用户A请求接口"3.新增分组便签内容"')
            noteid_content = InterfaceCall().create_note_content_3(self.userid1, self.wps_sid1, noteid_body["noteId"])
            g_n.append(noteid_body["noteId"])
            g_n_c.append(noteid_content)
        print(g_n)
        print(len(g_n_c), g_n_c)
        print(g_n_c[n::-1])
        # 操作
        rows = 2
        for ii in range(rows):
            print('***************************************************************************')
            print(ii)
            step('用户A请求接口"8.查看分组下便签"')
            expect8 = {"noteId": g_n_c[n:-(rows+2):-1][ii]["noteId"], "createTime": int, "star": 0,
                       "remindTime": 0, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
                       "groupId": res7["groupId"], "title": g_n_c[n:-(rows+2):-1][ii]["title"],
                       "summary": g_n_c[n:-(rows+2):-1][ii]["summary"], "thumbnail": None,
                       "contentVersion": 1, "contentUpdateTime": int}
            InterfaceCall().group_note_get_8(self.userid1, self.wps_sid1, expect8,
                                             g_n_c[n::-1][ii]["noteId"], res7["groupId"],
                                             rows=rows)



