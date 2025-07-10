import sys
import ntwork
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

    while True:
        getMsg = getMessages.GetMessages(host, user, passwd, name, create_time, table, column, wework)

        create_time, messages_tmp = getMsg.getMessage()
        messages = messages + messages_tmp

        if len(messages) >= post_num:
            for message in messages:
                wework.send_text(roomId, message)
            messages = []

        sleep(sleepInterval)
except KeyboardInterrupt:
    ntwork.exit_()
    sys.exit()