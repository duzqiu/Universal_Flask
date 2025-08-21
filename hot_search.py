# app.py
from flask import Flask, jsonify
from server import MongoDBServer
from flask_cors import CORS 

app = Flask(__name__)
CORS(app) # 允许跨域请求
mongo_server = MongoDBServer()

@app.route('/api/hot_search/list/<int:limit>', methods=['GET']) 
@app.route('/api/hot_search/list', methods=['GET'])
def get_hot_search(limit=10):
    platform_list = [
        "baidu", "toutiao", "dy_hot", "dy_plant","dy_entertain","dy_society","dy_sh"
        ] # 支持的平台列表
    try: 
        result = dict()  # 初始化结果字典
        for platform in platform_list:
            cursor = mongo_server.get_data(platform, limit=limit) # 获取指定平台的数据
            result[platform] = list(cursor) # 将游标转换为列表
        return jsonify({
            "success": True, 
            "count": len(result),
            "data": mongo_server.serialize_doc(result) # 序列化文档
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    print("Flask 服务启动中...")
    print("API 地址: http://localhost:5000/api/hot_search/list")
    app.run(host='0.0.0.0', port=5000, debug=True)
    