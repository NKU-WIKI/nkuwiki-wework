import sys
import ntwork

import generateEmoji
import getConversationId
import getMessages
import readConfig
from time import sleep

try:
    globals().update(readConfig.readConfig())

    wework = ntwork.WeWork()
    # 打开pc企业微信, smart: 是否管理已经登录的微信
    wework.open(smart=True)

    # 等待登录
    wework.wait_login()

    getId = getConversationId.GetConversationId(1, wework)

    roomId = getId.getId(rooms)

    messages = []
    msgToSend = []

    while True:
        getMsg = getMessages.GetMessages(host, user, passwd, name, create_time, table, column, wework)

        create_time, messages_tmp = getMsg.getMessage()
        messages = messages + messages_tmp

        if len(messages) >= post_num:
            for i in range(0,len(messages),max_send_num):
                messages_tmp = messages[0:min(max_send_num, len(messages))]
                if len(messages) >= max_send_num:
                    messages = messages[max_send_num:]
                for j in range(len(messages_tmp)):
                    message = generateEmoji.generateEmoji(j) + messages_tmp[j]
                    if message == generateEmoji.generateEmoji(j) + messages_tmp[0]:
                        msgToSend.append(message)
                    else:
                        msgToSend[i//max_send_num] = msgToSend[i//max_send_num] + "\n\n" + message

            for room in roomId:
                for msg in msgToSend:
                    wework.send_text(room, msg)
            messages = []
            msgToSend = []

        sleep(sleepInterval)
except KeyboardInterrupt:
    ntwork.exit_()
    sys.exit()