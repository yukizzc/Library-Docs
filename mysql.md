# 安装配置

https://www.jb51.net/article/198291.htm

一、下载压缩包后解压开

![](img\mysql1.png)

二、进入目录内的bin，然后运行cmd（同时把这个路径放到环境变量中）。执行下面一系列动作（8.0版本已经不需要自己创建ini配置了）

![](img\mysql2.png)

 三、启动服务成功后，敲mysql -u root -p
如果能进入mysql命令界面就说明成功了。

# SQL命令

https://www.runoob.com/mysql/mysql-select-query.html

一般直接使用可视化的软件比如SQLyg来进行管理方便

# python操作

https://www.runoob.com/python3/python-mysql-connector.html

coon是建立连接，实例化一个connect()对象。

游标（cursor）**是一个存储在MySQL服务器上的数据库查询，它不是一条SELECT语句，而是被该语句检索出来的结果集。在存储了游标之后，应用程序可以根据需要滚动或浏览其中的数据。游标主要用于交互式应用，其中用户需要滚动屏幕上的数据，并对数据进行浏览或做出更改。

## 创建数据库

```python
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=""
)
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE ft")
#关闭游标
mycursor.close()
#关闭数据库链接
mydb.close()
```

## 创建表

```python
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ft"
)
mycursor = mydb.cursor()
table_name = 'jiujiu'
# 这里第一个字段id是自动生成主键的（可以不添加），插入数据时候不需要填这个数据
temp = ' (  id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(10),age INT(10),money FLOAT(20,2)   )'
sql = 'create table ' + table_name + temp
mycursor.execute(sql)
mycursor.close()
mydb.close()
```

## 插入一条数据

```python
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ft"
)
mycursor = mydb.cursor()
sql = "INSERT INTO jiujiu (name, age, money) VALUES (%s, %s, %s)"
val = ("桔梗", 33, 2300.2)
mycursor.execute(sql, val)
mydb.commit()    # 数据表内容有更新，必须使用到该语句
print(mycursor.rowcount, "记录插入成功。")
```

## 插入多条数据

```python
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ft"
)
mycursor = mydb.cursor()
sql = "INSERT INTO jiujiu (name, age, money) VALUES (%s, %s, %s)"
val = [
    ("桔梗", 33, 2300.2),
    ("桔梗", 34, 2400.2),
    ("桔梗", 35, 2500.2),
    ("桔梗", 36, 2600)
]
mycursor.executemany(sql, val)
mydb.commit()    # 数据表内容有更新，必须使用到该语句
print(mycursor.rowcount, "记录插入成功。")
```

## 查询数据

```python
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ft"
)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM jiujiu")
myresult = mycursor.fetchall()     # fetchall() 获取所有记录，如果获取一条数据用fetchone()数据库第一条
for x in myresult:
    print(x)
```

## 根据条件查询

```python
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ft"
)
mycursor = mydb.cursor()
sql = " SELECT * FROM jiujiu WHERE name =%s and age = %d "
val = ("桔梗",33)
mycursor.execute(sql,val)
myresult = mycursor.fetchall()
for x in myresult:
    print(x)
```

查询全部的记录：      select * from jiujiu;

查第一条记录：       select * from jiujiu limit 1;

查前面两条记录：     select * from jiujiul imit 0,2;

查第二和第三条记录:   select * from jiujiu limit 1,2;

查最后一条记录：     select * from jiujiu order by id DESC limit 1;

## 修改数据

```python
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ft"
)
mycursor = mydb.cursor()
sql = "UPDATE jiujiu SET name = %s WHERE name = %s and money = %d"
# 更新多个字段用逗号隔开
# update jiujiu set name =%d,money=%d where name =%s"
val = ("刘","桔梗",2600)
mycursor.execute(sql,val)
mydb.commit()
print(mycursor.rowcount, " 条记录被修改")
```

# 注意点

## 实时读取更新的数据

常规读取数据库时候如果该数据库有更新，那么是读不到最新值的，比如下面例子循环读取然后手工录一个新数据，这个新数据不会被读取到

```python
import mysql.connector
import time
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ft"
)
mycursor = mydb.cursor()
while True:
    time.sleep(3)
    mycursor.execute("SELECT * FROM jiujiu order by id DESC limit 1")
    result = mycursor.fetchone()
    print(result)
```

解决方法

```python
import mysql.connector
import time
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="ft"
)
mycursor = mydb.cursor()
while True:
    time.sleep(3)
    mycursor.execute("SELECT * FROM jiujiu order by id DESC limit 1")
    result = mycursor.fetchone()
    # 每次执行完提交事务，也可以不加而在mysql.connector.connect时候添加一个参数:autocommit=1
    mydb.commit() 
    print(result)
```

## 关闭游标和数据库

每次最后命令后commit一下总归没错，最后记得关闭

```python
# 关闭游标
mycursor.close()
# 关闭数据库链接
mydb.close()
```