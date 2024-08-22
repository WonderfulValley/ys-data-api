import base64
import requests

# 填Key
aa = "sk-5hsEXPEOUl"
aa = aa + "oLypArXsRhT3BlbkFJDQ0shgBKhufWbx63KARW"


def get_bg_prompt(img_url):
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
                            "url": f"{img_url}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://func-hgee-eiajxuqvru.ap-southeast-1.fcapp.run", headers=headers, json=payload)
    return response.json()

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
    response = requests.post("https://func-hgee-eiajxuqvru.ap-southeast-1.fcapp.run", headers=headers, json=payload)
    return response.json()

#
# def get_bg_prompt(base64_image):
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {aa}"
#     }
#
#     payload = {
#         "model": "gpt-4o",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text",
#                         "text": "请用200个英文单词描述这张图片的背景，忽略所有图片上的文字和前景主体，以便在stable diffusion的文生图中复现该图片的背景"
#                     },
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/jpeg;base64,{base64_image}"
#                         }
#                     }
#                 ]
#             }
#         ],
#         "max_tokens": 300
#     }
#
#     response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
#
#     return response.json()
