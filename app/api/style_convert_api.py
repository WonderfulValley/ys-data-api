from app.modules import gpt4o
from app.modules import aliyun_conn
from app.modules import replicate_conn
from app.utils import user_info_utills
from app.modules.storage import OSSStorage
from app.modules.aliyun_oss_sts import Sample
from app.utils.apiUtils import ApiUtils
from datetime import datetime
import os
from app.model.model import UserImageOperation, Image
from app.utils.mysql_utils import mysqlSession
import uuid
import time
import requests

OSSStorage = OSSStorage(access_key=os.environ.get("ALI_ACCESS_KEY_ID1") + os.environ.get("ALI_ACCESS_KEY_ID2"),
                        secret_key=os.environ.get("ALI_ACCESS_KEY_SECRET1") + os.environ.get("ALI_ACCESS_KEY_SECRET2"),
                        endpoint="oss-cn-beijing.aliyuncs.com",
                        bucket='fwings-prod')


def removeBg(oss_path, target_oss_path, user_id):
    img_url = OSSStorage.file_sign_oss_path(oss_path)
    out_img_url = replicate_conn.remove_bg(img_url)
    res_oss = OSSStorage.file_upload_from_url(out_img_url, target_oss_path)
    res_oss_path = res_oss['oss_path']
    recordUserAction(res_oss_path, res_oss['width'], res_oss['height'], "removeBackground", user_id)
    return ApiUtils.ok({"oss_path": res_oss_path})


def is_url_accessible(url):
    try:
        response = requests.get(url)
        # 检查状态码是否是200，表示请求成功
        if response.status_code == 200:
            # 检查Content-Type头部是否表明这是一个图片文件
            content_type = response.headers.get('Content-Type')
            if content_type and content_type.startswith('image/'):
                print("是image")
                tmp_name = str(time.time()) + '.jpg'
                res_oss = OSSStorage.file_upload_from_url(url, "invalid_image_test", tmp_name=tmp_name)
                print(res_oss)
                return True
            else:
                print("不是image", content_type)
                tmp_name = str(time.time()) + '.jpg'
                res_oss = OSSStorage.file_upload_from_url(url, "invalid_image_test", tmp_name=tmp_name)
                print(res_oss)
                return False
        else:
            print("不是200")
            return False
    except requests.exceptions.RequestException as e:
        # 如果请求过程中出现异常，比如网络问题、DNS解析失败等，返回False
        print(e)
        return False


