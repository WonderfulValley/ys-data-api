
from sqlalchemy import Column, Integer, String, Text, BigInteger, func, DateTime, Float, Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()


class XhsCreator(Base):
    __tablename__ = 'xhs_creator'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增ID')
    user_id = Column(String(64), nullable=False, comment='用户ID')
    nickname = Column(String(64), comment='用户昵称')
    avatar = Column(String(255), comment='用户头像地址')
    ip_location = Column(String(255), comment='评论时的IP地址')
    add_ts = Column(BigInteger, nullable=False, server_default=func.current_timestamp(), comment='记录添加时间戳')
    last_modify_ts = Column(BigInteger, nullable=False, default=func.current_timestamp(), comment='记录最后修改时间戳')
    desc = Column(Text, comment='用户描述')
    gender = Column(String(1), comment='性别')
    follows = Column(String(16), comment='关注数')
    fans = Column(String(16), comment='粉丝数')
    interaction = Column(String(16), comment='获赞和收藏数')
    tag_list = Column(Text, comment='标签列表')


class XhsCreatorTagging(Base):
    __tablename__ = 'xhs_creator_tagging'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(100))
    height = Column(Float, comment='身高')
    weight = Column(Float, comment='体重')
    age = Column(Integer, comment='年龄')
    hair = Column(String(255), comment='发型')
    shape = Column(String(255), comment='体型')
    style = Column(String(500), comment='风格，逗号分隔')
    scene = Column(String(500), comment='场景，逗号分隔')
    add_ts = Column(DateTime, server_default=func.now(), comment='记录添加时间')
    last_modify_ts = Column(DateTime, server_onupdate=func.now(), nullable=False, onupdate=func.now(), comment='记录最后修改时间')


class XhsCreatorTaggingChai(Base):
    __tablename__ = 'xhs_creator_tagging_chai'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(100))
    height = Column(Float, comment='身高')
    weight = Column(Float, comment='体重')
    age = Column(Integer, comment='年龄')
    hair = Column(String(255), comment='发型')
    shape = Column(String(255), comment='体型')
    style = Column(String(500), comment='风格，逗号分隔')
    scene = Column(String(500), comment='场景，逗号分隔')
    add_ts = Column(DateTime, default=func.now(), comment='记录添加时间')
    last_modify_ts = Column(DateTime, default=func.now(), onupdate=func.now(), comment='记录最后修改时间')


class XhsCreatorTaggingGpt(Base):
    __tablename__ = 'xhs_creator_tagging_gpt'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(100))
    height = Column(Float, comment='身高')
    weight = Column(Float, comment='体重')
    age = Column(Integer, comment='年龄')
    hair = Column(String(255), comment='发型')
    shape = Column(String(255), comment='体型')
    style = Column(String(500), comment='风格，逗号分隔')
    scene = Column(String(500), comment='场景，逗号分隔')
    add_ts = Column(DateTime, server_default='CURRENT_TIMESTAMP', comment='记录添加时间')
    last_modify_ts = Column(DateTime, server_default='CURRENT_TIMESTAMP', onupdate='CURRENT_TIMESTAMP',
                            comment='记录最后修改时间')

class XhsImage(Base):
    __tablename__ = 'xhs_image'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='自增ID')
    final_img_url = Column(String(255), comment='线上地址')
    file_url = Column(String(255), comment='存储位置')
    user_id = Column(String(64), nullable=False, comment='用户ID')
    nickname = Column(String(64), comment='用户昵称')
    avatar = Column(String(255), comment='用户头像地址')
    ip_location = Column(String(255), comment='评论时的IP地址')
    add_ts = Column(BigInteger, nullable=False, comment='记录添加时间戳')
    last_modify_ts = Column(BigInteger, nullable=False, comment='记录最后修改时间戳')
    note_id = Column(String(64), nullable=False, comment='笔记ID')
    type = Column(String(16), comment='笔记类型(normal | video)')
    title = Column(String(255), comment='笔记标题')
    desc = Column(String,comment='笔记描述')
    video_url = Column(String, comment='视频地址')
    time = Column(BigInteger, nullable=False, comment='笔记发布时间戳')
    last_update_time = Column(BigInteger, nullable=False, comment='笔记最后更新时间戳')
    liked_count = Column(String(16), comment='笔记点赞数')
    collected_count = Column(String(16), comment='笔记收藏数')
    comment_count = Column(String(16), comment='笔记评论数')
    share_count = Column(String(16), comment='笔记分享数')
    image_list = Column(String, comment='笔记封面图片列表')
    tag_list = Column(String, comment='标签列表')
    note_url = Column(String(255), comment='笔记详情页的URL')


