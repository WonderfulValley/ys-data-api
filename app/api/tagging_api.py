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

def getNodeList():
    session = mysqlSession()
    user_id = "53f9ce73b4c4d6062982ff8a"
    # 作者所有的文章
    notes = session.query(XhsNote,
                          session.query(func.count(XhsImage.id)).
                          filter(XhsImage.note_id == XhsNote.note_id).
                          scalar_subquery().label('image_count'),
                          session.query(func.count(XhsImageTagging.user_id)).
                          filter(XhsImageTagging.note_id == XhsNote.note_id).
                          scalar_subquery().label('tagged_image_count'), ).filter(XhsNote.user_id == user_id).all()
    # creator = session.query(XhsCreator).filter(XhsCreator.user_id == user_id).all()
    # creator_tag = session.query(XhsCreatorTagging).filter(XhsCreatorTagging.user_id == user_id).all()
    for note, image_count, tagged_image_count in notes:
        print(
            f"ID: {note.id},note_id: {note.note_id},image_count: {image_count},tagged_image_count: {tagged_image_count}")

def getImageList():
    session = mysqlSession()
    user_id = "56577a2282718c0a974d261d"
    note_id = "5a4cf388fb2a365983d9ee02"
    images_with_tags_query = session.query(XhsImage, XhsImageTagging).join(
        XhsImageTagging,
        XhsImage.file_url == XhsImageTagging.file_path
    ).filter(
        XhsImage.note_id == note_id,
        XhsImageTagging.note_id == note_id
    ).all()

    for img, tagging in images_with_tags_query:
        print(f"Image ID: {img.id}, File Path: {img.file_url}")
        print(f"  XhsImageTagging ID: {tagging.id}")

def getCrawlerTrend():
