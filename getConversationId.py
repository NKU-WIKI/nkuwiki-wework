# -*- coding: utf-8 -*-
import sys
from time import sleep

import ntwork

class GetConversationId:
    #设置时间，获取不到加长一点
    getTime = 3
    wework = ntwork.WeWork()
    conversationId = []

    def __init__(self, getConversationIdTime, wework):
        self.getTime = getConversationIdTime
        self.wework = wework

    def getId(self,roomName):
        # 获取群列表并输出
        sleep(self.getTime)  # 防止获取不到
        rooms = self.wework.get_rooms()

        while not rooms:
            print("time out when get rooms!")
            self.getTime = self.getTime + 1
            sleep(self.getTime)  # 防止获取不到
            rooms = self.wework.get_rooms()

        print("群列表: ")
        print(rooms)

        #根据群名得到conversationId
        for i in rooms['room_list']:
            for j in roomName:
                if i['nickname'] == j:
                    self.conversationId.append(i['conversation_id'])

        return self.conversationId

