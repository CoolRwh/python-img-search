# -*- coding: utf-8 -*-
import os
import urllib
from glob import glob

from PIL import Image
from elasticsearch import Elasticsearch
# -*- coding: utf-8 -*-
import config
from towhee.dc2 import pipe, ops, DataCollection
from flask import Flask, request, render_template,jsonify
import image_decode_custom

import time

'''
    以图搜图服务
'''

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploaded/goods/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 限制上传文件大小为 16MB


es = Elasticsearch(config.elastic_url)
image_decode_custom = image_decode_custom.ImageDecodeCV2()
last_upload_img = ""


image_embedding = ops.image_embedding.timm(model_name='resnet50')


# es查询
def feature_search(query,min_score=1.6):
    global es
    # print(query)
    bodydata = {
            "size": 30,
            "min_score":min_score,
            "query": {
                "script_score": {
                    "query": {
                        "match_all": {}
                    },
                    "script": {
                        "source": "cosineSimilarity(params.queryVector, doc['feature'])+1.0",
                        "params": {
                            "queryVector": query
                        }
                    }
                }
            }
        }
    results = es.search(index=config.elasticsearch_index,body=bodydata)
    hitCount = results['hits']['total']['value']
    print("hitCount",hitCount)
    if hitCount > 0:
        answers = []
        max_score = results['hits']['max_score']

        if max_score >= 0.35:
            for hit in results['hits']['hits']:
                if hit['_score'] > 0.5 * max_score:
                    imgurl = hit['_source']['url']
                    name = hit['_source']['name']
                    imgurl = imgurl.replace("#", "%23")
                    imgurl = "/static/uploaded/goods/" + str(imgurl)
                    answers.append([imgurl, name])
    else:
        answers = []
    return answers

def error(data = {},msg="error!",code=422):
    return jsonify({"success":False,"code":code,"msg":msg,"data":data})

def success(data = {},msg="success!",code=200):
    return jsonify({"success":True,"code":code,"msg":msg,"data":data})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# 图片 url 转换 成为 Vec 向量
def urlToVec(url):
    img = image_decode_custom(url)
    vec = image_embedding(img)
    return vec


def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False




#######################################################################################################################################
### api v1
# 搜索图片
@app.route('/api/v1/search', methods=['POST'])
def api_v1_search():
    global es
    try:
        file = request.files['query_img']
        if 'query_img' not in request.files or not bool(request.files.get('query_img')):
            raise ValueError("请上传图片")
            if file.filename == '':
                 raise ValueError("文件名称不能为空")
            if not allowed_file(file.filename):
                raise ValueError("文件类型异常")
            
                    # Save query image
        img = Image.open(file.stream)  # PIL image
            # print(file.filename)            
        uploaded_img_path = "static/uploaded/" + file.filename
        img.save(uploaded_img_path)
        vec = urlToVec(uploaded_img_path)
        data = {}
        # data['vec'] = vec.tolist()
        bodydata = {
                    "_source":["_id","name","url"],
                    "size": 30,
                    "min_score": 1.6,
                    "query": {
                        "script_score": {
                            "query": {
                                "match_all": {}
                            },
                            "script": {
                                "source": "cosineSimilarity(params.queryVector, doc['feature'])+1.0",
                                "params": {
                                    "queryVector": vec
                                }
                            }
                        }
                    }
                }
        results = es.search(index=config.elasticsearch_index,body=bodydata)
        data['total'] = results['hits']['total']['value']
        data['list']  = results['hits']['hits']
        return success(data)
    except Exception as e:
        return error([],e.args[0])


### url 转换 向量 api 接口
@app.route('/api/v1/img_vec', methods=['GET'])
def api_v1_imsg_vec():
    try:
        path = request.values.get('url')
        if None == path or path == "":
            raise ValueError("图片地址不能为空！")
        
        check1 = is_contains_chinese(path)
        
        if is_contains_chinese == True :
            img = Image.open(path)
            format = img.format
            if format not in config.upload_type :
                raise ValueError("文件格式不支持上传！")
            
            path = ''
            file_name = str(round(time.time() * 10000)) + "." + format
            uploaded_img_path = config.upload_path + file_name
            #####################################
            img.save(uploaded_img_path)
            path = uploaded_img_path
        
        vec = urlToVec(path).tolist()
        return success(vec)
    except Exception as e:
        return error([],e.args[0])


