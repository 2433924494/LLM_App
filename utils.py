import logging
from langchain_community.chat_models import ChatTongyi
from numpy.random import chisquare
from openai import OpenAI
import os
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

# init
model_name='llama3.1-405b-instruct'
client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
TongyiModel = ChatTongyi(
    model='qwen-max',
    api_key=os.getenv("DASHSCOPE_API_KEY")
)


# 文本纠错助手
def text_correction(user_input_text, api_key=None):
    if api_key:
        client.api_key = api_key
    # TODO 若无api_key,拒绝访问
    system_prompt = '''
    你是一个高中语文教师,熟悉各类病句的错误类型,并知道如何解释并修改。
    你的任务是仔细检查用户提供的文本，识别其中存在的**语法错误、拼写错误、用词不当以及标点错误**等各类问题，并给出正确的修正建议和修正后的文本。
    注意**不要有多余的回答**.
    回答示例：
    - **{错误类型1}：**
        - {修改之处，建议及解释}
        - ...
    - **{错误类型2}：**
        - {修改之处，建议及解释}
        - ...
    ...
    - **{错误类型n}：**
        - {修改之处，建议及解释}
        - ...
    - **修改后的句子**：...
    --示例结束--
    若不存在某类错误，则**无需体现**。错误类型包括**["语法错误","拼写错误","用词不当","标点符号错误"]**.
    '''
    try:
        completion = client.chat.completions.create(
            model='qwen-max',  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': '这是需要纠错的句子：“' + user_input_text + '”'}
            ],
            temperature=0.1,
            stream=True
        )
        return completion
    except Exception as e:
        logging.warning(e)
        return "Error!"


# 微博文案小助手
class WeiboText(BaseModel):
    label: str = Field(..., description="文案标签")
    text: str = Field(..., description="文案")


def generate_weibo(user_input_theme, user_input_emotion, api_key=None):
    if api_key:
        TongyiModel.dashscope_api_key = api_key
    system_prompt_template = '''
    假设你精通于撰写微博文案,请根据我的要求生成相应的文案.
    要求:
    1.根据提供的**主题,情感**,生成相关文案,字数50字以上.
    2.携带三个及以上的tag,标签应包含**关键信息**,每个标签以##包裹并以空格间隔,例如'#label#',**注意text内不用带标签**.
    3.以**json格式**返回.
    {parser_instruction}
    '''
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_prompt_template), ("user", "主题:{theme},情感:{emotion}")]
    )
    parser = PydanticOutputParser(pydantic_object=WeiboText)
    parser_instruction = parser.get_format_instructions()
    chain = prompt_template | TongyiModel | parser
    result = chain.invoke(
        {'parser_instruction': parser_instruction,
         'theme': user_input_theme,
         'emotion': user_input_emotion})
    return result

if __name__ == '__main__':
    print(generate_weibo('珠海航展', '激昂'))
