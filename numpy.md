```python
import numpy as np
```

# 创建numpy


```python
a = np.array([1, 2, 3])
b = np.array([[1,2,3],[4,5,6]])
a.shape, b.shape
```
# 属性

```python
np.zeros((2,2))
```


```python
np.ones((1,2))
```


```python
# 单位矩阵
np.eye(5)
```


```python
# 随机整数
np.random.randint(low=2,high=5, size=(2, 4))
```


```python
# 标准正太分布
np.random.randn(2,4)
```


```python
# 0-1之间的随机，两种方法一样不过参数形式不一样，后者接受一个元组
np.random.rand(2,4),np.random.random((2,4))
```


```python
# 数列，最后一个参数是步长
np.arange(0,10,2)
```


```python
# 切分num个数的数列
np.linspace(start=0,stop=10,num=20,endpoint=False)
```

# 索引切片


```python
# Create the following rank 2 array with shape (3, 4)
# [[ 1  2  3  4]
#  [ 5  6  7  8]
#  [ 9 10 11 12]]
a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])
```


```python
a[0,:],a[1,3]
```


```python
# 布尔索引
a[a>5]
```

# 数据类型


```python
a = np.array([1.1, 1.2],dtype = np.int32)
a.dtype
```


```python
# 转换成浮点类型
b = a.astype(np.float32)
```


```python
a.dtype, b.dtype
```

# 数学计算


```python
# 矩阵计算,直接用*表示的是点乘
x = np.array([[1,2],[3,4]])
y = np.array([[5,6],[7,8]])
np.dot(x,y)
```


```python
# 求和,axis=0表示沿着行累加
x = np.array([[1,2],
              [3,4]])
x.sum(),x.sum(axis=0),x.sum(axis=1),x.T
```


```python
# 最大值，均值
x.max(),x.mean(axis=0)
```


```python
# 转换维度
x.reshape(-1,1)
```

# np叠加


```python
a=[1,2,3,4]
b=[5,6,7,8]
c=[9,10,11,12]
```


```python
# 横向叠加
np.hstack((a,b,c))
```


```python
# 纵向叠加
np.vstack((a,b,c))
```
