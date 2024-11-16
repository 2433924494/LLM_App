# 大模型应用实践课
## 直接运行
- `streamlit run 首页.py`
## 使用Docker
- Dockerfile其中的DASHSCOPE_API_KEY应自行修改或在页面上输入
- `docker build -t llm_app .`
- `docker run -p 8501:8501 llm_app`
