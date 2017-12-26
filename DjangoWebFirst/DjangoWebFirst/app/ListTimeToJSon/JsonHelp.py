import json
from datetime import datetime
import random

"""Json 序列化 时间帮助"""
class DateEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, datetime):  
            return obj.strftime('%Y-%m-%d %H:%M:%S') 
        else:  
            return json.JSONEncoder.default(self, obj) 

class RandomPass():
    def default(self,num):
        s = []
        while(len(s) < num):
            x = random.randint(0,9)
            if x not in s:
                s.append(x)
        back=[str(i) for i in s]
        return ''.join(back)

