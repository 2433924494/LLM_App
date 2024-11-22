from langchain_community.chat_models import ChatTongyi
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

# init
TongyiModel = ChatTongyi(
    model='qwen-max',
    api_key=os.getenv("DASHSCOPE_API_KEY")
)

# 心理咨询师
system_prompt = '''
我是一位名叫{user_name}的客户，而你是一位专业的心理治疗师。
我希望你能表现出富有同理心、慈悲、开放和具有文化敏感性的心理治疗师形象，你擅长精神分析、心理动力学理论和认知行为疗法。
运用积极倾听技巧、开放式问题和清晰的沟通，帮助客户反思他们的思想、情感和经历。
在指导他们找到生活中特定的问题或模式时，请考虑他们的文化背景。
运用跨学科知识，整合精神分析和心理动力学方法，以及运用问题解决技巧和创造力的认知行为疗法技巧。
给予反思性反馈，介绍正念和放松技巧，定期用批判性思维技能检查客户的进展。
赋予客户为自己的康复承担责任的能力，根据客户的需求和喜好调整你的方法。
'''
prompt = ChatPromptTemplate.from_messages(
    [
        ('system', system_prompt),
        MessagesPlaceholder(variable_name='history'),
        ('human', '{input}')
    ]
)
chain = prompt | TongyiModel


def get_by_user_name(user_name: str) -> BaseChatMessageHistory:
    return SQLChatMessageHistory(user_name, 'sqlite:///Lab3_memory.db')


def get_chat_response(user_input, user_name, api_key=None):
    if api_key:
        TongyiModel.api_key = api_key
    chain_with_history = RunnableWithMessageHistory(chain, get_by_user_name, input_messages_key="input",
                                                    history_messages_key="history", )
    return chain_with_history.stream({'user_name': user_name, 'input': user_input},
                                     config={'configurable': {'session_id': user_name}})


