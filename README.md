# towhee-img-search
towhee+elasticsearch实现本地以图搜图

elasticsearch版本为 7.14.1

github地址：[https://github.com/CoolRwh/python-img-search](https://github.com/CoolRwh/python-img-search)


## 使用方法

一、使用 OSS 存储图片，将图片库上传到 OSS。

二、创建 elasticsearch 索引。

 * 特征向量，`resnet50` 模型 提取的图片向量维度是2048，
 * es7.4版本支持的最大维度是1024,
 * es7.14版本支持的最大维度是2048

模型地址
```
model_urls = {
    'resnet18': 'https://download.pytorch.org/models/resnet18-5c106cde.pth',
    'resnet34': 'https://download.pytorch.org/models/resnet34-333f7ec4.pth',
    'resnet50': 'https://download.pytorch.org/models/resnet50-19c8e357.pth',
    'resnet101': 'https://download.pytorch.org/models/resnet101-5d3b4d8f.pth',
    'resnet152': 'https://download.pytorch.org/models/resnet152-b121ed2d.pth',
}

```

PUT imgsearch

```json
{
  "mappings": {
    "properties": {
      "feature": {
        "type": "dense_vector",
        "dims": 2048
      },
      "url": {
        "type": "keyword"
      },
      "name": {
        "type": "keyword"
      }
    }
  }
}
```

三、修改 config.py 中的配置。

四、运行 extractFeatures.py，提取图片特征向量并存储到elasticsearch。

五、运行 searchServer.py，启动 web 服务。




参考文章 ：elasticsearch安装方法参考文章：[全文检索-ElasticSearch](https://blog.csdn.net/xjhqre/article/details/124553312)