'''
Given a sorted array and a target value, return the index if the target is found.
If not, return the index where it would be if it were inserted in order.
You may assume no duplicates in the array.
'''
'''分清情况，人工debug
思路：1 若元素相等
2.不相等时， 2.1判断头和尾元素
            2.2 看内部的元素'''
class Solution(object):
    def searchInsert(self, nums, target):
        j =1
        for i in range(len(nums)):
            if nums[i] == target :
                return i
                j = 0
                break

        if j == 1 :
            if target >= nums[-1]:
                return len(nums)
            else:

                    if nums[0] > target:
                        return 0
                    else:
                        for k in range(len(nums)) :
                              if nums[k] < target <nums [k+1] :
                                      return k+1

value = 4
nums = [1,3,5]
so =Solution()
print(so.searchInsert(nums,value))


"不要轻易提交，run code 可能没问题，但是提交很可能有问题！ 多用几组例子想想看"
"错误示范"
# "class Solution(object):
#     def searchInsert(self, nums, target):
#         j =1
#         for i in range(len(nums)):
#             if nums[i] == target :
#                 return i
#                 j = 0
#                 break

#     以下写的 不对了，未考虑到 value大于array内所有数的情况
#         if j == 1 :
#             for k in range(len(nums)):
#                 if nums[k] < target :
#                     return k+1
#                     break"

"版本2   函数range 产生的是一个列表， range(8)-1 错误写法"
"一旦脱离ide，写代码是不是就有点生了呀"


# class Solution(object):
#     def searchInsert(self, nums, target):
#         """
#         :type nums: List[int]
#         :type target: int
#         :rtype: int
#         """
#         j = 1
#         for i in range(len(nums)):
#             if nums[i] == target:
#                 return i
#                 j = 0
#                 break
#
#         if j == 1:
#             if target >= nums[-1]:
#                 return len(nums)
#             else:
#                 for k in range(len(nums)) - 1:
#                     if nums[k] < target < nums[k + 1]:
#                         return k + 1
#                         break
#                     else:
#                         return 0class Solution(object):
'''别人的写法 思路： 1.判断第一个和最后一个元素 与 target的关系
                  2.考虑内部的元素。for 循环： 相等则输出， 不等则用 num【i】 》 target 来确定输出  注意此处是谁大于谁。用target》num【i】则 不可行'''
'''  def searchInsert(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        if nums[0]>target:
            return 0
        if nums[-1]<target:
            return len(nums)
        for i in range(len(nums)):
            if nums[i]==target:
                return i
            elif nums[i]>target and i!=0:
                return i'''