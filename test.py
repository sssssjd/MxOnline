# -*- coding: utf-8 -*-
__author__ = 'sssssjd'
__date__ = '2018/8/24 13:55'
a=1  # 个数
n=2  # 值
m = True
while m:
    n = n + 1
    for i in range(2, n):
        if n % i == 0:
            break
    else:
        a = a+1
    if a == 521029:
        print(n)
        m = False

