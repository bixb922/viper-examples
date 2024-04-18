@micropython.native
def nonlocal_fails():
    y = None
    @micropython.viper
    def internal_viper():
        nonlocal y
        viperx:int = 111
        y = viperx # <--- this assignment will not work!
        return y
    return internal_viper()
print(f"{nonlocal_fails()=}, expected result 111")


def foo():
    x : int = 0
    @micropython.viper
    def inner() -> int:
        nonlocal x
        q : int = int(x)
        q += 1
        x = q  # x never increments
        return int(x)
    return inner

bar = foo()
print(f"{bar()=}")  # 0
print(f"{bar()=}")  # 0
print(f"{bar()=}")  # 0
