import builtins
import sys

x = 1
g = None
# h is not created yet
@micropython.viper
def global_test():
    global x, g, h
    # Operation viper with global needs cast
    x = x + builtins.int(1)
    # However next line gives ViperTypeError: can't do binary op between 'object' and 'int'
    # x = x + 1
    viperx:int = 111
    # Assign to global work
    g = viperx
    h = 222
    
global_test()

print(f"global test {x=}, expected 2")
assert x == 2
print(f"global test {g=}, expected 111")
assert g == 111
print(f"global test {h=}, expected 222")
assert h == 222


def nonlocal_test():
    x = 1
    y = None
    z = None
    # Unlike global, must declare a non-local here
    @micropython.viper
    def internal_viper():
        nonlocal x, y, z
        # Operation viper with global needs cast
        x = x + builtins.int(1)
        # However next line gives 
        #x = x + 1 <-- ViperTypeError: can't do binary op between 'object' and 'int'
        viperx:int = 111
        # Assign to global work
        y = viperx
        z = builtins.int(viperx*2)
    internal_viper()
    print(f"nonlocal test {x=}, expected 2")
    print(f"nonlocal test {y=}, expected 222")
    print(f"nonlocal test {z=}, expected 111")

    assert x == 2
    assert y == 111
    assert z == 111

nonlocal_test()
sys.exit()

def closure_test():
    x = 1
    @micropython.viper
    def inner_function():
        nonlocal x
        # Next line gives ViperTypeError: can't do binary op between 'object' and 'int'
        #x = x + 1
        # this works
        x = x + builtins.int(1)
        return x
    inner_function()
    return inner_function
bar = closure_test()
print(f"closure_test {bar()=}, expected 3")
print(f"closure_test {bar()=}, expected 4")
print(f"closure_test {bar()=}, expected 5")
assert bar() == 6


# non-viper closure 
def non_viper_closure():
    x = 1
    def inner_function():
        nonlocal x
        x = x + 1
        return x
    inner_function()
    return inner_function
bar2 = non_viper_closure()
print(f"non_viper_closure, {bar2()=}, expected 3")
print(f"non_viper_closure, {bar2()=}, expected 4")
print(f"non_viper_closure, {bar2()=}, expected 5")
assert bar2() == 6


# robert-hh example of closure, fails at compile time
#@micropython.viper
#def foo():
#    x : int = 0         # <-- ViperTypeError: local 'x' used before type known
#    @micropython.viper
#    def inner() -> int:
#        nonlocal x
#        x = x + 1
#        return x
#    return inner
#
#bar = foo()
#print(bar())  # 0
#print(bar())  # 0


# This does not work
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
print(f"{bar()=}")  # <-- returns 0
print(f"{bar()=}")  # <-- returns 0
print(f"{bar()=}")  #  <-- returns 0
