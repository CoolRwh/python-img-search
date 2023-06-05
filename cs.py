import os
import time
import urllib
from glob import glob
from elasticsearch import Elasticsearch
from towhee.dc2 import pipe, ops
import config
import image_decode_custom


'''
提取图片特征向量上传es
'''

cnt = 0  # 图片处理计数


es = Elasticsearch(config.elastic_url)
image_decode = image_decode_custom.ImageDecodeCV2()
image_embedding = ops.image_embedding.timm(model_name='resnet50')

# Load image path
def load_image(folderPath):
    for filePath in glob(folderPath):
        if os.path.splitext(filePath)[1] in config.types:
            yield filePath


# 生成对应图片向量，存储到es
def es_insert(filePath, vec):
    vec = vec[::2]  # 特征向量，resnet50提取的图片向量维度是2048，es7.4版本支持的最大维度是1024
    fileName = os.path.basename(filePath)  # 图片名称
    imgUrl = config.pic_oss_url + urllib.parse.quote(fileName)  # OSS地址
    doc = {'url': imgUrl, 'feature': vec,'name': fileName}
    es.index(index=config.elasticsearch_index, body=doc)  # 保存到elasticsearch

    global cnt
    cnt += 1
    print("当前图片：" + fileName + " ---> " + str(cnt))

def extract(galleryPath):
    for path in glob(galleryPath):
        if os.path.splitext(path)[1] not in config.types:
            continue
        img = image_decode(path)
        vec = image_embedding(img)
        es_insert(path, vec)


if __name__ == '__main__':
    start_time = time.time()
    # extract(config.train_pic_path)
    # path = "https://pic.yzhfuture.com/ecloud/ef439713-9979-1b7f-b432-577b05801c1f/pic/commodity/main1238801654571622.jpg"
    # ileName = os.path.basename(path)  # 图片名称
    
    # img = image_decode(path)
    
  
    print(config.url)
  
    # vec = image_embedding(img)
    # print(vec[::2])
    end_time = time.time()
    
    
    fileName = time.time()
    print(round(fileName * 10000))
    

    
    total_time = end_time - start_time
    print("程序运行时间为：", total_time, "秒")
