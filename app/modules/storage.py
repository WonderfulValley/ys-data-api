import oss2
import hashlib
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image
import base64


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

    # def file_upload(self, file_name, file_prefix):
    #     file_object = open(file_name, "rb").read()
    #     sha256 = hashlib.sha256(file_object).hexdigest().lower()
    #     file_type = file_name.split(".")[-1]
    #     upload_name = sha256.lower() + "." + file_type
    #     response = self.bucket.put_object_from_file(file_prefix + "/" + upload_name, file_name)
    #     os.system("rm -rf " + file_name)
    #     return file_prefix + "/" + upload_name

    # def file_upload_image_data(self, file_name, file_prefix, image_data):
    #     sha256 = hashlib.sha256(image_data).hexdigest().lower()
    #     file_type = file_name.split(".")[-1]
    #     upload_name = sha256.lower() + "." + file_type
    #     response = self.bucket.put_object(file_prefix + "/" + file_name, image_data)
    #     return file_prefix + "/" + file_name

    # def file_upload_batch(self, file_names, file_prefix):
    #     result_list = Parallel(n_jobs=min(len(file_names),8))(delayed(self.file_upload)(file_name, file_prefix)for file_name in file_names)
    #     return result_list
    # def file_download(self, file_name):
    #     response = self.bucket.get_object(file_name)
    #     temp_object = response.read()
    #     return temp_object
    #
    # def file_copy(self, source_key, target_key):
    #     self.bucket.copy_object(self.bucket.bucket_name, source_key, target_key)
    #     print("copy成功： " + target_key)

    # def file_download_batch(self, file_names):
    #     result_list = Parallel(n_jobs=min(len(file_names),8))(delayed(self.file_download)(file_name)for file_name in file_names)
    #     return result_list
    # def file_upload_md5_image(self, md5_str):
    #     if md5_str is None or len(md5_str) == 0:
    #         return ""
    #     random_uuid = uuid.uuid4()
    #     uuid_str = str(random_uuid)
    #     image_data = base64.b64decode(md5_str)
    #     global_image_storage.file_upload_image_data(uuid_str + ".png", "sd-images", image_data)
    #     return f"sd-images/{uuid_str}.png"
