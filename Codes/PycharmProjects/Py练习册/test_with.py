'''1 执行__enter__,返回值赋给example
   2.执行block块
   3.执行__exit__程序'''
class Test():
    def __enter__(self):
        print("In __enter__()")
        return "test_with"


    def __exit__(self, type, value, trace):
        print("In __exit__()")


def get_example():
    return Test()


with get_example() as example:
    print("example:", example)
