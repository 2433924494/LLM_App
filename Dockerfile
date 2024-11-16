
FROM python:3.9-slim

RUN mkdir -p app
ENV DASHSCOPE_API_KEY=xxxx
WORKDIR app
COPY . /app
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
        && pip install -r requirements.txt
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["streamlit", "run", "首页.py", "--server.port=8501", "--server.address=0.0.0.0"]