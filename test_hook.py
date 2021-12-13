""" this is test file for pre-commit hooks with black reformatting"""


def fun(a):
    useless_copy = a.copy()  # this is pointless
    return a


def func(a):
    return 10 * a


if __name__ == "__main__":
    arr = [1, 2]
    print(fun(arr) + func(arr))
