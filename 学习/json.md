# json

## 	二级

> ### dict 转json字符串

```python
import json
dictdata = {"a":"b","b":{"c":"cc"}}
str = json.dumps(dictdata)
print(str)
```

```json
{"a":"b","b":{"c":"cc"}}
```
格式化输出
```python
str = json.dumps(dictdata,sort_keys=True, indent=4, separators=(',', ':'))
print(str)
```

```json
{
    "a":"b",
    "b":{
        "c":"cc"
    }
}
```







# 一级一级一级一级一级一级一级一级一级

## 二级

### 	三级







# 一级2222222222222222222

## 二级