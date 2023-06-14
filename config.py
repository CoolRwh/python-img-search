"""
以图搜图配置文件，批量处理
"""
import os
from dotenv import load_dotenv, find_dotenv


#### 加载 .env  到 环境变量
load_dotenv(find_dotenv('.env'))


#### http_server 配置
server_host = os.environ.get('SERVER_HOST', '0.0.0.0')
server_port = os.environ.get("SERVER_PORT",5555)

server_debug = True

if "False" == os.environ.get("SERVER_DEBUG"):
    server_debug = False

print("打开调试模式：",server_debug)


FILE_DIR = os.path.dirname(os.path.realpath(__file__))
save_path = os.path.join(FILE_DIR, 'static', 'uploaded')

# 要提取特征图片库的地址，示例：'F:/ACG/出处归档/*'
train_pic_path = r"E:\www\yzh\towhee-img-search\static\uploaded\pen\*"

types = [".jpg", ".jpeg", ".gif", ".png", ".JPG", ".JPEG", ".GIF", ".PNG"]


upload_type =["jpg", "jpeg", "gif", "png", "JPG", "JPEG", "GIF", "PNG"]


upload_path= 'static/uploaded/'

# elasticsearch
elasticsearch_index = "imgsearch"  # 索引名，示例 imgsearch
elastic_url = os.environ.get('ELASTIC_SEARCH_URL',"http://elastic:123456@127.0.0.1:9200")


folder = ''  # bucket下的文件夹名，示例：'test/'
pic_oss_url = "" + folder  # oss存储地址前缀，示例："https://{bucket名称}.oss-cn-hangzhou.aliyuncs.com/" + folder