def newBackground(oss_path, target_oss_path, steps, scale, size, n, negative_prompt, user_id):
    print("开始调用gpt4o", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # response = gpt4o.get_bg_prompt(base64_image)
    img_url = OSSStorage.file_sign_oss_path(oss_path)  # 根据oss_path获取外部可访问的url
    print("gpt4o使用的url为：", img_url)
    response = gpt4o.get_bg_prompt(img_url)  # 访问gpt4o
    try:
        prompt = response['choices'][0]['message']['content']
    except Exception as error:
        print("图片第一次访问gpt4o失败", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("gpt4o使用的url为：", img_url)
        if is_url_accessible(img_url):
            print("自行访问url成功1", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print("url确实无法访问1", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print(response)
        # print(error.message)
        time.sleep(5)
        print("暂停5秒尝试第二次访问gpt4o")
        response = gpt4o.get_bg_prompt(img_url)  # 访问gpt4o
        try:
            prompt = response['choices'][0]['message']['content']
        except Exception as error:
            print("图片第二次访问gpt4o失败", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if is_url_accessible(img_url):
                print("自行访问url成功2", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                print("url确实无法访问2", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print(response)
            # print(error.message)
            time.sleep(5)
            print("暂停5秒尝试第三次访问gpt4o")
            response = gpt4o.get_bg_prompt(img_url)  # 访问gpt4o
            try:
                prompt = response['choices'][0]['message']['content']
            except Exception as error:
                print("图片第三次访问gpt4o失败", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                if is_url_accessible(img_url):
                    print("自行访问url成功3", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    print("url确实无法访问3", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                print(response)
                print(error.message)
                prompt = None
    if prompt is None:
        return ApiUtils.err(message="生图失败")
    print("结束调用gpt4o", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("开始调用sdxl", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    img_results = aliyun_conn.aliyun_sdxl(prompt, steps, scale, size, n, negative_prompt)
    oss_res_paths = []
    size_parts = size.split('*')
    for img_result in img_results:
        oss_res_path = OSSStorage.file_upload_from_url(img_result.url, target_oss_path)['oss_path']
        oss_res_paths.append(oss_res_path)
        recordUserAction(oss_res_path, size_parts[0], size_parts[1], "repaint", user_id)
    print("结束调用sdxl", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return ApiUtils.ok({"oss_res_paths": oss_res_paths, "prompt": prompt})


def newBackgroundReplicate(oss_path, target_oss_path, steps, scale, size, n, negative_prompt, user_id):
    print("开始调用gpt4o", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    base64_str = OSSStorage.file_base64_oss_path(oss_path)
    response = gpt4o.get_bg_prompt_by_base64(base64_str)  # 访问gpt4o
    try:
        prompt = response['choices'][0]['message']['content']
        print("prompt=", prompt)
    except Exception as error:
        print("图片第一次访问gpt4o失败", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        time.sleep(5)
        print("暂停5秒尝试第二次访问gpt4o")
        response = gpt4o.get_bg_prompt_by_base64(base64_str)  # 访问gpt4o
        try:
            prompt = response['choices'][0]['message']['content']
        except Exception as error:
            print("图片第二次访问gpt4o失败", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            time.sleep(5)
            print("暂停5秒尝试第三次访问gpt4o")
            response = gpt4o.get_bg_prompt_by_base64(base64_str)  # 访问gpt4o
            try:
                prompt = response['choices'][0]['message']['content']
            except Exception as error:
                print("图片第三次访问gpt4o失败", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                print(response)
                print(error)
                prompt = None
    if prompt is None:
        return ApiUtils.err(message="生图失败")
    print("结束调用gpt4o", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("开始调用sdxl", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    size_parts = size.split('*')
    img_results = replicate_conn.replicate_sdxl(prompt, steps=steps, scale=scale, w=size_parts[0], h=size_parts[1], n=n,
                                                negative_prompt=negative_prompt)
    print(img_results)
    oss_res_paths = []
    for img_result in img_results:
        oss_res_path = OSSStorage.file_upload_from_url(img_result, target_oss_path)['oss_path']
        oss_res_paths.append(oss_res_path)
        recordUserAction(oss_res_path, size_parts[0], size_parts[1], "repaint", user_id)
    print("结束调用sdxl", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return ApiUtils.ok({"oss_res_paths": oss_res_paths, "prompt": prompt})


def getBackgroundPromptByOssPath(oss_path):
    print("开始单独调用gpt4o", datetime.now().strftime("%H:%M:%S"))
    response = gpt4o.get_bg_prompt(OSSStorage.file_sign_oss_path(oss_path))
    prompt = response['choices'][0]['message']['content']
    print("结束单独调用gpt4o", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return ApiUtils.ok({"prompt": prompt})


def genImage(prompt, target_oss_path, steps, scale, size, n, negative_prompt):
    print("开始单独调用sdxl", datetime.now().strftime("%H:%M:%S"))
    img_results = aliyun_conn.aliyun_sdxl(prompt, steps, scale, size, n, negative_prompt)
    oss_res_paths = []
    for img_result in img_results:
        oss_res_path = OSSStorage.file_upload_from_url(img_result.url, target_oss_path)['oss_path']
        oss_res_paths.append(oss_res_path)
    print("结束单独调用sdxl", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return ApiUtils.ok({"oss_res_paths": oss_res_paths})


def genImageReplicate(prompt, target_oss_path, steps, scale, size, n, negative_prompt):
    print("开始单独调用sdxl", datetime.now().strftime("%H:%M:%S"))
    size_parts = size.split('*')
    # img_results = aliyun_conn.aliyun_sdxl(prompt, steps, scale, size, n, negative_prompt)
    img_results = replicate_conn.replicate_sdxl(prompt, steps=steps, scale=scale, w=size_parts[0], h=size_parts[1], n=n,
                                                negative_prompt=negative_prompt)
    print(img_results)
    oss_res_paths = []
    for img_result in img_results:
        oss_res_path = OSSStorage.file_upload_from_url(img_result, target_oss_path)['oss_path']
        oss_res_paths.append(oss_res_path)
    print("结束单独调用sdxl", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return ApiUtils.ok({"oss_res_paths": oss_res_paths})


def newCredentials():
    credentials = Sample.getCredentials()
    print("返回新的sts", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return ApiUtils.ok({"credentials": credentials})


def recordUserAction(ossFilePath, naturalWidth, naturalHeight, operation_type, user_id):
    # 获取hash
    parts = ossFilePath.split('/')
    filename = parts[-1]
    image_hash, extension = os.path.splitext(filename)
    # 处理图片
    image_id = 0
    with mysqlSession() as session:
        new_image = Image(
            oss_path=ossFilePath,
            width=naturalWidth,
            height=naturalHeight,
            uuid=uuid.uuid4(),
            parent_id=0,
            image_source='user',
            state='USER',
            image_hash=image_hash,
            creator_source='wx',
            creator=user_id,
            image_object='USER'
        )
        session.add(new_image)
        session.commit()
        image_id = new_image.id

    # 最终记录
    with mysqlSession() as session:
        new_operation = UserImageOperation(
            user_id=user_id,
            image_id=image_id,
            operation_type=operation_type
        )
        session.add(new_operation)
        session.commit()
    return "ok"


def login(code):
    return user_info_utills.login(code)


def getUserOpenid(token):
    return user_info_utills.get_user_openid(token)
