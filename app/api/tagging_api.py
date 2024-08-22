from app.modules.storage import OSSStorage
from app.utils.apiUtils import ApiUtils
from datetime import datetime
import os
from app.model.tagging_model import XhsCreator
from app.utils.mysql_utils import mysqlSession
import uuid


OSSStorage = OSSStorage(access_key=os.environ.get("ALI_ACCESS_KEY_ID1") + os.environ.get("ALI_ACCESS_KEY_ID2"),
                        secret_key=os.environ.get("ALI_ACCESS_KEY_SECRET1") + os.environ.get("ALI_ACCESS_KEY_SECRET2"),
                        endpoint="oss-cn-beijing.aliyuncs.com",
                        bucket='fwings-prod')
def getCreatorList():
    session = mysqlSession()
    creators = session.query(XhsCreator).all()
    for creator in creators:
        print(f"ID: {creator.id}, User ID: {creator.user_id}, Nickname: {creator.nickname}")


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
