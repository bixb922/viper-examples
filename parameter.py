import builtins

# Verify what happens when a viper int is passed to a function
def some_function(s,x):
    print(f"{s}: {x} 0x{x:.08x}")
    return x
    
@micropython.viper
def viperfun():
    x = 1
    ret = some_function("viper int 1=", x)
    assert ret == builtins.int(1)
    
    y = uint(0xffffffff)
    ret = some_function("viper uint 0xffffffff",y)
    assert ret == builtins.int(0xffffffff)
    
    z = int(-1)
    ret = some_function("viper int -1=", z)
    assert ret == builtins.int(-1) 
    
    ba = bytearray(10)
    pba = ptr8(ba)
    print("the pointer address is", uint(pba))
    some_function("viper ptr8=", pba)
    
    pmem = ptr8(0xffffffff)
    ret = some_function("viper ptr8 to 0xffffffff", pmem)
    assert ret == builtins.int(0xffffffff)
    
    #print(f"{isinstance(pmem,int)}")
    #NotImplementedError: conversion to object
    
    # f gets converted to a builtins.int before isinstance does it's stuff
    f = 0
    assert isinstance(f, builtins.int)
    
    # int gets converted to builtins.int before type() does it's stuff
    #viper_type = type(int)
    #assert viper_type == builtins.int
    
    # a number with with nine hexadecimal "f" will be passed as builtins.int
    ret = some_function("passing number > 4 bytes", 0xfffffffff)
    print(f"passing number > 4 bytes return value: {ret} == {ret:08x}")
    assert ret == builtins.int(0xfffffffff )
    
viperfun()

# Now call a viper function from a non-viper to verify the parameters are cast
# using int()  or uint()
@micropython.viper
def viper_fun_int(s,  x:int )->int:
    print(s, f"check parameter cast int: argument {x} == {x:08x}")
    return x
@micropython.viper
def viper_fun_uint(s,  x:uint )->uint:
    print(s, f"check parameter cast uint: argument {x} == {x:08x}")
    return x

def check_parameter_cast():
    
    # uint and int function produce the same result for positive numbers
    for fun in (viper_fun_int, viper_fun_uint):
        ret = fun("1", 1)
        assert ret == 1

        # Check maximum small int
        ret = fun("0x3fffffff",0x3fffffff)
        assert ret == 0x3fffffff

        # Check maximum signed int
        ret = fun("0x7fffffff", 0x7fffffff)
        assert ret == 0x7fffffff

        ret = fun("0xff7a55bb33", 0xff7a55bb33)
        assert ret ==         0x7a55bb33 # truncated to 4 bytes, but by chance positive
        assert ret > 0

    # Check with just 4 bytes of f
    ret = viper_fun_int("0xffffffff", 0xffffffff)
    print(f"0xffffffff return value {ret} == {ret:08x}")
    assert ret == -1 # truncated to 4 bytes

    # Check with just 4 bytes of f
    ret = viper_fun_uint("0xffffffff", 0xffffffff)
    print(f"0xffffffff return value {ret} == {ret:08x}")
    assert ret == 0xffffffff # truncated to 4 bytes

        
    # Check with number > 4 bytes
    ret = viper_fun_int("0xffffffffff", 0xffffffffff)
    print(f"0xffffffffff return value {ret} == {ret:08x}")
    assert ret == -1 # truncated to 4 bytes

    # Check with number > 4 bytes. Here uint is different than int
    ret = viper_fun_uint("0xffffffffff", 0xffffffffff)
    print(f"0xffffffffff return value {ret} == {ret:08x}")
    assert ret == 0xffffffff # truncated to 4 bytes
        
check_parameter_cast()

# viper int does not convert string to int, unlike builtins.int
try:
    viperfun("123")
except TypeError:
    print("OK: can't cast string to viper int in a parameter")