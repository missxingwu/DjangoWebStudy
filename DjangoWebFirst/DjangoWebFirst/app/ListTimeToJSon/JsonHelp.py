import json
from datetime import datetime

"""Json 序列化 时间帮助"""
class DateEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S') 
        else:  
            return json.JSONEncoder.default(self, obj) 
