import requests

class Clear:
    host = 'http://note-api.wps.cn'

    def note_clear(self, userid, wps_sid, startindex=0, rows=9999):
        '''
        清空首页的所有标签--1.获取首页便签/5.删除便签(到回收站)/13.清空回收站
        :param rows:
        :param wps_sid:
        :param startindex:
        :param userid: 用户id
        :param sid: 用户cookie
        :return:
        '''
        # 涉及url:1.获取首页便签/5.删除便签(到回收站)/13.清空回收站
        note_get_url = f'{self.host}/v3/notesvr/user/{userid}/home/startindex/{startindex}/rows/{rows}/notes'
        note_delete_url = f'{self.host}/v3/notesvr/delete'
        note_clear_url = f'{self.host}/v3/notesvr/cleanrecyclebin'
        # 个人账号
        headers = {
            'Cookie': wps_sid,
            'X-User-Key': userid,
            'Content-Type': 'application/json'  # POST请求时需要
        }

        # 获取用户的首页便签
        res = requests.get(note_get_url, headers=headers)
        noteids_get = []
        if res.json()["webNotes"] is not []:
            for item in res.json()["webNotes"]:  # 遍历获取到所有便签，提取其中的noteId
                noteids_get.append(item["noteId"])

            # 删除首页所有便签
            for noteid in noteids_get:
                body = {
                    "noteId": noteid  # 接口要求传入的请求body
                }
                res_delete = requests.post(note_delete_url, headers=headers, json=body)

            # 清空 回收站 所有便签
            clear_body = {
                "noteIds": [-1]
            }
            res_clear = requests.post(note_clear_url, headers=headers, json=clear_body)
        return res_clear.status_code, noteids_get

    def group_note_clear(self, userid, wps_sid):
        # 涉及url:6.获取分组列表 遍历分组列表  5.删除分组标签  清空回收站
        groups_get_url = f'{self.host}/v3/notesvr/get/notegroup'
        groups_note_get_url = f'{self.host}/v3/notesvr/web/getnotes/group'
        note_delete_url = f'{self.host}/v3/notesvr/delete'
        note_clear_url = f'{self.host}/v3/notesvr/cleanrecyclebin'
        # 个人账号
        headers = {
            'Cookie': wps_sid,
            'X-User-Key': userid,
            'Content-Type': 'application/json'  # POST请求时需要
        }
        # 6.获取分组列表
        body_groups = {
            'excludeInvalid': True
        }
        res_groups = requests.post(groups_get_url, headers=headers, json=body_groups)
        groups_get = []
        for item in res_groups.json()["noteGroups"]:  # 遍历获取到所有便签，提取其中的noteId
            # print(item)
            groups_get.append(item["groupId"])
        print(groups_get)

        # 8.查看分组标签，遍历groups所有便签并收集
        group_noteids_get = []
        for group in groups_get:  # 每个分组
            body_group = {
                'groupId': group,  # required
                'startIndex': 0,  # optional
                'rows': 999  # optional
            }
            res_group_notes = requests.post(groups_note_get_url, headers=headers,
                                            json=body_group)
            # print(group)
            # print(res_group_notes.json())
            if res_group_notes.json() is not []:
                for item in res_group_notes.json()["webNotes"]:
                    group_noteids_get.append(item["noteId"])
        # 5.删除所有(首页、分组)便签
        for group_noteid in group_noteids_get:
            body_group_noteid = {
                "noteId": group_noteid  # 接口要求传入的请求body
            }
            res_delete = requests.post(note_delete_url, headers=headers, json=body_group_noteid)

        # 清空 回收站 所有便签
        clear_body = {
            "noteIds": [-1]
        }
        res_clear = requests.post(note_clear_url, headers=headers, json=clear_body)
        return res_clear.status_code, group_noteids_get

    def calendar_note_clear(self, userid, wps_sid):
        '''
        清空首页的所有标签--1.获取首页便签/5.删除便签(到回收站)/13.清空回收站
        :param wps_sid:
        :param userid: 用户id
        :return:
        '''
        # 涉及url:10.查看日历下便签/5.删除便签(到回收站)/13.清空回收站
        calendar_note_get_url = f'{self.host}/v3/notesvr/web/getnotes/remind'
        note_delete_url = f'{self.host}/v3/notesvr/delete'
        note_clear_url = f'{self.host}/v3/notesvr/cleanrecyclebin'
        # 个人账号
        headers = {
            'Cookie': wps_sid,
            'X-User-Key': userid,
            'Content-Type': 'application/json'  # POST请求时需要
        }

        # 接口"10.查看日历下便签"
        data10 = {
            "remindStartTime": 1703952000, "remindEndTime": 1709136000, "startIndex": 0, "rows": 999
        }
        res = requests.post(calendar_note_get_url, headers=headers, json=data10)
        noteids_get = []
        if res.json()["webNotes"] is not []:
            for item in res.json()["webNotes"]:  # 遍历获取到所有便签，提取其中的noteId
                noteids_get.append(item["noteId"])

            # 删除首页所有便签
            for noteid in noteids_get:
                body = {
                    "noteId": noteid  # 接口要求传入的请求body
                }
                res_delete = requests.post(note_delete_url, headers=headers, json=body)

            # 清空 回收站 所有便签
            clear_body = {
                "noteIds": [-1]
            }
            res_clear = requests.post(note_clear_url, headers=headers, json=clear_body)
        return res_clear.status_code, noteids_get




if __name__ == "__main__":
    wps_sid1 = 'wps_sid=V02SQzSIdSSJrlietN-FXU2L2GHPc8000adf855d002d3a5415'
    userId1 = '758797333'
    print(Clear().note_clear(userId1, wps_sid1))
    # print(Clear().group_note_clear(userId1, wps_sid1))
    # print(Clear().calendar_note_clear(userId1, wps_sid1))
