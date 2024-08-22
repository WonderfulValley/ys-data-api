from fastapi import FastAPI, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
import requests
import time
from app.model.model import User
from datetime import datetime

from app.utils.mysql_utils import mysqlSession

SECRET_KEY = "jwt-secret-key-lsixkgbgs"  # 请替换为你的密钥
ALGORITHM = "HS256"
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def create_access_token(data: dict, expires_delta: int = 3600):
    to_encode = data.copy()
    expire = time.time() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def login(code: str = Form(...)):
    user_info = req_wx_user_info(code)
    print(user_info, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    js_code = user_info['openid']
    data = {"openid": js_code}
    token = create_access_token(data=data)
    return {"access_token": token, "token_type": "bearer"}

def get_user_openid(token: str):
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    openid = decoded_payload['openid']
    return openid

def get_userid_by_openid(openid: str):
    with mysqlSession() as session:
        # 尝试查询与openid匹配的User
        user = session.query(User).filter_by(source_content=openid).first()
        if user:
            # 如果找到，返回用户的id
            return user.id
        else:
            # 如果没有找到，创建一个新用户
            new_user = User(source_content=openid)
            # 将新用户添加到session中
            session.add(new_user)
            try:
                # 提交事务，将数据保存到数据库
                session.commit()
                # 返回新用户的id
                return new_user.id
            except Exception as e:
                # 如果发生其他错误，回滚事务并抛出异常
                session.rollback()
                raise e


# 替换为你的实际参数
APPID = 'wxac5dd4ccd67ab068'
SECRET = 'e92bec412dbee2b8fce13b3702489e42'

def req_wx_user_info(js_code):
    # 构造请求 URL
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={js_code}&grant_type=authorization_code"

    # 发送 GET 请求
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析 JSON 响应
        result = response.json()
        return result

    else:
        # 请求失败，打印错误信息
        print(f"请求失败，状态码：{response.status_code}，错误信息：{response.text}")
        result = response.json()
        return result
