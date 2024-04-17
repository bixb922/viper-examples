from array import array
import sys
import builtins
import asyncio

# Example of pointer arithmetic
@micropython.viper
def myfun(b:ptr32)->int:
    a = array("i", (11,22,33,44))
    len_of_array:int = 4
    x:ptr32 = ptr32(a)
    j:int = 0
    s:int = 0
    while j < 4:
        s += x[j] + b[j]
        j += 1
    pointer_to_second_half_of_a: ptr32 = ptr32(uint(x) + (int(len(a))//2)*4 )
    print("halves", pointer_to_second_half_of_a[0], pointer_to_second_half_of_a[1])
    return s
b = array("i", (55,66,77,88))
print(myfun(b))

# int just truncates the value
def intfun():
    return int(0x3162647F6462173)
print(f"{intfun() & 0xffffffff=:x}")
@micropython.viper
def otherfun():
    x = int(intfun())
    print(f"{x & 0x3fffffff=:x} {intfun()=:x}")
    assert x == int(0xF6462173)
otherfun()

# When viper int is shifted, most significant bits get lost
@micropython.viper
def shiftleft():
    x:int = 0-1
    for i in range(40):
        x = x<<1
        print(f"{i} {x=:x} {x=}")
    assert x == 0
shiftleft()


# How to test if an int is viper
@micropython.viper
def test_if_viper_int():
    x:int = 1
    assert (x << 31) < 0
test_if_viper_int()
print("")

@micropython.viper
def test_conversion():
    my_float_variable = 1.0
    x = 2
    my_float_variable = my_float_variable + float(x)
    assert my_float_variable == 3.0
    # Without float():ViperTypeError: can't do binary op between 'object' and 'int'
test_conversion()
print("test conversion complete")


@micropython.viper
def integer_expression():
    # ViperTypeError: local 'x' has type 'object' but source is 'int'
    x = 0xffffffff
    # Cannot change type from builtins.int to viper int
    #x = 1 #<-- ViperTypeError: local 'x' has type 'object' but source is 'int'
    assert x<<builtins.int(40) > builtins.int(0)
integer_expression()

@micropython.viper
def get_element():
    # ptr32 just gets the first 4 bytes.
    # 
    ai = array("i", (-1, 2, 3, 4) ) # signed int 32 bits
    aI = array("I", (-1, 2, 3, 4 ))  # unsigned int 32 bits
    al = array("l", (-1, 2, 3, 4 )) # signed int 32 bits
    aL = array("L", (-1, 2, 3, 4 )) # unsigned int 32 bits
    ah = array("h", (-1, 2, 3, 4 )) # signed int 16 bits
    aH = array("H", (-1, 2, 3, 4 )) # unsigned int 16 bits
    ai0 = ptr32(ai)[0]
    aI0 = ptr32(aI)[0]
    al0 = ptr32(al)[0]
    aL0 = ptr32(aL)[0]
    ah0 = ptr32(ah)[0]
    aH0 = ptr32(aH)[0]
    print(f"{ai0=}")
    assert ai0 == -1
    print(f"{aI0=}")
    assert aI0 == -1
    print(f"{al0=}")
    assert al0 == -1
    print(f"{aL0=}")
    assert aL0 == -1
    print(f"{ah0=} {ah0=:08x}")
    assert ah0 == int(0x0002ffff)
    print(f"{aH0=} {aH0=:08x}")
    assert aH0 == int(0x0002ffff)
    
    print(f"{ai0=} {aI0=} {al0=} {aL0=} {ah0=} {aH0=}")
    uai0 = uint(ptr32(ai)[0])
    uaI0 = uint(ptr32(aI)[0])
    ual0 = uint(ptr32(al)[0])
    uaL0 = uint(ptr32(aL)[0])
    uah0 = uint(ptr32(ah)[0])
    uaH0 = uint(ptr32(aH)[0])
    assert uai0 == uint(0xffffffff)
    assert uaI0 == uint(0xffffffff)
    assert ual0 == uint(0xffffffff)
    assert uah0 == uint(0x0002ffff)
    assert uaH0 == uint(0x0002ffff)
    
    print(f"{uai0=:08x} {uaI0=:08x} {ual0=:08x} {uaL0=:08x} {uah0=:08x} {uaH0=:08x}")
    print(f"{uai0=} {uaI0=} {ual0=} {uaL0=} {uah0=} {uaH0=}")
    
    ah0_ptr16 = ptr16(ah)[0]
    print(f"{ah0_ptr16=}")
    

get_element()
print("")

@micropython.viper
def assign_byte():
    x = ptr8(bytearray(10))
    v_uint = uint(0xffff)
    v_int = int(-1*256)
    x[0] = v_uint
    print(f"assign_byte assigned {v_uint} to ptr8, stores {x[0]=}")
    assert x[0] == 0xff
    x[0] = v_int
    print(f"assign_byte assigned a {v_int} to ptr8, stored {x[0]=}")
    assert x[0] == 0
assign_byte()

@micropython.viper
def reassignptr():
    x = bytearray(10)
    z = ptr32(x)
   # z = "hello"# <-- ViperTypeError: local 'z' has type 'ptr32' but source is 'object'
reassignptr()


print("cast string", int("1111"))
@micropython.viper
def cast_string():
    try:
        x = int("1")# <-- runtime TypeError: can't convert str to int
        assert False
    except TypeError:
        print("ok, viper int does not convert strings")
cast_string()


@micropython.viper
def ptr_bytes():
    x = ptr8(b'123')
    print("ptr_bytes string", x[0],x[1],x[2])
    print("can do ptr8 of bytes but not recommended")
    assert x[0] == 0x31
    assert x[1] == 0x32
    assert x[2] == 0x33
    
ptr_bytes()



@micropython.viper
def function_slice():
    x = bytearray((1,2,3,4,5))
    slice = x[builtins.int(0):builtins.int(2)]
    print("bytearray slice", slice ) 
    pslice = ptr8( slice )
    assert pslice[0] == 1 and pslice[1] == 2 
function_slice()

# Check if viper can be called as generator
@micropython.viper
def viper_add_1(p:int)->int:
    return p+1

def gene():
    x = 0
    x = viper_add_1(x)
    yield "hello"
    x = viper_add_1(x)
    yield "bye"
    yield x
it = iter(gene())
assert next(it) == "hello"
assert next(it) == "bye"
assert next(it) == 2
print("generator test complete")

# Call viper from asyncio
async def waiting_fun():
    x = 0
    x = viper_add_1(x)
    await asyncio.sleep_ms(10)
    x = viper_add_1(x)
    assert x == 2
asyncio.run(waiting_fun())

# Check optional and kw parameters
@micropython.viper
def kwfun(a, b=None, c=None):
    print(f"kwfun {a=} {b=} {c=}")
# kwfun(a=11,b=21,c=31) # <-- TypeError: function doesn't take keyword arguments
kwfun(13,23,33)
# kwfun(11,22) # <-- TypeError: function takes 3 positional arguments but 2 were given
# kwfun(10) # <-- TypeError: function takes 3 positional arguments but 2 were given#

