from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from langchain_community.chat_models import ChatTongyi
import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

TongyiModel = ChatTongyi(
    model='qwen-max',
    api_key=os.getenv("DASHSCOPE_API_KEY")
)


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
