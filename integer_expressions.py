# (c) 2023 Hermann Paul von Borries
# MIT License

import sys
import builtins

    
@micropython.viper
def detect_viper_int_range():
    # Detect viper range
    # This detection is really done at compile time.
    # If a variable is not a viper int, then the + line will fail
    # with compile time error ViperTypeError: can't do binary op between 'object' and 'int'
    # If this code passes compilation, then the print statements are correct
    a = 2**28-1
    a = a + 1
    print( "2**28-1 is viper int" )
    b = 2**29-1
    b = b + 1
    print( "2**29-1 is a viper int" )
    c = 2**30-1
    c = c + builtins.int(1)
    print( "2**30-1 is a builtins.int")
    d = 2**31-1
    d = d + builtins.int(1)
    print("2**31-1 is a builtins.int")
    
    e = -2**28
    e = e + 1
    print( "-2**28 is a viper int" )
    f = -2**29
    f = f + 1
    print( "-2**29 is a viper int" )
    g = -2**30
    g = g + builtins.int(1)
    print( "-2**30 is a builtins.int" )
    h = -2**31
    h = h + builtins.int(1)
    print( "-2**31 is a builtins.int" )
    

    
detect_viper_int_range()
sys.exit()
#=====================
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