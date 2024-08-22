from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import base64
from functools import wraps
from typing import Dict
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

from app.utils import user_info_utills
from app.utils.user_info_utills import get_user_openid, get_userid_by_openid

currentModuleName = "apigateway"
model_path = "/modules"

fastapi = FastAPI()
fastapi.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源跨域访问，也可以指定具体的来源
    allow_credentials=True,  # 允许发送身份验证信息（如cookies）
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP头部
)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


import app.api.style_convert_api

style_convert_api = app.api.style_convert_api


# 验证用户是否登录，jwt换user_id
def validate_user_info(func):
    @wraps(func)
    def wrapper(input_data: Dict, *args, **kwargs):
        if 'jwt' not in input_data or input_data['jwt'] is None:
            print("无用户信息", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            input_data['user_id'] = 0
            return func(input_data, *args, **kwargs)
        jwt = input_data['jwt']
        openid = get_user_openid(jwt)
        print("用户信息openid", openid, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        user_id = get_userid_by_openid(openid)
        input_data['user_id'] = user_id
        print("用户信息user_id", user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return func(input_data, *args, **kwargs)

    return wrapper


@fastapi.post('/removeBg')
@validate_user_info
def removeBg(input_data: dict, request: Request):
    if 'target_oss_path' not in input_data:
        input_data['target_oss_path'] = 'llp_test'
    oss_url = style_convert_api.removeBg(input_data['img'], input_data['target_oss_path'], input_data['user_id'])
    return oss_url


@fastapi.post('/newBackground')
@validate_user_info
def newBackground(input_data: dict):
    if 'target_oss_path' not in input_data:
        input_data['target_oss_path'] = 'llp_test'

    if 'scale' not in input_data:
        input_data['scale'] = 12
    if 'size' not in input_data:
        input_data['size'] = "1024*1024"
    if 'n' not in input_data:
        input_data['n'] = 1
    if 'negative_prompt' not in input_data:
        input_data['negative_prompt'] = "garfield"
    # input_data['user_id'] = 1
    SdxlEngine = config['DEFAULT']['SdxlEngine']
    if SdxlEngine == "aliyun":
        if 'steps' not in input_data:
            input_data['steps'] = 60
        base64_img_str = style_convert_api.newBackground(input_data['img'], input_data['target_oss_path'],
                                                         input_data['steps'], input_data['scale'], input_data['size'],
                                                         input_data['n'], input_data['negative_prompt'],
                                                         input_data['user_id'])
    else:
        # 不支持scale和negative_prompt
        if 'steps' not in input_data:
            input_data['steps'] = 20
        base64_img_str = style_convert_api.newBackgroundReplicate(input_data['img'], input_data['target_oss_path'],
                                                                  input_data['steps'], input_data['scale'],
                                                                  input_data['size'],
                                                                  input_data['n'], input_data['negative_prompt'],
                                                                  input_data['user_id'])
    return base64_img_str


@fastapi.post('/getBackgroundPromptByOssPath')
def getBackgroundPromptByOssPath(input_data: dict):
    base64_img_str = style_convert_api.getBackgroundPromptByOssPath(input_data['oss_path'])
    return base64_img_str


@fastapi.post('/genImage')
def genImage(input_data: dict):
    if 'target_oss_path' not in input_data:
        input_data['target_oss_path'] = 'llp_test'
    if 'steps' not in input_data:
        input_data['steps'] = 60
    if 'scale' not in input_data:
        input_data['scale'] = 12
    if 'size' not in input_data:
        input_data['size'] = "1024*1024"
    if 'n' not in input_data:
        input_data['n'] = 1
    if 'negative_prompt' not in input_data:
        input_data['negative_prompt'] = "garfield"
    base64_img_str = style_convert_api.genImage(input_data['prompt'], input_data['target_oss_path'],
                                                input_data['steps'], input_data['scale'], input_data['size'],
                                                input_data['n'], input_data['negative_prompt'])
    # base64_img_str = style_convert_api.genImageReplicate(input_data['prompt'], input_data['target_oss_path'],
    #                                             input_data['steps'], input_data['scale'], input_data['size'],
    #                                             input_data['n'], input_data['negative_prompt'])
    return base64_img_str


@fastapi.get('/newSts')
def newSts():
    credentials = style_convert_api.newCredentials()
    return credentials


@fastapi.post('/login')
def login(input_data: dict):
    jwt = style_convert_api.login(input_data['code'])
    return jwt


@fastapi.get('/userOpenid')
def userOpenid(input_data: dict):
    jwt = style_convert_api.getUserOpenid(input_data['token'])
    return jwt


@fastapi.post('/record_user_action')
@validate_user_info
def recordUserAction(input_data: dict):
    if 'ossFilePath' not in input_data:
        input_data['ossFilePath'] = ''
    if 'width' not in input_data:
        input_data['width'] = '0'
    if 'height' not in input_data:
        input_data['height'] = '0'
    if 'operation_type' not in input_data:
        input_data['operation_type'] = 'upload'
    action = style_convert_api.recordUserAction(input_data['ossFilePath'], input_data['width'],
                                                input_data['height'], input_data['operation_type'],
                                                input_data['user_id'])
    return action

# def loadModule(currentModuleName):
#     if currentModuleName == "styleConvert":
#         import application.api.style_convert_api
#         style_convert_api = application.api.style_convert_api
#
#         @fastapi.get('/newBackground')
#         def newBackground(input_data: dict, request: Request):
#             print("开始调用gpt4o")
#             image_path = "1.png"
#             base64_image = encode_image(image_path)
#             res = style_convert_api.newBackground(base64_image)
#             print(res)
#             # mysql_utils.insert_data("hegui_user_log", {
#             #     "action": "page",
#             #     "request": json.dumps(input_data, ensure_ascii=False),
#             #     "response": json.dumps(res, ensure_ascii=False)
#             # })
#             print("结束调用gpt4o")
#             return res
#
#
# # 启动命令示例
# # python main.py --currentModuleName=apigateway
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--currentModuleName', type=str, required=False, choices=["styleConvert", "apigateway"],
#                         help='currentModuleName', default="styleConvert")
#     parser.add_argument('--port', type=int, required=False, help='port', default=80)
#     args = parser.parse_args()
#     currentModuleName = args.currentModuleName
#     port = args.port
#     loadModule(currentModuleName)
#     uvicorn.run(fastapi, host="0.0.0.0", port=port)
