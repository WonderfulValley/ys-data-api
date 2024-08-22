from app.model.model import UserImageOperation
from app.utils.mysql_utils import mysqlSession, engine, Base
from app.model.model import Image
from app.model.model import User

# def get_images():
#     with SessionLocal() as db:  # 使用 with 语句确保会话在使用后关闭
#         images = db.query(Image).limit(10).all()
#         return images


# images = get_images()
# for image in images:
#     print(image.id, image.uuid, image.image_source)  # 打印图片信息
#
# tables = Base.metadata.tables
# print(tables[UserImageOperation.__tablename__].create(bind=engine))

with mysqlSession() as session:
    new_operation = UserImageOperation(
        user_id=1,  # 假设用户ID为1
        image_id=2,  # 假设图片ID为2
        operation_type='uploadMain',  # 操作类型
    )
    session.add(new_operation)
    session.commit()
    print(new_operation.id)

# for table_name, table in tables.items():
#     print(table.create(engine))