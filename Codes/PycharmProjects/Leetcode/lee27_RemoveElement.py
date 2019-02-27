# #注意读懂题目
# Given an array nums and a value val,
# remove all instances of that value in-place and return the new length.
# Do not allocate extra space for another array,
# you must do this by modifying the input array in-place with O(1) extra memory.
# The order of elements can be changed. It doesn't matter what you leave beyond the new length.

#只要求返回长度
class Solution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        length = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[length] = nums[i]
                length += 1
        return length
nums = [1,2,2,4, 5]
val =2
so = Solution()
print(nums)
print(so.removeElement(nums,val))
