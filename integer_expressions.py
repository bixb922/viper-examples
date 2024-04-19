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

@micropython.viper
def viper_expression():
    x = 1
    # Viper expressions are truncated even when not assigned to a viper int
    print(f"{x=} {x<<31=} expected: negative number")
    assert x << 31 < 0
    print(f"{1<<31=} expected: positive number")
    assert 1<<31>builtins.int(0)
    b = builtins.int(1)
    b = builtins.int(x << 31)
    print(f"builtins.int = x<<31 is {b}")
    # This is unexpected behavior. The value is truncated even before assigning!!
    # so x=1;x=x<<31 is not equal to x = 1<<31
viper_expression()  

@micropython.viper
def fun():
    y = (1<<2) + 1
    print(f"{y=} {y=:08x}")
    y = y << 31
    print(f"{y=} {y=:08x}")
    if y < 0:
        print("1<<2+1 is of type viper int")
    else:
        print("1<<2+1 is of type builtins.int")
        assert False
    print("")
    
    z = 2*3+1
    z = z << 31
    if z < 0:
        print("2*3+1 is of type viper int")
    else:
        print("2*3 is of type builtins.int")
        assert False
    print("")
    
    k = 1 + 2
    k = k << 31
    if k < 0:
        print("1+2 is of type viper int")
    else:
        print("1+2 is of type builtins.int")
        assert False
        
    print("")
    # Works up to <<29, larger than that will yield ViperTypeError: can't do binary op between 'object' and 'int'
    m = (1 << 29) + 1
    m = m << 31
    if m < 0:
        print(f"1<<29 is of type viper int")
    else:
        print(f"1<<29 is of type builtins.int")
        assert False
    print(f"{m=}")
    
    print("")
     # Works up to <<29, larger than that will yield ViperTypeError: can't do binary op between 'object' and 'int'
    p = 2**3-1
    p = p << 31
    if p < 0:
        print(f"2**3+1 is of type viper int")
    else:
        print(f"2**3+1 is of type builtins.int")
        assert False
    print(f"{p=} {p=:08x}")   
    print("")

    q = 0x3fffffff
    # Works up to 0x3fffff, 0x7ffffff will give
    # ViperTypeError: can't do binary op between 'object' and 'int'
    q = q << 31
    if q < 0:
        print(f"0xffffff is of type viper int")
    else:
        print(f"0xffffff is of type builtins.int")
        assert False
    print(f"{q=} {q=:08x}")   
    

fun()


@micropython.viper
def shift_left():
    x:int = 1
    y:int = 0
    for i in range(28,36):
        y = x << int(i)
        print(f"shift left viper 1<<{i:2d}={y:11d}={y:08x}")
        #>>> UNEXPECTED
    assert y == 0 
    
shift_left()