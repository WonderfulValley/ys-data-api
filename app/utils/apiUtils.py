class ApiUtils:
    @staticmethod
    def to_dict(status: int, data: dict = None, message: str = ""):
        """将状态、数据和消息转换为字典，方便转换为JSON"""
        return {
            "status": status,
            "data": data if data is not None else {},
            "message": message
        }

    @staticmethod
    def to_json(status: int, data: dict = None, message: str = ""):
        """将状态、数据和消息转换为JSON字符串"""
        import json
        return json.dumps(ApiUtils.to_dict(status, data, message))

    @staticmethod
    def ok(data: dict = None, status: int = 200, message: str = "ok"):
        """创建成功的API响应"""
        return ApiUtils.to_dict(status, data, message)

    @staticmethod
    def err(data: dict = None, status: int = 401, message: str = "服务端错误"):
        """创建错误的API响应"""
        return ApiUtils.to_dict(status, data, message)