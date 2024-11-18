# 大模型应用实践课
## 文本纠错助手
![文本纠错助手.png](images%2F%E6%96%87%E6%9C%AC%E7%BA%A0%E9%94%99%E5%8A%A9%E6%89%8B.png)
## 微博文案生成助手
![微博文案生成助手.png](images%2F%E5%BE%AE%E5%8D%9A%E6%96%87%E6%A1%88%E7%94%9F%E6%88%90%E5%8A%A9%E6%89%8B.png)
## How to use
### 直接运行
- `streamlit run 首页.py`
### 使用Docker
- Dockerfile其中的DASHSCOPE_API_KEY应自行修改或在页面上输入
- `docker build -t llm_app .`
- `docker run -p 8501:8501 llm_app`
