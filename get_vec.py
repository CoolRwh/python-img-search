# -*- coding: utf-8 -*-
from PIL import Image
# from towhee.dc2 import pipe, ops, DataCollection

from towhee import pipe, ops, DataCollection
# import image_decode_custom
import numpy as np

import torch
import timm

'''
    以图搜图服务
'''

# backbone = timm.create_model('resnet50', pretrained=False, num_classes=500, in_chans=13)
# # out = backbone()

# model_names = timm.list_models(pretrained=True)
# print("支持的预训练模型数量：%s"%len(model_names))
# strs='*resne*t*'
# model_names = timm.list_models(strs)
# print("通过通配符 %s 查询到的可用模型：%s"%(strs,len(model_names)))
# model_names = timm.list_models(strs,pretrained=True)
# print("通过通配符 %s 查询到的可用预训练模型：%s"%(strs,len(model_names)))


# model = ops.image_embedding.timm(model_name='resnet50')
# model = ops.image_embedding.timm(model_name='resnet101')
model = ops.image_embedding.timm(model_name='resnet152')

# loc(float)：此概率分布的均值（对应着整个分布的中心centre
# scale(float)：此概率分布的标准差（对应于分布的宽度，scale越大，图形越矮胖；scale越小，图形越瘦高）
# size(int or tuple of ints)：输出的shape，默认为None，只输出一个值
projection_matrix = np.random.normal(scale=1.0, size=(2048,512))

def dim_reduce(vec):
    return np.dot(vec, projection_matrix)


img_url = r'./static/uploaded/pic/111/16921707896593.jpg'
img = Image.open(img_url)
# vec = model(img)
# print(len(vec))
# print(vec)


vec = model(img)
print(vec)