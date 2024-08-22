import requests
def is_url_accessible(url):
    try:
        response = requests.get(url)
        # 如果状态码是200，表示URL是可访问的
        if response.status_code == 200:
            return True
        else:
            print(response.status_code)
            return False
    except requests.exceptions.RequestException as e:
        print(e)
        # 如果请求过程中出现异常，比如网络问题、DNS解析失败等，返回False
        return False
print (is_url_accessible("https://fwings-prod.oss-cn-beijing.aliyuncs.com/user_images/upload_images/a9786397-a2bd-42fd-bf82-feb49a8b0e69.png?OSSAccessKeyId=STS.NT16yyk2yEYAtFS6Yf28L9YPn&Expires=1720525800&Signature=itxoGYQQqEEYkELsd%2B4oudIAmgU%3D&security-token=CAISvwJ1q6Ft5B2yfSjIr5eEfcPNhu1Y8puqdmDi0lkzPrdg1pz7jDz2IHhMdHZoAu0atfsxn2tR6voSlqF9UZhDWUHCYZOBNUGEEFnzDbDasumZsJYm6vT8a0XxZjf%2F2MjNGZabKPrWZvaqbX3diyZ32sGUXD6%2BXlujQ%2Fbr4NwdGbZxZASjaidcD9p7PxZrrNRgVUHcLvGwKBXn8AGyZQhKwlMk2DovsfrinpfEsECA3APAp7VL99irEP%2BNdNJxOZpzadCx0dFte7DJuCwqsEASpPgu1%2FEYomiZ5YrEXwUB%2BXGBKPGR%2FMdoKhN0YKQq7VbLbHALBZSS082kdOSfo34lVYk92NTOwQkG5oCN3m%2F9gxqF0XJf72iMs7bBf9C%2B2AgvailAHxhBcLECUWRrIkdBJHykbMHulj%2FECo2Tr2jYuMleGoABn7N4QZsxLa%2BskyEi6l9AAYhJ6LIXf4niisbVhHn58VZmdaADbGF%2BVOV9SZE7CMqm%2BYf3idBqD5Z3s54Kc5uS2PW%2FPX9edLqymtmn9TsGRVyjMuyJ%2FzkSF9L8vYXCcs3pndY5prRxALmErTIA2d1AEQs0DIO3zZEtqO1BDrYu1oQgAA%3D%3D"))
