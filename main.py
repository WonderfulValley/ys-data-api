import argparse

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import base64
from functools import wraps
from typing import Dict
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

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


import app.api.tagging

tagging_api = app.api.tagging


@fastapi.post('/removeBg')
def removeBg(input_data: dict, request: Request):
    if 'target_oss_path' not in input_data:
        input_data['target_oss_path'] = 'llp_test'
    oss_url = tagging_api.removeBg(input_data['img'], input_data['target_oss_path'], input_data['user_id'])
    return oss_url


@fastapi.get('/newSts')
def newSts():
    credentials = tagging_api.newCredentials()
    return credentials

# @fastapi.post('/record_user_action')
# def recordUserAction(input_data: dict):
#     if 'ossFilePath' not in input_data:
#         input_data['ossFilePath'] = ''
#     if 'width' not in input_data:
#         input_data['width'] = '0'
#     if 'height' not in input_data:
#         input_data['height'] = '0'
#     if 'operation_type' not in input_data:
#         input_data['operation_type'] = 'upload'
#     action = tagging_api.recordUserAction(input_data['ossFilePath'], input_data['width'],
#                                                 input_data['height'], input_data['operation_type'],
#                                                 input_data['user_id'])
#     return action

def loadModule(currentModuleName):
    if currentModuleName == "styleConvert":
        import app.api.tagging
        tagging_api = app.api.tagging

        @fastapi.get('/newBackground')
        def newBackground(input_data: dict, request: Request):
            image_path = "1.png"
            base64_image = encode_image(image_path)
            res = tagging_api.newBackground(base64_image)
            return res


# 启动命令示例
# python main.py --currentModuleName=apigateway
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--currentModuleName', type=str, required=False, choices=["styleConvert", "apigateway"],
                        help='currentModuleName', default="styleConvert")
    parser.add_argument('--port', type=int, required=False, help='port', default=80)
    args = parser.parse_args()
    currentModuleName = args.currentModuleName
    port = args.port
    loadModule(currentModuleName)
    uvicorn.run(fastapi, host="0.0.0.0", port=port)
