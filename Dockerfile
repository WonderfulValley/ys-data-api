# 使用官方Python运行时作为父镜像
FROM python:3.8-slim

# 设置环境变量
ENV APP_HOME /app
ENV REPLICATE_API_TOKEN_PRE=r8_8mCh2ACEsB4nHqpZ2D7
ENV REPLICATE_API_TOKEN=${REPLICATE_API_TOKEN_PRE}rTHwLpm4hUFD1P5K3D
ENV ALI_ACCESS_KEY_ID1=LTAI5t9vhJGhFv
ENV ALI_ACCESS_KEY_ID2=4cc3EHdQRe
ENV ALI_ACCESS_KEY_SECRET1=nVgqbMnVoIsTOtoVb
ENV ALI_ACCESS_KEY_SECRET2=Jk130VPkJRrJ6

# 创建并选择一个工作目录
WORKDIR $APP_HOME

# 复制当前目录下的内容到容器中的/app目录
COPY . $APP_HOME

# 安装dependencies和db的dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8010

# 运行应用
# uvicorn main:fastapi --host 0.0.0.0 --port 8010
CMD ["uvicorn", "main:fastapi", "--host", "0.0.0.0", "--port", "8010"]