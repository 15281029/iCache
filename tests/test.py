import time

from iCache.iCache import Cache

cache = Cache(maxsize=255, ttl=5)  # 设置全局 ttl缓存有效期 5s

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
time.sleep(2)   # 延时 2s
# 确定缓存结果是否有效
print(cache.is_effective(func))
# 利用下标快速访问缓存元素
print(cache[func])
# 计算当前缓存大小
print(len(cache))
cache.delete(para='invalid')
cache.view_cache()
# 将缓存转储为 json
# print(cache.dump())
