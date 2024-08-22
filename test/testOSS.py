from app.modules.storage import OSSStorage

OSSStorage = OSSStorage(access_key="LTAI5t9vhJGhFv" + "4cc3EHdQRe",
                        secret_key="nVgqbMnVoIsTOtoVb" + "Jk130VPkJRrJ6",
                        endpoint="oss-cn-beijing.aliyuncs.com",
                        bucket='fwings-prod')


new_oss_path ="https://fwings-prod.oss-cn-beijing.aliyuncs.com/user_images/upload_images/1fe06d4c-1512-4694-b554-1d9e487d837f.png?OSSAccessKeyId=STS.NTBG8PGiwDGrvNeob61VGo3MY&Expires=1720603129&Signature=H7ibVxPCCvs4qp1uUP5Za7wkAhc%3D&security-token=CAISvwJ1q6Ft5B2yfSjIr5f3DILkqrZW84WZdGjUi2JjPdlrgPbmuzz2IHhMdHZoAu0atfsxn2tR6voSlqF9UZhDWUHCYZPCC1LfEFnzDbDasumZsJYm6vT8a0XxZjf%2F2MjNGZabKPrWZvaqbX3diyZ32sGUXD6%2BXlujQ%2Fbr4NwdGbZxZASjaidcD9p7PxZrrNRgVUHcLvGwKBXn8AGyZQhKwlMk2DovsfrinpfEsECA3APAp7VL99irEP%2BNdNJxOZpzadCx0dFte7DJuCwqsEASpPgu1%2FEYomiZ5YrEXwUB%2BXGBKPGR%2FMdoKhN0YKQq7VbLbHALBZSS082kdOSfo34lVYk92PQCzTp15oCN3m%2F9gxqF0XJf72iMs7bBf9C%2B2AgvailAHxhBcLECUWRrIkdBJHykbMHulj%2FECr8wYwzYuMleGoABQr0bhXDxXu5Q41fSmk948uiE%2BNEnr6YLbNvxxmi%2BYV8Gn5v4llO8hvWtpIvtQoVziMLuQZEJ2%2Bmw4ziDU3C59mpd5%2FMo%2FnBK%2FYHCo0SXIrC3Ua4A%2FpuaRW2Bzgu4RzZhgiI3j3GFExf1ldYVjPTu29Bb9L6Yp1j0YzmJmNkDymUgAA%3D%3D"
params = dict()
params['x-oss-process'] = "image/format,webp"
print(4,new_oss_path)
url = OSSStorage.file_sign_oss_path(new_oss_path)
print(url)