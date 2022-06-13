```python
import numpy as np
import pandas as pd
```


```python
# 展示所有行，None可以改成具体限制数量
pd.set_option('display.max_rows', None)
# 展示所有列，None可以改成具体限制数量
pd.set_option('display.max_columns', None) 
```

# 创建pandas


```python
# 通过字典创建
dic = {'name':['liu','guoli'],'age':[32,33]}
df = pd.DataFrame(dic)
```


```python
# array创建
array1 = np.random.randint(low=2,high=100, size=(2, 4))
df = pd.DataFrame(array1,index=[1,2],columns=['a','b','c','d'])
```

# 常用属性


```python
boolean=[True,False]
gender=["男","女"]
color=["white","black","yellow"]
data=pd.DataFrame({
    "height":np.random.randint(150,190,20),
    "weight":np.random.randint(40,90,20),
    "smoker":[boolean[x] for x in np.random.randint(0,2,20)],
    "gender":[gender[x] for x in np.random.randint(0,2,20)],
    "age":np.random.randint(15,90,20),
    "color":[color[x] for x in np.random.randint(0,len(color),20) ]
}
)
```


```python
# 根据列名取数据
data.loc[[0,1],['height','age']]
```


```python
# 根据位置序号取数据
data.iloc[0:4,2:5]
```


```python
#属性
data.columns,data.index,data.shape
```


```python
# 返回array数据
data.values
```


```python
# 头尾展示
data.head(3),data.tail(2)
```


```python
# 统计信息
data.count()
```


```python
# 详细信息
data.info()
```


```python
# 数值类型的描述
data.describe()
```


```python
# 非数值类型的描述
data.describe(include=object)
```


```python
# 列累加
data.cumsum()
```


```python
# 列相减
data.loc[:,['height','age']].diff(periods=1)
```


```python
# 相关系数
data.corr()
```


```python
#统计某列数据分布（数值和对应的数量）
data['color'].value_counts()
```


```python
#枚举某一列 
data['color'].unique() 
```

# 方法

```python
#删除指定字段里有None的行
df.dropna(subset=['sales_depart_name'],inplace=True)
#某个字段里包含某个字符的筛选数据
df[df.sales_depart_name.str.contains('包含的字符')]
```

```python
#筛选某列数值属于某个列表范围内
data[data['color'].isin(['yellow','white'])]
```

```python
#根据布尔值筛选数据
data[data['gender']=='男']
```


```python
#返回每个元素在当前列的排名，从小到大
data.rank()  
```


```python
#根据列进行排序,ascending=False表示降序
data.sort_values(by=['height', 'weight'],ascending=False) 
```


```python
#修改index
data2 = data.reindex(index=np.arange(len(data))[::-1])
```


```python
# 重置index
data2.reset_index(inplace=True)
```


```python
# 删除某列
del data2['index']  
```


```python
#删除指定列或行，axis删除列。inplace表示替换原数据      
data.drop(['height','weight'],axis=1,inplace=True) 
```

```python
# 改变某列数据类型
df['date'] = df['date'].astype('str')
# 把字符串转换成日期格式，日期可以进行排序
df = pd.DataFrame([['2019-05-30',1],['2020-06-30',2],['2018-06-30',2]],columns=['date','num'])
df['date_str'] = pd.to_datetime(df['date'])
df.sort_values(by='date_str')
```

```python
# 把seires转换成dataframe
df_series = pd.Series(np.random.randint(0,100,size=(10)),
                        index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
df = pd.DataFrame(df_series, columns=['A'])
```



# map方法


```python
#使用字典进行映射
data["gender"] = data["gender"].map({"男":1, "女":0})
```


```python
#使用函数
def age_map(x):
    gender = x if x >50 else 50
    return gender
#注意这里传入的是函数名，不带括号
data["age"] = data["age"].map(age_map)
```

# 聚合groupby

```python
import pandas as pd
dic = {'name':['liu','guoli','liu'],
       'age':[32,33,34],
       'local':['广东','韶关','韶关'],
       'height':[160,160,155]}
df = pd.DataFrame(dic)
group = df.groupby(by='name')
group2 = df.groupby(by=['name','local'])
group.mean(),group2.mean()
```

|      | name  | age  | local | height |
| ---- | ----- | ---- | ----- | ------ |
| 0    | liu   | 32   | 广东  | 160    |
| 1    | guoli | 33   | 韶关  | 160    |
| 2    | liu   | 34   | 韶关  | 155    |

|          | age  | height |
| -------- | ---- | ------ |
| **name** |      |        |
| guoli    | 33.0 | 160.0  |
| liu      | 33.0 | 157.5  |

|       |       | age  | height |
| ----- | ----- | ---- | ------ |
| name  | local |      |        |
| guoli | 韶关  | 33.0 | 160.0  |
| liu   | 广东  | 32.0 | 160.0  |
|       | 韶关  | 34.0 | 155.0  |

Groupby简单来讲就是实现数据的快速分组聚合（求和、求均值等计算），比如按照name、local等进行数据的均值（和值）计算等

# 数据合并concat merge

[pandas 的拼接merge和concat函数小结 - 亚北薯条 - 博客园 (cnblogs.com)](https://www.cnblogs.com/laiyaling/p/11798046.html)

