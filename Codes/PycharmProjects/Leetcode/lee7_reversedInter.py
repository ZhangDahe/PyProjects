class Solution(object):
 def reverse(self,x):
    x_max = 2 ** 31 - 1
    x_min = -2 ** 31
    if x < 0:
        x = -1 * int(  str(0 - x)[::-1]   )
    else:
        x = int( str(x)[::-1] )
    if x > x_max or x < x_min:
        return 0
    return x
so = Solution()
print(so.reverse(123))

# 别人的代码。 最快速度
#
# class Solution(object):
#     def reverse(self, x):
#         """
#         :type x: int
#         :rtype: int
#         """
#         s = cmp(x, 0)  x大于0，s=1；x《0 s=0
#         n = int(str(s * x)[::-1])
#
#         return s * n * (n < 2 ** 31)
