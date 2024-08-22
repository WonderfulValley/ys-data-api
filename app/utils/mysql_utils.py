# app/database.py  
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model.model import Base  # 假设 Base 是你的模型基类  

# 数据库连接设置  
DATABASE_URL = 'mysql+pymysql://image_service:k$cF8_0Kcb@rm-uf6528279hy6f7so3zo.mysql.rds.aliyuncs.com:3306/fwings?charset=utf8mb4'

# 创建 SQLAlchemy 引擎  
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

# 创建会话工厂  
mysqlSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)