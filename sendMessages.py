# -*- coding: utf-8 -*-
import ntwork
import pymysql

import getConversationId


class SendMessages:
    time = "'2025-07-07 00:00:00'"
    sleepInterval = 3
    mysql = {"host": "",
             "user": "",
             "password": "",
             "name": "",}
    conversationId = ""
    wework = ntwork.WeWork()

    def __init__(self, host, user, password, name, startTime, conversationId, wework):
        ##设置时间,初始化为2000-01-01 00:00:00
        self.time = startTime

        self.mysql['host'] = host
        self.mysql['user'] = user
        self.mysql['password'] = password
        self.mysql['name'] = name

        self.conversationId = conversationId

        self.wework = wework


    def getColumnInfo(self, table, column, cursor):
        if column == "create_time":
            sql = "select create_time from wxapp_post order by create_time desc limit 1"
            cursor.execute(sql)
            resTime = cursor.fetchall()
            time = "'" + resTime[0][0].strftime("%Y-%m-%d %H:%M:%S") + "'"
            print(time)
            return time
        else:
            sql = "select " + column + " from " + table + " where create_time > " + self.time
            cursor.execute(sql)
            res = cursor.fetchall()
            print(res)
            return res

    def generateMessages(self, title, url):
        # 生成聊天信息
        messages = []
        for i in range(len(url)):
            if url[i][0]:
                message = title[i][0] + "\n" + url[i][0]
            else:
                message = title[i][0] + "\n" + ""

            messages.append(message)

        print(messages)

        return messages

    def sendMessage(self):
        # 连接mysql
        isConnected = False

        while not isConnected:
            try:
                db = pymysql.connect(host=self.mysql['host'],
                                     user=self.mysql['user'],
                                     password=self.mysql['password'],
                                     database=self.mysql['name'])
                isConnected = True
            except:
                isConnected = False
                print("time out, try again")

        cursor = db.cursor()

        resTitle = self.getColumnInfo("wxapp_post", "title", cursor)
        resUrl = self.getColumnInfo("wxapp_post", "url_link", cursor)
        messages = self.generateMessages(resTitle, resUrl)

        #更新时间
        self.getColumnInfo("wxapp_post", "create_time", cursor)

        # 发送消息
        for i in messages:
            self.wework.send_text(conversation_id=self.conversationId, content=i)

        # 关闭游标和数据库连接
        cursor.close()
        db.close()