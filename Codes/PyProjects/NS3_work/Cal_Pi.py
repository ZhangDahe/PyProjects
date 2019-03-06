from decimal import *
import operator
import matplotlib.pyplot as plt
import numpy as np

#容忍  用来保证迭代停止.
rongren = 10E-100

#统计每个数字出现的丰度
def fun1(x):
    num = []
    dic = {}
    for i in x:
            if i in dic:
                continue
            else:
                dic[i] = x.count(i)

    #按照key的值进行排序，得到list.    list转dict
    sorted_key_list=sorted(dic.items(),key=operator.itemgetter(0))
    sort_dic = dict(sorted_key_list)

    #打印排序之后的字典
    for key,value in sort_dic.items():
         print('{key}:{value}'.format(key = key ,value = value))


#n为数列的某一项
def bbp(n):
    pi = Decimal(0)
    k = 0
    while k<n:
        pi += (Decimal(1) / (16 ** k)) * ( (Decimal(4) / (8 * k + 1)) -
                                           (Decimal(2) / (8 * k + 4)) - (Decimal(1)
                                         / (8 * k + 5)) - (Decimal(1) / (8 * k + 6)))
        k += 1
    return pi

def main(accu):
    getcontext().prec = (accu)
    n = 0
    x = [ ]
    y = [ ]
    while (True):
        if abs(bbp(n+1)-bbp(n)) < rongren:
            print(bbp(n+1))
            break
        else:
            x.append(n)
            y.append(bbp(n))
            n += 1
    #删掉结果中的 .  保存为字符串
    str1 = str(bbp(n+1))
    str2 = str1.translate(str.maketrans('','','.'))
    fun1(str2)

    fig = plt.figure()
    fig.suptitle('Convergence of observation series')
    plt.xlabel('n')
    plt.ylabel('bbp(n)')
    plt.scatter(x, y, s=5, marker='x')  # s= 控制点的大小
    plt.show()
#main(accu) 控制数字精确度
if __name__=="__main__":
    main(50)
