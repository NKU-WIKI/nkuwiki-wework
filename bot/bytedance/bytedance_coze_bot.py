# encoding:utf-8
import re
import time
from typing import List, Tuple

import requests
from requests import Response

from bot.bot1 import Bot
from bot.chatgpt.chat_gpt_session import ChatGPTSession
from bot.session_manager import SessionManager
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from config import conf
from channel.wework.run import wework
class ByteDanceCozeBot(Bot):
    def __init__(self):
        super().__init__()
        self.sessions = SessionManager(ChatGPTSession, model=conf().get("model") or "coze")

    def reply(self, query, context=None):
        # acquire reply content
        
        if context.type == ContextType.TEXT:
            logger.info("[COZE] query={}".format(query))
            
            session_id = context["session_id"]
            session = self.sessions.session_query(query, session_id)
            logger.debug("[COZE] session query={}".format(session.messages))
            reply_content, err = self._reply_text(session_id, session)
            if err is not None:
                logger.error("[COZE] reply error={}".format(err))
                return Reply(ReplyType.ERROR, "我暂时遇到了一些问题，请您稍后重试~")
            logger.debug(
                "[COZE] new_query={}, session_id={}, reply_cont={}, completion_tokens={}".format(
                    session.messages,
                    session_id,
                    reply_content["content"],
                    reply_content["completion_tokens"],
                )
            )
            self.sessions.session_reply(reply_content["content"], session_id, reply_content["total_tokens"])
            response = reply_content["content"]
            relust = remove_markdown(response)
            return Reply(ReplyType.TEXT, relust)
        
        elif context.type == ContextType.IMAGE_CREATE:
            logger.info("[COZE] painting={}".format(query))
            session_id = context["session_id"]
            session = self.sessions.session_query(query, session_id)
            logger.debug("[COZE] session query={}".format(session.messages))
            reply_content, err = self._reply_text(session_id, session)
            if err is not None:
                logger.error("[COZE] reply error={}".format(err))
                return Reply(ReplyType.ERROR, "我暂时遇到了一些问题，请您稍后重试~")
            logger.debug(
                "[COZE] new_query={}, session_id={}, reply_cont={}, completion_tokens={}".format(
                    session.messages,
                    session_id,
                    reply_content["content"],
                    reply_content["completion_tokens"],
                )
            )
            self.sessions.session_reply(reply_content["content"], session_id, reply_content["total_tokens"])
            response = reply_content["content"]
            # if "lf-bot-studio-plugin" in response:
            image_url = extract_markdown_image_url(response)
            url = image_url if image_url else has_url(response)
            relust = remove_markdown(response)
            # return Reply(ReplyType.TEXT, relust)
            return Reply(ReplyType.IMAGE_URL, url)
        else:
            reply = Reply(ReplyType.ERROR, "Bot不支持处理{}类型的消息".format(context.type))
            return reply


    def _get_api_base_url(self):
        return conf().get("coze_api_base", "https://api.coze.cn/open_api/v2")

    def _get_headers(self):
        return {
            'Authorization': f"Bearer {conf().get('coze_api_key', '')}"
        }

    def _get_payload(self, user: str, query: str, chat_history: List[dict]):
        return {
            'bot_id': conf().get('coze_bot_id'),
            "user": user,
            "query": query,
            "chat_history": chat_history,
            "stream": False
        }
    def _reply_text(self, session_id: str, session: ChatGPTSession, retry_count=0):
        try:
            query, chat_history = self._convert_messages_format(session.messages)
            base_url = self._get_api_base_url()
            chat_url = f'{base_url}/chat'
            headers = self._get_headers()
            payload = self._get_payload(session.session_id, query, chat_history)
            response = requests.post(chat_url, headers=headers, json=payload)
            if response.status_code != 200:
                error_info = f"[COZE] response text={response.text} status_code={response.status_code}"
                logger.warn(error_info)
                return None, error_info
            answer, err = self._get_completion_content(response)
            if err is not None:
                return None, err
            completion_tokens, total_tokens = self._calc_tokens(session.messages, answer)
            return {
                "total_tokens": total_tokens,
                "completion_tokens": completion_tokens,
                "content": answer
            }, None
        except Exception as e:
            if retry_count < 2:
                time.sleep(3)
                logger.warn(f"[COZE] Exception: {repr(e)} 第{retry_count + 1}次重试")
                return self._reply_text(session_id, session, retry_count + 1)
            else:
                return None, f"[COZE] Exception: {repr(e)} 超过最大重试次数"

    def _convert_messages_format(self, messages) -> Tuple[str, List[dict]]:
        chat_history = []
        for message in messages:
            role = message.get('role')
            if role == 'user':
                content = message.get('content')
                chat_history.append({"role":"user", "content": content, "content_type":"text"})
            elif role == 'assistant':
                content = message.get('content')
                chat_history.append({"role":"assistant", "type":"answer", "content": content, "content_type":"text"})
            elif role =='system':
                # TODO: deal system message
                pass
        user_message = chat_history.pop()
        if user_message.get('role') != 'user' or user_message.get('content', '') == '':
            raise Exception('no user message')
        query = user_message.get('content')
        logger.debug("[COZE] converted coze messages: {}".format([item for item in chat_history]))
        logger.debug("[COZE] user content as query: {}".format(query))
        return query, chat_history

    def _get_completion_content(self, response: Response):
        json_response = response.json()
        if json_response['msg'] != 'success':
            return None, f"[COZE] Error: {json_response['msg']}"
        answer = None
        for message in json_response['messages']:
            if message.get('type') == 'answer':
                answer = message.get('content')
                break
        if not answer:
            return None, "[COZE] Error: empty answer"
        return answer, None

    def _calc_tokens(self, messages, answer):
        # 简单统计token
        completion_tokens = len(answer)
        prompt_tokens = 0
        for message in messages:
            prompt_tokens += len(message["content"])
        return completion_tokens, prompt_tokens + completion_tokens

def remove_markdown(text):
    # 替换Markdown的粗体标记
    text = text.replace("**", "")
    # 替换Markdown的标题标记
    text = text.replace("### ", "").replace("## ", "").replace("# ", "")
    # 去除链接外部括号
    text = re.sub(r'\((https?://[^\s\)]+)\)', r'\1', text)
    text = re.sub(r'\[(https?://[^\s\]]+)\]', r'\1', text)
    return text

def extract_markdown_image_url(content):
    """提取包含s.coze.cn域名的图片URL（不限Markdown格式）"""
    # 修改正则表达式，匹配任意位置出现的s.coze.cn链接
    coze_image_pattern = r'(https://s\.coze\.cn[^\s\)]+)'
    image_url = re.search(coze_image_pattern, content)
    return image_url.group(1) if image_url else None

def has_url(content):
    # 原有函数保持不变，优先使用新函数提取图片URL
    image_url = extract_markdown_image_url(content)
    if image_url:
        return image_url
    
    # 原有普通URL匹配逻辑
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    url = re.search(url_pattern, content)
    return url.group() if url else False