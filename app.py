# -*- coding: utf-8 -*-
import sys
from time import sleep

import ntwork
import pymysql

##设置时间,初始化为2000-01-01 00:00:00
time = "'2025-07-01 00:00:00'"
sleepInterval = 1800

while True:
    #连接mysql
    isConnected = False

    while not isConnected:
        try:
            db = pymysql.connect(host='host',
                                 user='user',
                                 password='passwd',
                                 db='database')
            isConnected = True
        except:
            isConnected = False

    #选择标题
    cursor = db.cursor()


    sql = ("select title from table where create_time >= " + time)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)


    sql = ("select create_time from table order by create_time desc limit 1")
    cursor.execute(sql)
    resTime = cursor.fetchall()
    time = "'" + resTime[0][0].strftime("%Y-%m-%d %H:%M:%S") + "'"
    print(time)

    wework = ntwork.WeWork()

    # 打开pc企业微信, smart: 是否管理已经登录的企业微信
    wework.open(smart=True)

    # 等待登录
    wework.wait_login()

    # 发送消息
    for i in result:
        wework.send_text(conversation_id="id", content=str(i[0]))

    # 关闭游标和数据库连接
    cursor.close()
    db.close()

    #关闭ntwork
    ntwork.exit_()

    time.sleep(sleepInterval)
