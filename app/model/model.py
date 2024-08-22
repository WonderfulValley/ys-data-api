from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

# 定义Base基类
Base = declarative_base()


class Image(Base):
    """
    图片表
    """
    __tablename__ = 'image'
    id = Column(Integer, autoincrement=True, primary_key=True)  # 通常主键应该明确指定primary_key=True
    uuid = Column(String(50), nullable=False, unique=True)  # 唯一ID
    parent_id = Column(String(50), nullable=False, default='')  # 背景图关联的源图uuid
    image_source = Column(String(20), nullable=False, default='')
    state = Column(String(20), nullable=False, default='')
    oss_path = Column(String(500), nullable=False, default='')  # 本地 OSS 存储路径
    image_hash = Column(String(100), nullable=False, default='')  # 图片 hash 值
    image_object = Column(String(20), nullable=False, default='')  # PIC：成品 BACK：背景 OBJ：主体
    source_url = Column(String(1000), nullable=False, default='')  # 源图 url
    width = Column(Integer, nullable=False, default=0)  # 图片宽度
    height = Column(Integer, nullable=False, default=0)  # 图片高度
    prompt = Column(String(1000), nullable=False, default='')  # 图片的生图提示词
    create_time = Column(DateTime, nullable=False, server_default=func.now())  # 创建时间
    mark_time = Column(DateTime, nullable=True)  # 源图背景是否有价值的标记时间
    resolve_time = Column(DateTime, nullable=True)  # 背景图反解时间
    review_time = Column(DateTime, nullable=True)  # 洗稿图反解结果 review 时间
    creator_source = Column(String(50), nullable=True)
    creator = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<Image(uuid='{self.uuid}', image_source='{self.image_source}', " \
               f"state='{self.state}', oss_path='{self.oss_path}', " \
               f"width={self.width}, height={self.height}, " \
               f"create_time='{self.create_time.isoformat() if self.create_time else None}')>"


class User(Base):
    """
    用户表
    """
    __tablename__ = 'user'
    id = Column(Integer, autoincrement=True, primary_key=True)
    source_content = Column(String(50), nullable=False, unique=True)  # 默认为微信的openid
    source = Column(String(50), nullable=False, default='wx')  # 默认为微信的openid
    create_time = Column(DateTime, nullable=False, server_default=func.now())  # 创建时间
    update_time = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())  # 更新时间，在插入和更新时设置当前时间
    is_deleted = Column(Integer, default=0)  # 预留
    creator_id = Column(String(50), nullable=True)  # 预留
    updater_id = Column(String(50), nullable=True)  # 预留


class UserImageOperation(Base):
    """
    用户对图片的操作表
    """
    __tablename__ = 'user_image_operation'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, nullable=False)
    image_id = Column(Integer, nullable=False)
    operation_type = Column(String(50), nullable=False)  # uploadMain uploadBackground repaint download
    operation_time = Column(DateTime, nullable=False, server_default=func.now())
