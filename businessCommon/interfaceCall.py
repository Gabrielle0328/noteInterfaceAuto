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


class InterfaceCall:
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

    def normal_note_get_1(self, userid, wps_sid, startindex, rows, content_data, expect1):
        path1 = f'/v3/notesvr/user/{userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res1 = ApiRe().get(url=self.host + path1, wps_sid=wps_sid)  # json=body,body=data
        # expect1 = {"noteId": noteid, "createTime": int, "star": 0, "remindTime": 0, "remindType": 0,
        #            "infoVersion": 1, "infoUpdateTime": int, "groupId": None, "title": "test",
        #            "summary": "test", "thumbnail": None, "contentVersion": 1,
        #            "contentUpdateTime": int}
        time1 = 0
        for i in res1.json()["webNotes"]:
            if i["noteId"] == content_data["noteId"]:
                CheckMethod().output_check(expect1, i)
                time4 = time1 + 1
        print(time1)
        if time1 != 1:
            if time1 >= 1:
                print("存在重复数据")
            else:
                print("不存在该条数据")
        else:
            print("存在且仅存在一条该便签")
        return time1, res1

    def normal_note_get_4(self, userId, wps_sid, cb_res, content_data, expect4):
        '''
        调用接口“4.获取便签内容”查看返回体对齐内容
        :param expect4:
        :param cb_res: 传入新增便签主体的noteId
        :param content_data: 传入新增便签内容的data
        :return:
        '''
        path4 = '/v3/notesvr/get/notebody'
        data4 = {
            'noteIds': [cb_res],
        }
        res4 = ApiRe().post(url=self.host + path4, userId=userId, wps_sid=wps_sid,
                            body=data4)  # json=body,body=data
        # expect4 = {"summary": content_data["summary"], "noteId": content_data["noteId"],
        #            "infoNoteId": content_data["noteId"], "bodyType": 0, "body": content_data["body"],
        #            "contentVersion": 1, "contentUpdateTime": int, "title": content_data["title"],
        #            "valid": 1}
        time4 = 0
        if res4.json()["noteBodies"] != []:
            for i in res4.json()["noteBodies"]:
                print(i)
                if i["noteId"] == content_data["noteId"]:
                    CheckMethod().output_check(expect4, i)
                    time4 = time4 + 1
            print(time4)
            if time4 != 1:
                if time4 >= 1:
                    print("存在重复数据")
                else:
                    print("不存在该条数据")
            else:
                print("存在且仅存在一条该便签")
        else:
            CheckMethod().output_check(expect4, res4.json())
            print("请求接口'4.获取便签内容'的返回结果包含的便签数量为0，即不存在任何便签数据！！！")
        return time4, res4

    def calendar_note_get_10(self, userId, wps_sid, remindTime, content_data, expect10):
        '''
        调用接口“10.查看日历下便签”查看返回体对齐内容  2024-01~2024-03
        :param expect10:
        :param remindTime: 传入新增的日历便签主体的时间戳
        :param content_data: 传入新增的日历便签内容的data
        :return:
        '''
        path10 = '/v3/notesvr/web/getnotes/remind'
        data10 = {
            "remindStartTime": 1703952000, "remindEndTime": 1709136000, "startIndex": 0, "rows": 999
        }
        res10 = ApiRe().post(url=self.host + path10, userId=userId, wps_sid=wps_sid,
                             body=data10)  # json=body,body=data
        # res10 = requests.post(url=self.host + path10, headers=self.headers, json=data10)
        # expect10 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
        #             "remindTime": remindTime, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
        #             "groupId": None, "title": "test", "summary": "test", "thumbnail": None,
        #             "contentVersion": 1, "contentUpdateTime": int
        #             }
        time10 = 0
        for i in res10.json()["webNotes"]:
            if i["noteId"] == content_data["noteId"]:
                time10 = time10 + 1
                CheckMethod().output_check(expect10, i)
        print(time10)
        if time10 != 1:
            if time10 >= 1:
                print("存在重复数据")
            else:
                print("不存在该条数据")
        else:
            print("存在且仅存在一条该便签")
        return time10, res10

    def group_note_get_8(self, userId, wps_sid, expect8, noteid, groupid, startIndex=0, rows=50):
        path8 = '/v3/notesvr/web/getnotes/group'
        data8 = {
            "groupId": groupid,
            "startIndex": startIndex,
            "rows": rows
        }
        # res8 = requests.post(url=self.host + path8, headers=self.headers, json=data8)
        res8 = ApiRe().post(url=self.host + path8, userId=userId, wps_sid=wps_sid,
                            body=data8)  # json=body,body=data
        # expect8 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
        #            "remindTime": 0, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
        #            "groupId": "A", "title": "test", "summary": "test", "thumbnail": None,
        #            "contentVersion": 1, "contentUpdateTime": int
        #            }
        time8 = 0
        for i in res8.json()["webNotes"]:
            if i["noteId"] == noteid:
                CheckMethod().output_check(expect8, i)
                time8 = time8 + 1
        print(time8)
        if time8 != 1:
            if time8 >= 1:
                print("存在重复数据")
            else:
                print("不存在该条数据")
        else:
            print("存在且仅存在一条该便签")
        return time8

    def delete_note_5(self, userId, wps_sid, noteid):
        path5 = '/v3/notesvr/delete'
        data5 = {
            "noteId": noteid,
        }
        res5 = ApiRe().post(url=self.host + path5, userId=userId, wps_sid=wps_sid,
                            body=data5)  # json=body,body=data
        expect5 = {"responseTime": int}
        try:
            CheckMethod().output_check(expect5, res5.json())
            print("便签软删除成功！")
        except Exception as e:
            print("便签软删除过程发生异常！")

    def Recyclebin_note_recover_12(self, userid, wps_sid, noteid, startindex=0, rows=999):
        path12 = f'/v3/notesvr/user/{userid}/notes'
        headers12 = {
            'Cookie': wps_sid
        }
        data12 = {
            "userId": userid,
            "noteIds": [str(noteid)]
        }
        res12 = requests.patch(self.host + path12, headers=headers12, json=data12)
        if res12.status_code == 200:
            print("便签恢复成功！")
        else:
            print("便签恢复过程发生异常！")
        return res12.status_code

    def Recyclebin_note_get_11(self, userid, wps_sid, noteid, expect11):
        path11 = f'/v3/notesvr/user/{userid}/invalid/startindex/0/rows/50/notes'
        res11 = ApiRe().get(url=self.host + path11, wps_sid=wps_sid)  # json=body,body=data
        time11 = 0
        if res11.json()["webNotes"] != []:
            for i in res11.json()["webNotes"]:
                if i["noteId"] == noteid:
                    CheckMethod().output_check(expect11, i)
                    time11 = time11 + 1
            print(time11)
            if time11 != 1:
                if time11 >= 1:
                    print("存在重复数据")
                else:
                    print("不存在该条数据")
            else:
                print("存在且仅存在一条该便签")
        else:
            CheckMethod().output_check(expect11, res11.json())
            print("请求接口'11.查看回收站下便签列表'的返回结果包含的便签数量为0，即不存在任何便签数据！！！")
        return time11, res11

    def Recyclebin_note_delete_13(self, userid, wps_sid):
        path13 = f'/v3/notesvr/cleanrecyclebin'
        data13 = {
            "noteIds": ["-1"]
        }
        res13 = ApiRe().post(url=self.host + path13, userId=userid, wps_sid=wps_sid,
                             body=data13)  # json=body,body=data
        expect13 = {"responseTime": int}
        try:
            CheckMethod().output_check(expect13, res13.json())
            print("便签在回收站内删除成功！")
        except Exception as e:
            print("便签在回收站内删除过程发生异常！")
        return

    def Create_group_7(self, userid, wps_sid):
        path7 = f'/v3/notesvr/set/notegroup'
        groupid = f'{str(int(time.time() * 1000))}_groupId'
        groupname = f'{groupid}_groupName'
        data7 = {
            "groupId": groupid,
            "groupName": groupname,
            "order": 0
        }
        res7 = ApiRe().post(url=self.host + path7, userId=userid, wps_sid=wps_sid,
                            body=data7)  # json=body,body=data
        expect7 = {"responseTime": int, "updateTime": int}
        CheckMethod().output_check(expect7, res7.json())
        return data7

    # def Get_groups_6(self, userid, wps_sid, groupid_check, expect6, excludeInvalid=False):
    #     '''
    #     调用接口“6.获取分组列表”查看返回体对齐内容
    #     可传入参数(想要查询的分组)验证是否存在
    #     :param groupid_check:
    #     :param expect6:
    #     :param userid:
    #     :param wps_sid:
    #     :param excludeInvalid:
    #     :return:
    #     '''
    #     path6 = f'/v3/notesvr/get/notegroup'
    #     data6 = {
    #         "excludeInvalid": excludeInvalid
    #     }
    #     res6 = ApiRe().post(url=self.host + path6, userId=userid, wps_sid=wps_sid,
    #                         body=data6)  # json=body,body=data
    #     print(res6.json())
    #     if expect6["noteGroups"] == []:  # 当预测返回结果中"noteGroups":[]时
    #         try:
    #             CheckMethod().output_check(expect6, res6.json())
    #             print("请求接口'6.获取分组列表'的返回结果包含的分组数量为0，即不存在任何分组信息！！！")
    #         except Exception as e:
    #             print("接口6的返回结果错误")
    #     else:
    #         time6 = 0
    #         if res6.json()["noteGroups"] != []:
    #             for i in res6.json()["noteGroups"]:
    #                 if groupid_check == i["groupId"]:
    #                     CheckMethod().output_check(expect6, i)
    #                     time6 = time6 + 1
    #             print(time6)
    #             if time6 == 0:
    #                 print("分组不存在失效")
    #             elif time6 != 1:
    #                 if time6 > 1:
    #                     print("存在重复分组id")
    #                 else:  # (考虑负数)
    #                     print("不存在该分组id")
    #             else:
    #                 print("存在且仅存在一个该分组id")
    #         else:
    #             try:
    #                 CheckMethod().output_check(expect6, res6.json())
    #                 print("请求接口'6.获取分组列表'的返回结果包含的分组数量为0，即不存在任何分组信息！！！")
    #             except Exception as e:
    #                 print("接口6的返回结果错误")
    #     return res6
    def Get_groups_6(self, userid, wps_sid, groupid_check, expect6, excludeInvalid=False):
        '''
        调用接口“6.获取分组列表”查看返回体对齐内容
        可传入参数(想要查询的分组)验证是否存在
        :param groupid_check:
        :param expect6:
        :param userid:
        :param wps_sid:
        :param excludeInvalid:
        :return:
        '''
        path6 = f'/v3/notesvr/get/notegroup'
        data6 = {
            "excludeInvalid": excludeInvalid
        }
        res6 = ApiRe().post(url=self.host + path6, userId=userid, wps_sid=wps_sid,
                            body=data6)  # json=body,body=data
        print(res6.json())
        groups_id = []
        for g_information in res6.json()["noteGroups"]:
            groups_id.append(g_information["groupId"])
        print(groups_id)
        if groupid_check not in groups_id:
            try:
                CheckMethod().output_check(expect6, res6.json())
                print("请求接口'6.获取分组列表'的返回结果包含的分组数量为0，即不存在任何分组信息！！！")
            except Exception as e:
                print("接口6的返回结果错误")
        else:
            time6 = 0
            if res6.json()["noteGroups"] != []:
                for i in res6.json()["noteGroups"]:
                    if groupid_check == i["groupId"]:
                        CheckMethod().output_check(expect6, i)
                        time6 = time6 + 1
                print(time6)
                if time6 == 0:
                    print("分组不存在失效")
                elif time6 != 1:
                    if time6 > 1:
                        print("存在重复分组id")
                    else:  # (考虑负数)
                        print("不存在该分组id")
                else:
                    print("存在且仅存在一个该分组id")
            else:
                try:
                    CheckMethod().output_check(expect6, res6.json())
                    print("请求接口'6.获取分组列表'的返回结果包含的分组数量为0，即不存在任何分组信息！！！")
                except Exception as e:
                    print("接口6的返回结果错误")
        return res6

    def delete_group_9(self, userid, wps_sid, groupid):
        path9 = f'/notesvr/delete/notegroup'
        data9 = {"groupId": groupid}
        res9 = ApiRe().post(url=self.host + path9, userId=userid, wps_sid=wps_sid,
                            body=data9)  # json=body,body=data
        expect9 = {"responseTime": int}
        CheckMethod().output_check(expect9, res9.json())
        print("分组删除成功！")

    def create_note_body_2(self, userid, wps_sid, remindTime=None, remindType=None, groupId=None):
        path = '/v3/notesvr/set/noteinfo'
        data2 = {
            'noteId': f'{str(int(time.time() * 1000))}_noteId',  # 只是创建普通便签，其他optional不填
            "star": 0,
            "remindTime": remindTime,
            "remindType": remindType,
            "groupId": groupId
        }
        res2 = ApiRe().post(url=self.host + path, userId=userid, wps_sid=wps_sid,
                           body=data2)  # json=body,body=data
        print(data2["noteId"])
        return data2

    def create_note_body_2_num(self, userid, wps_sid, remindTime=None, remindType=None, groupId=None,
                               num=1):
        path = '/v3/notesvr/set/noteinfo'
        group_noteids = []
        for i in range(num):
            data2 = {
                'noteId': f'{str(int(time.time() * 1000))}_noteId',  # 只是创建普通便签，其他optional不填
                "star": 0,
                "remindTime": remindTime,
                "remindType": remindType,
                "groupId": groupId
            }
            res2 = ApiRe().post(url=self.host + path, userId=userid, wps_sid=wps_sid,
                               body=data2)  # json=body,body=data
            # print(data2["noteId"])
            group_noteids.append(data2["noteId"])
        print(group_noteids)
        return group_noteids

    def create_note_content_3(self, userid, wps_sid, noteid_body):
        path3 = '/v3/notesvr/set/notecontent'
        data3 = {
            'noteId': noteid_body,
            'title': 'test',
            'summary': 'test',
            'body': 'test',
            'localContentVersion': 1,
            'BodyType': 0
        }
        res3 = ApiRe().post(url=self.host + path3, userId=userid, wps_sid=wps_sid,
                           body=data3)  # json=body,body=data
        print(data3["noteId"], f'title:{data3["title"]}, summary:{data3["summary"]}, body:{data3["body"]}')
        return data3

if __name__ == "__main__":
    userId1 = '758797333'
    wps_sid1 = 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415'
    cb_res = '1707815822112_noteId'
    content_data = {
        'noteId': cb_res,
        'title': 'test',
        'summary': 'test',
        'body': 'test',
        'localContentVersion': 1,
        'BodyType': 0
    }
    expect8 = {"noteId": content_data["noteId"], "createTime": int, "star": 0,
               "remindTime": 0, "remindType": 0, "infoVersion": 1, "infoUpdateTime": int,
               "groupId": "A", "title": "test", "summary": "test", "thumbnail": None,
               "contentVersion": 2, "contentUpdateTime": int
               }
    # InterfaceCall().group_note_get_8(content_data, expect8)
    # InterfaceCall().Recyclebin_note_get_12(userId1, wps_sid1, noteid="1707935567330_noteId")
    InterfaceCall().Get_groups_6(userId1, wps_sid1, 123, )
