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
```

## 修改数据

```python
# 修改第一条数据
myquery = { "name": "liu" }
newvalues = { "$set": { "name": "刘" } }
mycol.update_one(myquery, newvalues)

# 修改多个数据
myquery = { "name": "liu" }
newvalues = { "$set": { "name": "刘" } }
mycol.update_many(myquery, newvalues)
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
df.to_excel('D:\liu.xls')
```
