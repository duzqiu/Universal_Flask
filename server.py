from pymongo import DESCENDING, MongoClient
from bson import ObjectId
from datetime import datetime

class MongoDBServer:
    def __init__(self):
        self.mongo_url = "mongodb://admin:123456@duzqiu.top:27017/"

    def _get_mongo_client(self): # 连接mongo数据库
        try:
            client = MongoClient(self.mongo_url)
            return client # 返回连接的客户端
        except:
            raise ConnectionError("无法连接到mongodb数据库") # 连接失败抛出异常
        
    def _get_mongo_coll(self, db, coll): # 获取mongo指定集合
        client = self._get_mongo_client()
        if client:
            db = client[db] # 使用指定的数据库
            collection = db[coll] # 使用指定的集合
            return collection # 返回集合对象
        else:
            raise ConnectionError("无法连接到mongodb集合") # 获取集合失败抛出异常
        
    def get_data(self, platform, db="news_hot_list", coll="news_hot", limit=10): # 获取指定平台的最新数据
        collection = self._get_mongo_coll(db, coll) # 获取集合对象
        data_platform = collection.find({"platform": platform}) # 查询指定平台的数据
        if data_platform: # 如果查询结果不为空
            data = data_platform.sort([("created_at", DESCENDING)]).limit(limit) # 按照创建时间降序排序并限制数量
        else:
            data = None
        return data
    
    def serialize_doc(self, doc):
        """将 MongoDB 文档中的 ObjectId 转为字符串"""
        if isinstance(doc, list): # 如果是列表
            return [self.serialize_doc(item) for item in doc]
        elif isinstance(doc, dict): # 如果是字典
            return {k: self.serialize_doc(v) for k, v in doc.items()}
        elif isinstance(doc, ObjectId): # 如果是 ObjectId
            return str(doc)
        elif isinstance(doc, datetime): # 如果是 datetime
            return doc.isoformat()
        else: # 其他类型直接返回
            return doc
    
if __name__ == "__main__":
    data = MongoDBServer().get_data("baidu")

    for i in data:
        print(f"Document: {i}")    