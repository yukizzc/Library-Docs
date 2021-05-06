|    函数    |                   描述                   |
| :--------: | :--------------------------------------: |
| json.dumps |     将 Python 对象编码成 JSON 字符串     |
| json.loads | 将已编码的 JSON 字符串解码为 Python 对象 |

# 编码

```python
import json                                                                                         
d={'桔梗':{'sex':'女','addr':'深圳','age':34},'啾':{ 'sex':'女','addr':'杭州'},}   
# 字典转成json,字典转换成字符串 加上ensure_ascii=False以后，可以识别中文， indent=2是间隔2个空格显示
print(json.dumps(d,ensure_ascii=False,indent=2))
```

```python
import json                                                                                         
d={'桔梗':{'sex':'女','addr':'深圳','age':34},'啾':{ 'sex':'女','addr':'杭州'},}   
# 打开一个名字为'test.json'的空文件
with open('test.json','w',encoding='utf-8') as f:   
    json.dump(d,f,ensure_ascii=False,indent=2)
```

区别：dumps是把python对象转换成字符串str格式，而dump把python对象转成str然后存入文件中

# 解码

```python
import json
f = open('test.json',encoding='utf-8') #打开json文件
res = f.read()
result = json.loads(res)
print(result)
```

```python
import json
f = open('test.json',encoding='utf-8') #打开的json文件
result = json.load(f)
print(result)
```

区别：后者会自动读文件少了.read()这一步

# 网上读取json文件

```python
import requests
url = 'https://ztutongrui.github.io//more.json'
r = requests.get(url) # 你要先requests获取整个网页内容
print(r) # 返回200是正常
# 直接解码
print(r.json())
```

r.json返回的就是一个字典