### 上传图片 转换 向量 api 接口
@app.route('/api/v1/getVecByImgFile', methods=['POST'])
def api_v1_upload_img_to_vec():
    try:
        vec_size = request.form.get("vec_size","2048")
        if vec_size  not in ["1024","2048"]:
            raise ValueError("vec 大小异常！") 
        
        file = request.files['query_img']
        if 'query_img' not in request.files or not bool(request.files.get('query_img')):
            raise ValueError("请上传图片")
            if file.filename == '':
                 raise ValueError("文件名称不能为空")
            if not allowed_file(file.filename):
                raise ValueError("文件类型异常")
        
        img = Image.open(file.stream)
        format = img.format
        if format not in config.upload_type :
            raise ValueError("文件格式不支持上传！")
        
   
        file_name = str(round(time.time() * 10000)) + "." + format

        uploaded_img_path = config.upload_path + file_name
        #####################################
        img.save(uploaded_img_path)
        ##################################### 
        vec = urlToVec(uploaded_img_path)

        if "1024" == vec_size:
            vec = vec[::2].tolist()
        else:
            vec = vec.tolist()  
            
        return success(vec)
    except Exception as e:
        return error([],e.args[0])



#######################################################################################################################################
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# # 搜索图片
# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         file = request.files['query_img']

#         # Save query image
#         img = Image.open(file.stream)  # PIL image
#         # print(file.filename)
#         uploaded_img_path = "static/uploaded/" + file.filename
#         # print(uploaded_img_path)
#         img.save(uploaded_img_path)

#         # Run search
#         dc = p_search(uploaded_img_path)
#         # 得到查询结果
#         answers = dc.get()[0]

#         # 删除上一次上传的图片
#         global last_upload_img
        
#         # print(last_upload_img)
        
#         if last_upload_img is not None and len(last_upload_img) != 0:
#             if os.path.exists(last_upload_img):
#                 os.remove(last_upload_img)
#             else:
#                 print('删除上一次上传图片失败:', last_upload_img)

#         last_upload_img = config.FILE_DIR + '/' + uploaded_img_path

#         return render_template('index.html',
#                                query_path=urllib.parse.quote(uploaded_img_path),
#                                scores=answers)
#     else:
#         return render_template('index.html')


# # 搜索图片
# @app.route('/addimg', methods=['GET', 'POST'])
# def addimg():
#     if request.method == 'POST':
#         file = request.files['query_img']

#         # Save query image
#         img = Image.open(file.stream)  # PIL image
#         # print(file.filename)
#         uploaded_img_path = "static/uploaded/" + file.filename
#         # print(uploaded_img_path)
#         img.save(uploaded_img_path)
#         #############################################################################################
#         ############ 上传图片到 es 
#         uploaded_img_path2 = "static/uploaded/goods/" + file.filename
#         img.save(uploaded_img_path2)
#         fileName = file.filename
#         imgUrl = file.filename
#         img = image_decode_custom(uploaded_img_path2)
#         vec = image_embedding(img)
#         doc = {'url': imgUrl, 'feature': vec,'name': fileName}
#         es.index(index=config.elasticsearch_index, body=doc)  # 保存到
#         print("当前图片：" + fileName + " ---> ")
#         #############################################################################################
#         # 删除上一次上传的图片
#         global last_upload_img
      
#         if last_upload_img is not None and len(last_upload_img) != 0:
#             if os.path.exists(last_upload_img):
#                 os.remove(last_upload_img)
#             else:
#                 print('删除上一次上传图片失败:', last_upload_img)

#         last_upload_img = config.FILE_DIR + '/' + uploaded_img_path

#         return render_template('add_img.html',
#                                query_path=urllib.parse.quote(uploaded_img_path))
#     else:
#         return render_template('add_img.html')


# # Load image path
# def load_image(folderPath):
#     for filePath in glob(folderPath):
#         if os.path.splitext(filePath)[1] in config.types:
#             yield filePath


# # Embedding pipeline
# p_embed = (
#     pipe.input('src')
#     # 传入src，输出img_path
#     .flat_map('src', 'img_path', load_image)
#     # 传入img_path，输出img
#     .map('img_path', 'img', image_decode_custom)
#     # 传入img，输出vec
#     .map('img', 'vec', ops.image_embedding.timm(model_name='resnet50'))
# )

# # Search pipeline
# p_search_pre = (
#     p_embed.map('vec', 'search_res', feature_search)
# )
# # 输出 search_res
# p_search = p_search_pre.output('search_res')







if __name__ == "__main__":
    
    
    app.run(config.server_host,port=config.server_port,debug=config.server_debug)