class XhsImageTagging(Base):
    __tablename__ = 'xhs_image_tagging'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(500), comment='小红书地址')
    file_path = Column(String(500), comment='文件存储位置')
    height = Column(Double, comment='身高')
    weight = Column(Double, comment='体重')
    age = Column(Integer, comment='年龄')
    hair = Column(String(255), comment='发型')
    shape = Column(String(255), comment='体型')
    style = Column(String(500), comment='风格，逗号分隔')
    scene = Column(String(500), comment='场景，逗号分隔')
    add_ts = Column(DateTime, default=func.now(), comment='记录添加时间')
    last_modify_ts = Column(DateTime, default=func.now(), onupdate=func.now(), comment='记录最后修改时间')


class XhsImageTaggingChai(Base):
    __tablename__ = 'xhs_image_tagging_chai'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(500), comment='小红书地址')
    file_path = Column(String(500), comment='文件存储位置')
    height = Column(Double, comment='身高')
    weight = Column(Double, comment='体重')
    age = Column(Integer, comment='年龄')
    hair = Column(String(255), comment='发型')
    shape = Column(String(255), comment='体型')
    style = Column(String(500), comment='风格，逗号分隔')
    scene = Column(String(500), comment='场景，逗号分隔')
    add_ts = Column(DateTime, default=func.now(), comment='记录添加时间')
    last_modify_ts = Column(DateTime, default=func.now(), onupdate=func.now(), comment='记录最后修改时间')


class XhsImageTaggingGpt(Base):
    __tablename__ = 'xhs_image_tagging_gpt'

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(500), comment='小红书地址')
    file_path = Column(String(500), comment='文件存储位置')
    height = Column(Double, comment='身高')
    weight = Column(Double, comment='体重')
    age = Column(Integer, comment='年龄')
    hair = Column(String(255), comment='发型')
    shape = Column(String(255), comment='体型')
    style = Column(String(500), comment='风格，逗号分隔')
    scene = Column(String(500), comment='场景，逗号分隔')
    add_ts = Column(DateTime, default=func.now(), comment='记录添加时间')
    last_modify_ts = Column(DateTime, default=func.now(), onupdate=func.now(), comment='记录最后修改时间')


class XhsNote(Base):
    __tablename__ = 'xhs_note'

    id = Column(Integer, primary_key=True, comment='自增ID')
    user_id = Column(String(64), nullable=False, comment='用户ID')
    nickname = Column(String(64), comment='用户昵称')
    avatar = Column(String(255), comment='用户头像地址')
    ip_location = Column(String(255), comment='评论时的IP地址')
    add_ts = Column(BigInteger, nullable=False, comment='记录添加时间戳')
    last_modify_ts = Column(BigInteger, nullable=False, comment='记录最后修改时间戳')
    note_id = Column(String(64), nullable=False, comment='笔记ID')
    type = Column(String(16), comment='笔记类型(normal | video)')
    title = Column(String(255), comment='笔记标题')
    desc = Column(Text, comment='笔记描述')
    video_url = Column(Text, comment='视频地址')
    time = Column(BigInteger, nullable=False, comment='笔记发布时间戳')
    last_update_time = Column(BigInteger, nullable=False, comment='笔记最后更新时间戳')
    liked_count = Column(String(16), comment='笔记点赞数')
    collected_count = Column(String(16), comment='笔记收藏数')
    comment_count = Column(String(16), comment='笔记评论数')
    share_count = Column(String(16), comment='笔记分享数')
    image_list = Column(Text, comment='笔记封面图片列表')
    tag_list = Column(Text, comment='标签列表')
    note_url = Column(String(255), comment='笔记详情页的URL')


class XhsNoteComment(Base):
    __tablename__ = 'xhs_note_comment'

    id = Column(Integer, primary_key=True, comment='自增ID')
    user_id = Column(String(64), nullable=False, comment='用户ID')
    nickname = Column(String(64), comment='用户昵称')
    avatar = Column(String(255), comment='用户头像地址')
    ip_location = Column(String(255), comment='评论时的IP地址')
    add_ts = Column(BigInteger, nullable=False, comment='记录添加时间戳')
    last_modify_ts = Column(BigInteger, nullable=False, comment='记录最后修改时间戳')
    comment_id = Column(String(64), nullable=False, comment='评论ID')
    create_time = Column(BigInteger, nullable=False, comment='评论时间戳')
    note_id = Column(String(64), nullable=False, comment='笔记ID')
    content = Column(Text, nullable=False, comment='评论内容')
    sub_comment_count = Column(Integer, nullable=False, comment='子评论数量')
    pictures = Column(String(512), comment='图片列表')
    parent_comment_id = Column(String(64), comment='父评论ID')





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
