import requests
import oss2
import hashlib
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image
import base64

# 填Key
aa = "sk-5hsEXPEOUl"
aa = aa + "oLypArXsRhT3BlbkFJDQ0shgBKhufWbx63KARW"

class OSSStorage():
    def __init__(self, access_key, secret_key, endpoint, bucket):
        self.auth = oss2.Auth(access_key, secret_key)
        self.session = oss2.Session(pool_size=1000)
        # todo 这个是外网，走流量
        # endpoint = "oss-cn-beijing.aliyuncs.com"
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket, enable_crc=False, session=self.session)

    def is_url(self, s):
        try:
            result = urlparse(s)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def file_sign_oss_path(self, oss_path):
        if self.is_url(oss_path):
            parsed_url = urlparse(oss_path)
            new_oss_path = parsed_url.path.lstrip('/')
            params = dict()
            params['x-oss-process'] = "image/format,webp"
            url = self.bucket.sign_url('GET', new_oss_path, 3600, slash_safe=True, params=params)
        else:
            params = dict()
            params['x-oss-process'] = "image/format,webp"
            url = self.bucket.sign_url('GET', oss_path, 3600, slash_safe=True, params=params)
            print(url)
        return url

    def file_base64_oss_path(self, oss_path):
        if self.is_url(oss_path):
            parsed_url = urlparse(oss_path)
            new_oss_path = parsed_url.path.lstrip('/')
            style = 'image/format,webp'
            # 读取OSS中的文件到内存中
            resp = self.bucket.get_object(new_oss_path, process=style)
            content = resp.read()
            # 将文件内容转换为Base64编码
            base64_encoded_str = base64.b64encode(content).decode('utf-8')
            # 打印Base64编码的字符串
        else:
            style = 'image/format,webp'
            # 读取OSS中的文件到内存中
            resp = self.bucket.get_object(oss_path, process=style)
            content = resp.read()
            # 将文件内容转换为Base64编码
            base64_encoded_str = base64.b64encode(content).decode('utf-8')
            # 打印Base64编码的字符串
        return base64_encoded_str

    def file_upload_from_url(self, url, file_prefix, tmp_name=None):
        # 将url里的图片直接上传到oss
        input = requests.get(url)
        image = Image.open(BytesIO(input.content))
        sha256 = hashlib.sha256(input.content).hexdigest().lower()
        file_type = 'png'
        if tmp_name is not None:
            upload_name = tmp_name
        else:
            upload_name = sha256.lower() + "." + file_type
        response = self.bucket.put_object(file_prefix + "/" + upload_name, input)
        return {"oss_path": file_prefix + "/" + upload_name,
                "width": image.width,
                "height": image.height
                }


def get_bg_prompt_by_base64(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {aa}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请用200个英文单词描述这张图片的背景，忽略所有图片上的文字和前景主体，以便在stable diffusion的文生图中复现该图片的背景"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                             "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    # print(response)
    return response.json()

OSSStorage = OSSStorage(access_key="LTAI5t9vhJGhFv" + "4cc3EHdQRe",
                        secret_key="nVgqbMnVoIsTOtoVb" + "Jk130VPkJRrJ6",
                        endpoint="oss-cn-beijing.aliyuncs.com",
                        bucket='fwings-prod')

str = OSSStorage.file_base64_oss_path("user_images/upload_images/4a66a9c9-db6a-4c3f-bdc4-f881909a7cb6.png")
get_bg_prompt_by_base64(str)
print(get_bg_prompt_by_base64)