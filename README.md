# iCache

用 Python 实现缓存机制 

# Env

Python 3.x

# Install

```
pip install iCache
```
or
```
git clone git@github.com:15281029/iCache.git
cd PyCache
python setup.py install
```

# Usage

- 自定义缓存大小，全局ttl和局部ttl
- 手动设置缓存项和缓存结果
- 装饰器自动设置函数缓存
- 利用下标访问缓存
- 可转储为json

```
from iCache import Cache
import time

cache = Cache(ttl=5)  # 设置全局 ttl缓存有效期 5s

# 手动建立单值缓存 并设置单指有效期，覆盖全局设置，仅对该值有效
cache.set(1, 'foo', ttl=3)
cache.set(2, 'bar')
# 得到该值的所有信息，包括 value 值 ttl 有效期 time 保存时间
print(cache.get_all(1))
# 仅得到值
print(cache.get_value(1))


# 支持装饰器函数自动保存函数返回值 并设置有效期 1s
@cache.cache(ttl=1)
def func(a, b):
    return a+b


func(1, 3)
# 查看所有缓存信息
cache.view_cache()
# 得到函数缓存值
print(cache.get_value(func))
# 查看当前缓存是否有效
print(cache.is_effective(func))
time.sleep(3)   # 延时 3s
# 再确定缓存结果是否有效
print(cache.is_effective(func))
```
```
{'value': 'foo', 'ttl': 3, 'time': 1520221365.6172993}
foo
{1: {'value': 'foo', 'ttl': 3, 'time': 1520221365.6172993}, 2: {'value': 'bar', 'ttl': 5, 'time': 1520221365.6172993}, 'dff8f8595067cae2cb9e004adc8a68c4876acdcc': {'value': 4, 'ttl': 1, 'time': 1520221365.6172993}}
4
True
False
```

# TODO

- 实现FIFO和FILO

# 后记

欢迎各位大佬fork star
