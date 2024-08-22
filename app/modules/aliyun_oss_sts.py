# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys

from typing import List

from alibabacloud_sts20150401.client import Client as Sts20150401Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_sts20150401 import models as sts_20150401_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Sts20150401Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=os.environ.get("ALI_ACCESS_KEY_ID1")+os.environ.get("ALI_ACCESS_KEY_ID2"),
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=os.environ.get("ALI_ACCESS_KEY_SECRET1")+os.environ.get("ALI_ACCESS_KEY_SECRET2")
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Sts
        config.endpoint = f'sts.cn-beijing.aliyuncs.com'
        return Sts20150401Client(config)

    @staticmethod
    def getCredentials() -> None:
        client = Sample.create_client()
        assume_role_request = sts_20150401_models.AssumeRoleRequest(
            duration_seconds=3600,
            role_arn='acs:ram::1091806542022686:role/oss-frontend',
            role_session_name='frontend'
        )
        try:
            # 复制代码运行请自行打印 API 的返回值
            res = client.assume_role_with_options(assume_role_request, util_models.RuntimeOptions())
            if res.status_code == 200:
                credentials = res.body.credentials
                return credentials
                print("export OSS_ACCESS_KEY_ID="+credentials.access_key_id)
                print("export OSS_ACCESS_KEY_SECRET="+credentials.access_key_secret)
                print("export OSS_SESSION_TOKEN="+credentials.security_token)
            else:
                return res
        except Exception as error:
            # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
            # 错误 message
            print(error.message)
            # 诊断地址
            print(error.data.get("Recommend"))
            UtilClient.assert_as_string(error.message)

