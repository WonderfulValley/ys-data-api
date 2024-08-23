from app.modules.storage import OSSStorage
from app.utils.apiUtils import ApiUtils
from datetime import datetime
import os
from app.model.tagging_model import XhsCreator
from app.utils.mysql_utils import mysqlSession
import uuid
from pathlib import Path
from sqlalchemy import select, func, join
from app.model.tagging_model import XhsCreator, XhsCreatorTagging, XhsNote, XhsImage, XhsImageTagging

OSSStorage = OSSStorage(access_key=os.environ.get("ALI_ACCESS_KEY_ID1") + os.environ.get("ALI_ACCESS_KEY_ID2"),
                        secret_key=os.environ.get("ALI_ACCESS_KEY_SECRET1") + os.environ.get("ALI_ACCESS_KEY_SECRET2"),
                        endpoint="oss-cn-beijing.aliyuncs.com",
                        bucket='fwings-prod')
def getCreatorList():
    # print(os.getcwd())
    directory_path = Path('docs/xhs/images')
    # 当前可以进行标注的用户。有图片的用户。一般是看docs/xhs/images里面的文件
    current_user_id = [creator.name for creator in directory_path.iterdir() if creator.is_dir()]
    session = mysqlSession()
    # 已标注的作者
    tagged_creators = session.query(XhsCreatorTagging.user_id).filter(
        XhsCreatorTagging.user_id.in_(current_user_id)).subquery().select()

    # 已标注的作者信息
    query = session.query(
        XhsCreator,
        session.query(func.count(XhsNote.id)).
            filter(XhsNote.user_id == XhsCreator.user_id).
            scalar_subquery().label('note_count'),
        session.query(func.count(XhsImage.id)).
            filter(XhsImage.user_id == XhsCreator.user_id).
            scalar_subquery().label('image_count'),
        session.query(func.count(XhsImageTagging.user_id)).
            filter(XhsImageTagging.user_id == XhsCreator.user_id).
            scalar_subquery().label('tagged_image_count'),
    ).filter(
        XhsCreator.user_id.in_(tagged_creators)  # 假设 tagged_creators 是用户ID列表
    )
    creators = query.all()
    print("已标注")
    for creator, note_count, image_count, tagged_image_count in creators:
        print(
            f"ID: {creator.id}, User ID: {creator.user_id}, Nickname: {creator.nickname}, note_count: {note_count}, image_count:{image_count}, tagged_image_count:{tagged_image_count}")

    # 未标注的作者信息
    query = query = session.query(
        XhsCreator,
        session.query(func.count(XhsNote.id)).
            filter(XhsNote.user_id == XhsCreator.user_id).
            scalar_subquery().label('note_count'),
        session.query(func.count(XhsImage.id)).
            filter(XhsImage.user_id == XhsCreator.user_id).
            scalar_subquery().label('image_count'),
        session.query(func.count(XhsImageTagging.user_id)).
            filter(XhsImageTagging.user_id == XhsCreator.user_id).
            scalar_subquery().label('tagged_image_count'),
    ).filter(~XhsCreator.user_id.in_(tagged_creators)).filter(XhsCreator.user_id.in_(current_user_id))
    creators = query.all()
    print("未标注")
    for creator, note_count, image_count, tagged_image_count in creators:
        print(
            f"ID: {creator.id}, User ID: {creator.user_id}, Nickname: {creator.nickname}, note_count: {note_count}, image_count:{image_count}, tagged_image_count:{tagged_image_count}")


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
