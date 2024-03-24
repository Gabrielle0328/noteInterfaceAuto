import json
import unittest
import requests


class TestPro(unittest.TestCase):
    def testCase01_major(self):
        """
        1.获取首页便签列表
        请求header：wps_sid，
        请求body：userId: userA，startindex: 0, rows: 50
        """
        userid = 758797333  # 同X-User-Key
        startindex = 0
        rows = 50
        host = 'http://note-api.wps.cn'
        path = f'/v3/notesvr/user/{userid}/home/startindex/{startindex}/rows/{rows}/notes'
        headers = {
            # 个人账号
            'Cookie': 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415',
            'X-User-Key': '758797333',
            # 'Content-Type': 'application/json' # POST请求时需要
        }
        # noteId_set = 'a1'
        # data = {
        #     'noteId': noteId_set,
        #     'star': '',
        #     'remindTime': '',
        #     'remindType': '',
        #     'groupId': '',
        # }
        res = requests.get(url=host + path, headers=headers)
        print(res.status_code)
        print(res.text)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        self.assertIn('responseTime', res.json().keys())  # 检查响应体
        self.assertIn('webNotes', res.json().keys())
        self.assertEqual(2, len(res.json().keys()))  # 检查响应体的字段数量
        self.assertEqual(int, type(res.json()['responseTime']))  # 检查响应体值的类型
        self.assertEqual(list, type(res.json()['webNotes']))
        print(res.json().keys())
        # print(res.json()["webNotes"])
        # return res.json().webNotes
        return res.json()["webNotes"]

    def testCase02_major(self):
        """
        2.上传/更新便签主体
        请求header：wps-id=user-A、X-user-key=userid-A
        请求body：noteId=a1， star=不填默认为0，'remindTime': '','remindType': '',groupId=
        """
        host = 'http://note-api.wps.cn'
        path = '/v3/notesvr/set/noteinfo'
        headers = {
            # 个人账号
            'Cookie': 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415',
            'X-User-Key': '758797333',
            'Content-Type': 'application/json'
        }
        noteId_set = 'a1'
        data = {
            'noteId': noteId_set,
            'star': '',
            'remindTime': '',
            'remindType': '',
            'groupId': '',
        }
        res = requests.post(url=host + path, headers=headers, json=data)
        print(res.status_code)
        print(res.text)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        self.assertIn('responseTime', res.json().keys())  # 检查响应体
        self.assertIn('infoVersion', res.json().keys())
        self.assertIn('infoUpdateTime', res.json().keys())
        self.assertEqual(3, len(res.json().keys()))  # 检查响应体的字段数量
        self.assertEqual(int, type(res.json()['responseTime']))  # 检查响应体值的类型
        self.assertEqual(int, type(res.json()['infoUpdateTime']))
        print(res.json().keys())
        return res.json()["infoVersion"]

    def testCase03_major(self):
        """
            3.新增便签内容
            请求header：wps-id=user-A、X-user-key=userid-A
            请求body：noteId=a1, 'title': '123','summary': '1234','body': '123456',
                    'localContentVersion': '','BodyType': 0
        """
        host = 'http://note-api.wps.cn'
        path = '/v3/notesvr/set/notecontent'
        headers = {
            # 个人账号
            'Cookie': 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415',
            'X-User-Key': '758797333',
            'Content-Type': 'application/json'
        }
        noteId_set = 'a1'
        data = {
            'noteId': noteId_set,
            'title': '123',
            'summary': '1234',
            'body': '123456',
            'localContentVersion': 37,
            'BodyType': 0
        }
        res = requests.post(url=host + path, headers=headers, json=data)
        print(res.status_code)
        print(res.text)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        self.assertIn('responseTime', res.json().keys())  # 检查响应体是否存在
        self.assertIn('contentVersion', res.json().keys())
        self.assertIn('contentUpdateTime', res.json().keys())
        self.assertEqual(3, len(res.json().keys()))  # 检查响应体的字段数量
        self.assertEqual(int, type(res.json()['responseTime']))  # 检查响应体值的类型
        self.assertEqual(int, type(res.json()['contentVersion']))
        self.assertEqual(int, type(res.json()['contentUpdateTime']))
        # 调用接口“4.获取便签内容”查看返回体对齐内容
        # # 检查改动的title、summary、body、localContentVersion、BodyType
        res4 = self.testCase04_major().json()
        print(res4)
        for i in res4["noteBodies"]:
            print(data["title"])
            print(i["title"])
            if i["noteId"] == data["noteId"]:
                self.assertEqual(data["title"], i["title"], msg='wrong title')  # 检查title
                self.assertEqual(data["summary"], i["summary"], msg='wrong summary')  # 检查summary
                self.assertEqual(data["body"], i["body"], msg='wrong body')  # 检查body
                self.assertEqual(data["BodyType"], i["bodyType"], msg='wrong body')  # 检查BodyType
                self.assertEqual(data["localContentVersion"] + 1, i["contentVersion"], msg='wrong body')
                self.assertEqual(i["contentVersion"], res.json()['contentVersion'], msg='wrong body')
                # 检查localContentVersion

    def testCase04_major(self, noteId_set=['a3']):
        """
            4.获取便签内容
            填入：请求header：wps-id= ， X-user-key= ，
                请求body：noteId=a1，
        """
        host = 'http://note-api.wps.cn'
        path = '/v3/notesvr/get/notebody'
        headers = {
            # 个人账号
            'Cookie': 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415',
            'X-User-Key': '758797333',
            # 'Content-Type': 'application/json'
        }
        # noteId_set = ['a1']
        data = {
            'noteIds': noteId_set,
        }
        res = requests.post(url=host + path, headers=headers, json=data)
        print(res.status_code)
        print(res.text)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        self.assertIn('responseTime', res.json().keys())  # 检查响应体是否存在
        self.assertIn('noteBodies', res.json().keys())
        self.assertEqual(2, len(res.json().keys()))  # 检查响应体的字段数量
        self.assertEqual(int, type(res.json()['responseTime']))  # 检查响应体值的类型
        self.assertEqual(list, type(res.json()['noteBodies']))
        return res

    def testCase05_major(self):
        """
            4.删除便签内容
            填入：请求header：wps-id= ， X-user-key= ，
                请求body：noteId=a1，
        """
        host = 'http://note-api.wps.cn'
        path = '/v3/notesvr/delete'
        headers = {
            # 个人账号
            'Cookie': 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415',
            'X-User-Key': '758797333',
            'Content-Type': 'application/json'
        }
        noteId_set = 'a3'
        data = {
            'noteId': noteId_set,
        }
        res = requests.post(url=host + path, headers=headers, json=data)
        print(res.status_code)
        print(res.text)
        # 检查返回体responseTime
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        self.assertIn('responseTime', res.json().keys())  # 检查响应体是否存在
        self.assertEqual(1, len(res.json().keys()))  # 检查响应体的字段数量
        self.assertEqual(int, type(res.json()['responseTime']))  # 检查响应体值的类型
        # 调用接口“4.获取便签内容(可以获得所有类型的标签)”查看返回体对齐内容
        # # 检查删除有效性: 被删除的noteId是否还存在(存在，且valid为0，在回收箱)
        res4 = self.testCase04_major(noteId_set=["a1", "a2", "a3"]).json()
        print(res4)
        check = False
        print(check)
        for i in res4["noteBodies"]:
            if i["noteId"] == data["noteId"] and i["valid"] == 0:  # 检查被删除标签的可查询性和valid值
                check = True
        self.assertEqual(True, check)
        # 如果是首页标签，删除后不能在接口“1.获取首页标签列表“查到
        # code
        # 如果是分组列表

    def testCase06_major(self):
        """
        6.获取分组列表
        请求header：wps_sid，
        请求body：excludeInvalid=
        """
        host = 'http://note-api.wps.cn'
        path = '/v3/notesvr/get/notegroup'
        headers = {
            # 个人账号
            'Cookie': 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415',
            'X-User-Key': '758797333',
            'Content-Type': 'application/json'  # POST请求时需要
        }
        data = {
            'excludeInvalid': '',
        }
        res = requests.post(url=host + path, headers=headers, json=data)
        print(res.status_code)
        print(res.text)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        self.assertIn('requestTime', res.json().keys())  # 检查响应体
        self.assertIn('noteGroups', res.json().keys())
        self.assertEqual(2, len(res.json().keys()))  # 检查响应体的字段数量
        self.assertEqual(int, type(res.json()['requestTime']))  # 检查响应体值的类型
        self.assertEqual(list, type(res.json()['noteGroups']))
        print(res.json().keys())
        # print(res.json()["webNotes"])
        # return res.json().webNotes
        return res

    def testCase07_major(self, groupId_set='A2', groupName_set='group-A2', order_set=0):
        """
        7.新增分组
        请求header：wps-id=user-A、X-user-key=userid-A
        请求body：groupId= , groupName= ， order= ，
        """
        host = 'http://note-api.wps.cn'
        path = '/v3/notesvr/set/notegroup'
        headers = {
            # 个人账号
            'Cookie': 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415',
            'X-User-Key': '758797333',
            'Content-Type': 'application/json'
        }
        # groupId_set = 'A1'
        # groupName_set = 'group-A1'
        # order_set = ''
        data = {
            'groupId': groupId_set,
            'groupName': groupName_set,
            'order': order_set,
        }
        res = requests.post(url=host + path, headers=headers, json=data)
        # print(res.status_code)
        # print(res.text)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        self.assertIn('responseTime', res.json().keys())  # 检查响应体
        self.assertIn('updateTime', res.json().keys())
        self.assertEqual(2, len(res.json().keys()))  # 检查响应体的字段数量
        self.assertEqual(int, type(res.json()['responseTime']))  # 检查响应体值的类型
        self.assertEqual(int, type(res.json()['updateTime']))
        # print(res.json().keys())
        # 调用接口“6.获取分组列表”查看返回体对齐内容
        # 检查添加分组有效性,userId,groupId,groupName,order,valid,
        res6 = self.testCase06_major().json()
        for i in res6["noteGroups"]:
            if i["groupId"] == data["groupId"]:
                print(f'输入期望值：{data["order"]}')
                print(f'实际查询值{i["order"]}')
                self.assertEqual(data["groupName"], i["groupName"], msg='wrong groupName')  # 检查groupName
                self.assertEqual(data["order"], i["order"], msg='wrong order')  # 检查order

    def testCase08_major(self, groupId_set='-', startIndex_set='', rows_set=''):
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
            # 'groupId': '!!!',
            # 'startIndex': 0,
            # 'rows': 50,
        }
        res = requests.post(url=host + path, headers=headers, json=data)
        print(res.status_code)
        print(res.text)
        # print(groupId_set)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        self.assertIn('responseTime', res.json().keys())  # 检查响应体
        self.assertIn('webNotes', res.json().keys())
        self.assertEqual(2, len(res.json().keys()))  # 检查响应体的字段数量
        self.assertEqual(int, type(res.json()['responseTime']))  # 检查响应体值的类型
        self.assertEqual(list, type(res.json()['webNotes']))
        # print(res.json().keys())
        # print(res.json()["webNotes"])
        # return res.json().webNotes
        return res.status_code, res.json()

    def testCase09_major(self, groupId_set='-', startIndex_set='', rows_set=''):
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
            'groupId': groupId_set,
            'startIndex': startIndex_set,
            'rows': rows_set,
        }
        res = requests.post(url=host + path, headers=headers, json=data)
        # print(res.status_code)
        # print(res.text)
        self.assertEqual(200, res.status_code, msg='状态码异常，期望的状态XXX')  # 检查状态码
        self.assertIn('responseTime', res.json().keys())  # 检查响应体
        self.assertEqual(1, len(res.json().keys()))  # 检查响应体的字段数量
        self.assertEqual(int, type(res.json()['responseTime']))  # 检查响应体值的类型
        return res, res.status_code, res.json()

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


print(TestPro().testCase09_major())
