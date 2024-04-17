# (c) 2023 Hermann Paul von Borries
# MIT License

import sys

@micropython.viper
def fun():
    x = 1
    print(f"{x=} {x<<31=} expected: negative number")
    print(f"{1<<31=} expected:negative number")
    y = 1<<2 + 1 
    if y<<31 < 0 :
        print("1<<2+1 is of type viper int")
    else:
        print("1<<2+1 is of type builtins.int")
        assert False
        
    z = 2*3+1
    if z<<31 < 0:
        print("2*3+1 is of type viper int")
    else:
        print("2*3 is of type builtins.int")
        assert False
        
    k = 1 + 2
    if k<<31 < 0:
        print("1+2 is of type viper int")
    else:
        print("1+2 is of type builtins.int")
        assert False
        
    print("")
    # Works up to <<29, larger than that will yield ViperTypeError: can't do binary op between 'object' and 'int'
    m = (1 << 29) + 1
    if m<<31 < 0:
        print(f"1<<29 is of type viper int")
    else:
        print(f"1<<29 is of type builtins.int")
        assert False
    print(f"{m=}")
    
    print("")
     # Works up to <<29, larger than that will yield ViperTypeError: can't do binary op between 'object' and 'int'
    p = 2**3-1
    if p<<31 < 0:
        print(f"2**3+1 is of type viper int")
    else:
        print(f"2**3+1 is of type builtins.int")
        assert False
    print(f"{p=} {p=:08x}")   
    

    q = 0x3fffffff
    # Works up to 0x3fffff, 0x7ffffff will give
    # ViperTypeError: can't do binary op between 'object' and 'int'
    if q<<31 < 0:
        print(f"0xffffff is of type viper int")
    else:
        print(f"0xffffff is of type builtins.int")
        assert False
    print(f"{q=} {q=:08x}")   
    

fun()
sys.exit()

@micropython.viper
def fun2():
    x = 0
    x = 1
    if x<<31 < 0:
        print("x is viper int")
    else:
        print("NOT EXPECTED x is no viper int")
        assert False
fun2()

@micropython.viper
def fun3():
    x = 1
    if x<<31 < 0:
        print("x is viper int")
    else:
        print("NOT EXPECTED x is no viper int")
        assert False
    # x = 1>>31 # <-- ViperTypeError: local 'x' has type 'int' but source is 'object'
    
    # This creates a builtins.int
    z = 1<<31 
    z = z<<builtins.int(10)
    assert z == builtins.int(0)
    
fun3()