# Model Api Server
多个模型工具的http api server

## 文件夹解释
###build
各个工具的启动命令，一般是带参数启动main.py
###docs
文档
###local_logs
本地调试时使用的日志。已gitignore

###app/api
相当于controller，对外暴露接口的所在
###app/modules
承接算法同学准备好的算法
###app/utils
工具类
###app/config.ini
config。可自行复制创建config_local.ini，优先级高于config.ini。已gitignore
config_local.ini 可以增加 [DEAFAULT]local = True 开启本地调试模式
###main.py 
主入口，从这里选择加载启动哪个工具、api