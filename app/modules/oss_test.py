from storage import OSSStorage
import os

OSSStorage = OSSStorage(access_key=os.environ.get("ALI_ACCESS_KEY_ID1") + os.environ.get("ALI_ACCESS_KEY_ID2"),
                        secret_key=os.environ.get("ALI_ACCESS_KEY_SECRET1") + os.environ.get("ALI_ACCESS_KEY_SECRET2"),
                        endpoint="oss-cn-beijing.aliyuncs.com",
                        bucket='fwings-prod')


print(OSSStorage.file_sign_oss_url('user_images/test/32d95806f25a44ab99ee3c1cb08b8e29b0fb891e4105c8797e40cdbbcf8178fc.png'))
# print(OSSStorage.file_upload_from_url(url='https://fwings-prod.oss-cn-beijing.aliyuncs.com/exampleobject.png?Expires=1718120814&OSSAccessKeyId=TMP.3Kgix7rWqWjnypzXE1qpyPmnc2NmMQ7PGptFknYccMAya4NjR5VwWPMzGtzQ3De8meeb9DQWUziGUdRDRbdrCx7jwc5eSx&Signature=xSPjizZsExmHyfPjfPDcoNRsZuk%3D',file_prefix='user_images/test'))