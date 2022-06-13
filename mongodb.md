# 安装配置

1、设置环境变量，路径是D:\Program Files\MongoDB\Server\3.6\bin

2、在D盘根目录，创建文件夹data，在data里面创建文件夹db

3、打开cmd命令窗口，输入mongod --dbpath D:\data\db，这样启动服务。

后面可以再加--port 123来指定端口（一般不用）。--logpath "d://mongodb//log//mongodb.log"可以添加日志路径

4、再打开一个cmd窗口，输入mongo链接mongodb

建立一个bat文件，里面输入mongod --dbpath D:\data\db就能一键启动服务了

mongod相当于服务端需要启动，mongo相当于客户端用来链接服务端

# python命令

## 创建链接、数据库、表

```python
import pymongo
# 创建链接
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 关闭链接
myclient.close()
```

```python
# 遍历所有库
dblist = myclient.list_database_names()
print(dblist)
# 创建数据库
mydb = myclient["base"]
# 遍历所有集合
collist = mydb.list_collection_names()
# 创建集合,就是类似表
mycol = mydb["table"]
```

## 插入数据

```python
# 插入单个数据
mydict = { "id": "1", "name": "guoli", "age": 34 }
x = mycol.insert_one(mydict) 

# 插入多个数据数据
mylist = [
  { "name": "juegegn"},
  { "name": "liu"},
  { "name": "liu"},
  { "name": "ft", "area": "杭州"}
]
x = mycol.insert_many(mylist)
# 插入pandas,把df转换成dict，这里records表示过滤df的index列
mycol.insert_many(df.to_dict('records'))
```

## 查询数据

```python
# 查询第一条数据
x = mycol.find_one()
print(x)
# 查询所有数据
for x in mycol.find():
    print(x)

# 查询指定条件
myquery = { "name": "liu" }
mydoc = mycol.find(myquery)
for x in mydoc:
    print(x)
# 查询符合指定条件数目
num = mycol.count_documents(myquery)
```

## 修改数据

```python
# 修改第一条数据,该方法第一个参数为查询的条件，第二个参数为要修改的字段
myquery = { "name": "liu" }
newvalues = { "$set": { "name": "刘" } }
mycol.update_one(myquery, newvalues)

# 修改多个数据,该方法第一个参数为查询的条件，第二个参数为要修改的字段
myquery = { "name": "liu" }
newvalues = { "$set": { "name": "刘" } }
mycol.update_many(myquery, newvalues)

# 如果没有数据就插入，否者进行更新
myquery = {"name": 'liu'}
mydoc = mycol.find_one(myquery)
if mydoc == None:
    mycol.insert_one({"name": "刘国燕", "area": "湖南"})
else:
    myquery = {"name": liu}
    newvalues = {"$set": {"name": "刘国燕", "area": "湖南"}}
    mycol.update_one(myquery, newvalues)
```

## 删除数据

```python
# 删除一个文档，该方法第一个参数为查询对象，指定要删除哪些数据。
myquery = { "name": "liu" }
mycol.delete_one(myquery)
# 删除后输出
for x in mycol.find():
    print(x)
# 删除所有符合条件的数据
x = mycol.delete_many(myquery)
print(x.deleted_count, "个文档已删除")
```



# 导出mongodb

## excel

```python
import pymongo
import pandas as pd
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["base"]
mycol = mydb["table"]
temp = []
for x in mycol.find():
    temp.append(x)
df = pd.DataFrame(temp)
df.to_excel('D:\liu.xlsx')
```

## 导出JSON

```python
import pymongo
import json
import re
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["base"]
mycol = mydb["table"]
temp = []
for x in mycol.find():
    # 因为collection.find()得到的字段_id是自动生成的ObjectId
    # 所以需要转换成str格式否者无法存入json
    x['_id'] = re.findall("'(.*)'",x.get('_id').__repr__())[0]
    temp.append(x)
with open('D:/liu.json','w',encoding='UTF-8') as f:
  	f.write(json.dumps(temp,indent=2))
```

## 导入JSON

```python
import pymongo
import json
from bson import ObjectId
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["base"]
mycol = mydb["table"]
with open('D:/liu.json', 'r', encoding='UTF-8') as f:
    res = f.read()
    result = json.loads(res)
    for i in result:
        # 把str类型转换成mongodb里的对应类型
        i['_id'] = ObjectId(i['_id'])
        # 如果想要重新自动生成id就在在这里把id字段删了
        # del i['_id']
    mycol.insert_many(result)
```

