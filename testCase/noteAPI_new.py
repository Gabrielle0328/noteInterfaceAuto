import json
import unittest
import requests
from common.checkMethods import CheckMethod
from businessCommon.createNote import Create
from businessCommon.clearNote import Clear
from businessCommon.inquireNote import Inqiure
import time
# from copy import deepcopy  # expect用作常量，被调用时可以用
from common.logCreate import info, step, error  # 日志相关
from common.yamlRead import YamlRead  # 读取Yaml文件:环境切换、配置等


class TestPro(unittest.TestCase):
    host = 'http://note-api.wps.cn'
    userid = '758797333'  # 同X-User-Key
    wps_sid = 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415'
    content_type = 'application/json'  # POST请求时需要
    headers = {
        # 个人账号
        'Cookie': wps_sid,
        'X-User-Key': userid,
        'Content-Type': content_type  # POST请求时需要
    }

    # 初始化
    def setUp(self) -> None:
        Clear().note_clear(self.userid, self.wps_sid)

    # 1.获取首页便签列表
    def testCase01_major(self):
        """
        1.获取首页便签列表
        请求header：wps_sid，
        请求body：userId: userA，startindex: 0, rows: 50
        """
        # 前置--新建一条便签的主体和内容
        res_create = Create().note_create(self.userid, self.wps_sid, 1)

        # 本接口操作
        startindex = 0
        rows = 50
        path = f'/v3/notesvr/user/{self.userid}/home/startindex/{startindex}/rows/{rows}/notes'

        res = requests.get(url=self.host + path, headers=self.headers)
        print(res.status_code)
        print(res.text)
        # self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        # self.assertIn('responseTime', res.json().keys())  # 检查响应体
        # self.assertIn('webNotes', res.json().keys())
        # self.assertEqual(2, len(res.json().keys()))  # 检查响应体的字段数量
        # self.assertEqual(int, type(res.json()['responseTime']))  # 检查响应体值的类型
        # self.assertEqual(list, type(res.json()['webNotes']))
        # print(res.json().keys())
        # print(res.json()["webNotes"])
        # return res.json().webNotes
        expect = {"responseTime": int, "webNotes": [
            {"noteId": res_create[0]["noteId"], "createTime": int, "star": 0, "remindTime": 0,
             "remindType": 0, "infoVersion": 1, "infoUpdateTime": int, "groupId": None,
             "title": res_create[0]["title"], "summary": res_create[0]["summary"], "thumbnail": None,
             "contentVersion": res_create[0]["localContentVersion"], "contentUpdateTime": int}]}
        CheckMethod().output_check(expect, res.json())
        return res.json()

    # 2.上传/更新便签主体
    def testCase02_major(self, noteId_set=f'{str(int(time.time() * 1000))}_noteId',
                         star_set=None, remindTime_set=None,
                         remindType_set=None, groupId_set=''):
        """
        2.上传/更新便签主体
        请求header：wps-id=user-A、X-user-key=userid-A
        请求body：noteId=a1， star=不填默认为0，'remindTime': '','remindType': '',groupId=
        """
        path = '/v3/notesvr/set/noteinfo'
        data = {
            'noteId': noteId_set,
            'star': star_set,
            'remindTime': remindTime_set,
            'remindType': remindType_set,
            'groupId': groupId_set,
        }
        res = requests.post(url=self.host + path, headers=self.headers, json=data)
        print(res.status_code)
        print(res.text)
        # self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        # self.assertIn('responseTime', res.json().keys())  # 检查响应体
        # self.assertIn('infoVersion', res.json().keys())
        # self.assertIn('infoUpdateTime', res.json().keys())
        # self.assertEqual(3, len(res.json().keys()))  # 检查响应体的字段数量
        # self.assertEqual(int, type(res.json()['responseTime']))  # 检查响应体值的类型
        # self.assertEqual(int, type(res.json()['infoUpdateTime']))
        # print(res.json().keys())
        expect = {"responseTime": int, "infoVersion": 1, "infoUpdateTime": int}
        CheckMethod().output_check(expect, res.json())
        return res.status_code, res.json()

    # 3.新增便签内容
    def testCase03_major(self, noteId_set='111',
                         title_set='123', summary_set='12345', body_set='123455678',
                         localContentVersion_set=10, BodyType_set=0):
        """
            3.新增便签内容
            请求header：wps-id=user-A、X-user-key=userid-A
            请求body：noteId=a1, 'title': '123','summary': '1234','body': '123456',
                    'localContentVersion': '','BodyType': 0        --全必填
        """
        path = '/v3/notesvr/set/notecontent'

        # 前置--新建便签主体
        noteId_set = f'{str(int(time.time() * 1000))}_noteId'
        info_body = {
            'noteId': noteId_set,  # 只是创建普哦那个便签，其他optional不填
        }
        res_body_create = requests.post(f'{self.host}/v3/notesvr/set/noteinfo', headers=headers, json=info_body)
        infoVersion = res_body_create.json()["infoVersion"]

        # 本接口操作
        data = {
            'noteId': noteId_set,
            'title': title_set,
            'summary': summary_set,
            'body': body_set,
            'localContentVersion': localContentVersion_set,
            'BodyType': BodyType_set
        }
        res = requests.post(url=self.host + path, headers=self.headers, json=data)
        print(res.status_code)
        print(res.text)
        # self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        # self.assertIn('responseTime', res.json().keys())  # 检查响应体是否存在
        # self.assertIn('contentVersion', res.json().keys())
        # self.assertIn('contentUpdateTime', res.json().keys())
        # self.assertEqual(3, len(res.json().keys()))  # 检查响应体的字段数量
        # self.assertEqual(int, type(res.json()['responseTime']))  # 检查响应体值的类型
        # self.assertEqual(int, type(res.json()['contentVersion']))
        # self.assertEqual(int, type(res.json()['contentUpdateTime']))
        expect = {"responseTime": int, "contentVersion": infoVersion, "contentUpdateTime": int}
        CheckMethod().output_check(expect, res.json())
        return res.status_code, res.json()

        # 调用接口“4.获取便签内容”查看返回体对齐内容
        # # 检查改动的title、summary、body、localContentVersion、BodyType
        # res4 = self.testCase04_major().json()
        # print(res4)
        # for i in res4["noteBodies"]:
        #     print(data["title"])
        #     print(i["title"])
        #     if i["noteId"] == data["noteId"]:
        #         self.assertEqual(data["title"], i["title"], msg='wrong title')  # 检查title
        #         self.assertEqual(data["summary"], i["summary"], msg='wrong summary')  # 检查summary
        #         self.assertEqual(data["body"], i["body"], msg='wrong body')  # 检查body
        #         self.assertEqual(data["BodyType"], i["bodyType"], msg='wrong body')  # 检查BodyType
        #         self.assertEqual(data["localContentVersion"] + 1, i["contentVersion"], msg='wrong body')
        #         self.assertEqual(i["contentVersion"], res.json()['contentVersion'], msg='wrong body')
        #         # 检查localContentVersion

    # 4.获取便签内容
    def testCase04_major(self):
        """
            4.获取便签内容
            填入：请求header：wps-id= ， X-user-key= ，
                请求body：noteId=a1，
        """
        path = '/v3/notesvr/get/notebody'

        # 前置--新建便签主体和内容
        res_create = Create().note_create(self.userid, self.wps_sid, 1)

        # 本接口操作
        noteId_set = res_create[0]["noteId"]
        data = {
            'noteIds': [noteId_set],
        }
        res = requests.post(url=self.host + path, headers=self.headers, json=data)
        print(res.status_code)
        print(res.text)
        # 检查状态码
        self.assertEqual(200, res.status_code, msg='状态码异常')  # 检查状态码
        # 检查返回body
        expect = {"responseTime": int, "noteBodies": [{"summary": res_create[0]["summary"],
        "noteId": res_create[0]["noteId"], "infoNoteId": res_create[0]["noteId"], "bodyType": 0,
        "body": res_create[0]["body"], "contentVersion": res_create[0]["localContentVersion"],
        "contentUpdateTime": int, "title": res_create[0]["title"], "valid": 1}]}
        CheckMethod().output_check(expect, res.json())
        return res

    # 5.删除便签 软删除
    def testCase05_major(self):
        """
            5.删除便签内容
            填入：请求header：wps-id= ， X-user-key= ，
                请求body：noteId=a1，
        """
        path = '/v3/notesvr/delete'
        headers = {
            # 个人账号
            'Cookie': self.wps_sid,
            'X-User-Key': self.userid,
            'Content-Type': self.content_type  # POST请求时需要
        }

        # 前置--先 新建便签主体和内容
        res_create = Create().note_create(self.userid, self.wps_sid, 1)

        noteId_set = res_create[0]["noteId"]
        print(noteId_set)
        data = {
            'noteId': noteId_set,
        }
        res = requests.post(url=self.host + path, headers=headers, json=data)
        print(res.status_code)
        print(res.text)
        # 检查状态码
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')
        # 检查返回body
        expect = {"responseTime": int}
        CheckMethod().output_check(expect, res.json())  # 检查返回体responseTime

        # 调用接口“4.获取便签内容(看valid值)”查看返回体对齐内容
        # # 检查删除有效性: 被删除的noteId是否还存在(存在，且valid为0，在回收箱)
        data_4 = {
            'noteIds': [noteId_set],
        }
        res4 = requests.post(url=self.host + '/v3/notesvr/get/notebody', headers=headers, json=data_4)
        # res4 = self.testCase04_major(noteId_set=["a3"])
        print(res4.json())
        expect_res4 = {"responseTime": int, "noteBodies": [{"summary": res_create[0]["summary"],
                                                            "noteId": res_create[0]["noteId"],
                                                            "infoNoteId": res_create[0]["noteId"], "bodyType": 0,
                                                            "body": res_create[0]["body"],
                                                            "contentVersion": res_create[0]["localContentVersion"],
                                                            "contentUpdateTime": int, "title": res_create[0]["title"],
                                                            "valid": 0}]}
        CheckMethod().output_check(expect_res4, res4.json())
        # res4 = self.testCase04_major(noteId_set=["a3"]).json()
        # print(res4)
        # check = False
        # print(check)
        # for i in res4["noteBodies"]:
        #     if i["noteId"] == data["noteId"] and i["valid"] == 0:  # 检查被删除标签的可查询性和valid值
        #         check = True
        # self.assertEqual(True, check)

        # 如果是首页标签，删除后不能在接口“1.获取首页标签列表“查到
        # 调用接口“1.获取首页标签”查看返回体对齐内容
        res_1 = requests.get(url=self.host
        + f'/v3/notesvr/user/{self.userid}/home/startindex/0/rows/999/notes', headers=headers)
        expect_res_1 = {"responseTime": int, "webNotes": []}
        CheckMethod().output_check(expect_res_1, res_1.json())
        # code
        # 如果是分组列表

    # 6.获取分组列表
    def testCase06_major(self, excludeInvalid_set=None):
        """
        6.获取分组列表
        请求header：wps_sid，
        请求body：excludeInvalid=
        """
        # 前置--新增分组
        groupId_set = f'{str(int(time.time() * 1000))}_groupId'
        groupName_set = f'<{groupId_set}>'
        print(groupName_set)
        order_set = 0
        group_list = []
        body_group = {
            'groupId': groupId_set,
            'groupName': groupName_set,
            'order': order_set,
        }
        group_list.append(body_group)
        print(group_list)
        res_group = requests.post(url=self.host + '/v3/notesvr/set/notegroup',
                            headers=self.headers, json=body_group)

        # 本接口操作
        path = '/v3/notesvr/get/notegroup'
        data = {
            'excludeInvalid': excludeInvalid_set,
        }
        res = requests.post(url=self.host + path, headers=self.headers, json=data)
        print(res.status_code)
        print(res.text)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        # self.assertIn('requestTime', res.json().keys())  # 检查响应体
        # self.assertIn('noteGroups', res.json().keys())
        # self.assertEqual(2, len(res.json().keys()))  # 检查响应体的字段数量
        # self.assertEqual(int, type(res.json()['requestTime']))  # 检查响应体值的类型
        # self.assertEqual(list, type(res.json()['noteGroups']))
        expect = {"requestTime": int,
                  "noteGroups": [{"userId": self.userid, "groupId": group_list[0]["groupId"],
                                  "groupName": group_list[0]["groupName"], "order": 0,
                                  "valid": 1, "updateTime": int}]}
        CheckMethod().output_check2(expect, res.json())
        print(res.json().keys())
        # print(res.json()["webNotes"])
        # return res.json().webNotes
        return res

    # 7.新增分组
    def testCase07_major(self, groupId_set='A2', groupName_set='group-A2', order_set=0):
        """
        7.新增分组
        请求header：wps-id=user-A、X-user-key=userid-A
        请求body：groupId= , groupName= ， order= ，
        """
        path = '/v3/notesvr/set/notegroup'
        groupId_set = f'{str(int(time.time() * 1000))}_groupId'
        groupName_set = f'<{groupId_set}>'
        print(groupName_set)
        order_set = 0
        body_group = {
            'groupId': groupId_set,
            'groupName': groupName_set,
            'order': order_set,
        }
        res = requests.post(url=self.host + path, headers=self.headers, json=data)
        # print(res.status_code)
        # print(res.text)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        expect = {"responseTime": int, "updateTime": int}
        CheckMethod().output_check2(expect, res.json())  # 检查状返回码

        # 调用接口“6.获取分组列表”查看返回体对齐内容
        # 检查添加分组有效性,userId,groupId,groupName,order,valid,
        res6 = self.testCase06_major().json()
        for i in res6["noteGroups"]:
            if i["groupId"] == data["groupId"]:
                print(f'输入期望值：{data["order"]}')
                print(f'实际查询值{i["order"]}')
                self.assertEqual(data["groupName"], i["groupName"], msg='wrong groupName')  # 检查groupName
                self.assertEqual(data["order"], i["order"], msg='wrong order')  # 检查order

    # 8.查看分组下便签
    def testCase08_major(self, groupId_set='A1', startIndex_set='', rows_set=''):
        """
        8.查看分组下便签
        请求header：wps_sid，
        请求body：groupId(必填),
                startIndex,rows(非必填)
        """
        host = 'http://note-api.wps.cn'
        path = '/v3/notesvr/web/getnotes/group'
        headers = {
            # 个人账号
            'Cookie': 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415',
            'X-User-Key': '758797333',
            'Content-Type': 'application/json'  # POST请求时需要
        }
        data = {
            'groupId': groupId_set,
            'startIndex': startIndex_set,
            'rows': rows_set,
        }
        res = requests.post(url=host + path, headers=headers, json=data)
        print(res.status_code)
        print(res.text)
        # print(groupId_set)
        # self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        # self.assertIn('responseTime', res.json().keys())  # 检查响应体
        # self.assertIn('webNotes', res.json().keys())
        # self.assertEqual(2, len(res.json().keys()))  # 检查响应体的字段数量
        # self.assertEqual(int, type(res.json()['responseTime']))  # 检查响应体值的类型
        # self.assertEqual(list, type(res.json()['webNotes']))
        # print(res.json().keys())
        # print(res.json()["webNotes"])
        # return res.json().webNotes
        expect = {"responseTime": int, "webNotes": list}
        CheckMethod().output_check2(expect, res.json())
        return res, res.status_code, res.json()

    # 9.删除分组
    def testCase09_major(self, groupId_set='A1'):
        """
        9.删除分组
        请求header：wps_sid，
        请求body：groupId(必填)
        """
        host = 'http://note-api.wps.cn'
        path = '/notesvr/delete/notegroup'
        headers = {
            # 个人账号
            'Cookie': 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415',
            'X-User-Key': '758797333',
            'Content-Type': 'application/json'  # POST请求时需要
        }
        data = {
            'groupId': groupId_set
        }
        res = requests.post(url=host + path, headers=headers, json=data)
        print(res.status_code)
        print(res.text)
        # self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        # self.assertIn('responseTime', res.json().keys())  # 检查响应体
        # self.assertEqual(1, len(res.json().keys()))  # 检查响应体的字段数量
        # self.assertEqual(int, type(res.json()['responseTime']))  # 检查响应体值的类型
        expect = {"responseTime": int}
        CheckMethod().output_check(expect, res.json())
        return res

    def testCase10_major(self, remindStartTime_set='-', remindEndTime_set='-',
                         startIndex_set='-', rows_set='-'):
        """
        10.查看日历下便签 *
        请求header：wps_sid，
        请求body：remindStartTime, remindEndTime, startIndex, rows--(必填)
        """
        host = 'http://note-api.wps.cn'
        path = '/v3/notesvr/web/getnotes/remind'
        headers = {
            # 个人账号
            'Cookie': 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415',
            'X-User-Key': '758797333',
            'Content-Type': 'application/json'  # POST请求时需要
        }
        data = {
            'remindStartTime': remindStartTime_set,
            'remindEndTime': remindEndTime_set,
            'startIndex': startIndex_set,
            'rows': rows_set,
        }
        res = requests.post(url=host + path, headers=headers, json=data)
        # print(res.status_code)
        # print(res.text)
        expect = {'responseTime': int, "webNotes": [
            {"noteId": str, "createTime": int, "star": 0, "remindTime": 0,
             "remindType": 0, "infoVersion": 1, "infoUpdateTime": int, "groupId": None,
             "title": "75u8dlZyTLqWCm/b2PLNlg==", "summary": "pIDnRrCwq8sUW3gyWpo7iw==", "thumbnail": None,
             "contentVersion": 3, "contentUpdateTime": int}]}
        CheckMethod().output_check(expect, res.json())
        return res.status_code, res.json()

    # 11.查看回收站下便签列表 *
    def testCase11_major(self, startIndex_set=0, rows_set=1):
        """
        11.查看回收站下便签列表 *
        请求header：wps_sid，
        请求body：userid, startIndex, rows--(必填)
        """
        # 前置1--新建便签主体和内容
        res_create = Create().note_create(self.userid, self.wps_sid, 1)
        # 前置2--删除便签(到回收站)
        body_delete = {
            "noteId": res_create[0]["noteId"]  # 接口要求传入的请求body
        }
        res_delete = requests.post(f'{self.host}/v3/notesvr/delete',
                                   headers=self.headers, json=body_delete)

        # 本接口操作
        path = f'/v3/notesvr/user/{self.userid}/invalid/startindex/{startIndex_set}/rows/{rows_set}/notes'
        data = {
            'userid': self.userid,
            'startIndex': startIndex_set,
            'rows': rows_set,
        }
        res = requests.get(url=self.host + path, headers=self.headers, json=data)
        # print(res.status_code)
        # print(res.text)
        expect = {'responseTime': int,
                  "webNotes": [{"noteId": res_create[0]["noteId"], "createTime": int, "star": 0,
                                "remindTime": 0, "remindType": 0, "infoVersion": 2,
                                "infoUpdateTime": int, "groupId": None,
                                "title": res_create[0]["title"], "summary": res_create[0]["summary"], "thumbnail": None,
                                "contentVersion": 1, "contentUpdateTime": int}]}
        CheckMethod().output_check(expect, res.json())
        # return res_create[0]["noteId"]
        return res

    # 12.恢复回收站的便签 *
    def testCase12_major(self):
        """
        12.恢复回收站的便签 *
        请求header：wps_sid，
        请求body：userid, noteIds--(必填)
        """
        # 前置--新建标签主体和内容后，删除标签
        res11 = self.testCase11_major()
        noteId_set = res11.json()
        # print(noteIds_set)

        # 本接口操作
        path = f'/v3/notesvr/user/{self.userid}/notes'
        data_recycle = {
            'userId': self.userid,
            'noteIds': [noteId_set["webNotes"][0]["noteId"]],
        }
        res = requests.patch(url=self.host + path, headers=self.headers, json=data_recycle)
        # print(res.status_code)
        # print(res.text)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码

        # 查看数据源
        res_inquire = Inqiure().note_inquire()
        expect = {'responseTime': int, "webNotes": [
            {"noteId": str, "createTime": int, "star": 0, "remindTime": 0, "remindType": 0,
             "infoVersion": 3, "infoUpdateTime": int, "groupId": None,
             "title": noteId_set["webNotes"][0]["title"],
             "summary": noteId_set["webNotes"][0]["summary"], "thumbnail": None,
             "contentVersion": noteId_set["webNotes"][0]["contentVersion"],
             "contentUpdateTime": int}]}
        CheckMethod().output_check(expect, res_inquire.json())
        # return  # 无响应body
        # 调用接口1.获取首页便签列表，校验是否恢复成功(我恢复的，就是我删除的)
        # res1_note_get = self.testCase01_major()
        # expect = {"responseTime": int, "webNotes": [
        #     {"noteId": noteIds_set["webNotes"][0]["noteId"], "createTime": int, "star": 0,
        #      "remindTime": 0, "remindType": 0, "infoVersion": 3, "infoUpdateTime": int,
        #      "groupId": None, "title": noteIds_set["webNotes"][0]["title"],
        #      "summary": noteIds_set["webNotes"][0]["summary"], "thumbnail": None,
        #      "contentVersion": noteIds_set["webNotes"][0]["localContentVersion"],
        #      "contentUpdateTime": int}]}
        #     # res_create是前置创造的便签
        # CheckMethod().output_check2(expect, res1_note_get)

    # 13.删除/清空回收站便签 *
    def testCase13_major(self, noteIds_set=["----"]):
        """
        13.删除/清空回收站便签 *
        请求header：wps_sid，
        请求body：noteIds--(必填)
        """
        # 前置--新增/删除到回收站/清除回收站


        path = '/v3/notesvr/cleanrecyclebin'
        data = {
            'noteIds': noteIds_set,
        }
        res = requests.post(url=self.host + path, headers=self.headers, json=data)
        print(res.status_code)
        print(res.text)
        expect = {'responseTime': int}
        CheckMethod().output_check(expect, res.json())
        return res.status_code, res.json()

    def testCase0x_input(self):
        """新增分组groupId字段缺失"""
        host = 'http://note-api.wps.cn'
        path = '/v3/notesvr/set/notegroup'
        headers = {
            'Cookie': 'wps_sid=V02SG3oIwfZGY3-EWrNqRBP1J1oAr6E00ab36a440036f58bfd',
            'X-User-Key': '922061821',
            'Content-Type': 'application/json'
        }
        groupId = '111111'
        data = {
            'groupId': groupId,
            'groupName': '旅游笔记',
            'order': 0
        }
        data.pop('groupId')
        res = requests.post(url=host + path, headers=headers, json=data)
        print(res.status_code)
        print(res.text)
        assert res.status_code == 500

# print(TestPro().testCase08_major(groupId_set='A1'))
# print(TestPro().testCase08_major(groupId_set='A1'))
# print(TestPro().testCase03_major(noteId_set='111', title_set='123', summary_set='12345', body_set='123455678', localContentVersion_set=9, BodyType_set=0))
