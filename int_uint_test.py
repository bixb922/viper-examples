import array
import builtins

@micropython.viper
def test_ptr_returns_int():
    a1 = array.array("l", (1,-1,2,0x7fffffff,0x80000000))
    ptra1 = ptr32(a1)
    # Test if signed int
    x = ptra1[0] << 31
    assert x < 0
    print("ptr32[] returns a viper signed int")
    
    a2 = array.array("H", (1,10,100,1000,65525))
    ptra2 = ptr16(a2)
    y = ptra2[0] << 31
    if y < 0:
        print("ptr16[] returns a viper signed int")
    else:
        print("ptr16[] returns a unsigned int")
        assert False
    
    a3 = bytearray(((1,2,4,8,255)))
    ptra3 = ptr8(a3)
    z = ptra3[0] << 31
    if z < 0:
        print("ptr8[] returns a viper signed int")
    else:
        print("ptr8[] returns a unsigned int")
        assert False

    a4 = array.array("l", (0xffffffff, 1))
    if ptr32(a4)[0] == -1 and ptr32(a4)[1] == 1:
        print("ptr32 returns all 32 bits")
    else:
        print("Unexpected a4 pointer behaviour")
        assert False

    a5 = array.array("H", (0xffff, 1, 0xc0c0))
    if ptr16(a5)[0] == 0xffff and ptr16(a5)[1] == 1 and ptr16(a5)[2] == 0xc0c0:
        print("ptr16 returns 16 bits, no sign propagation")
    else:
        print(f"Unexpected ptr16 pointer result {ptr16(a5)[0]=:x} {ptr16(a5)[3]=:x}")
        assert False

    a6 = array.array("B", (0xff, 1, 0xA6))
    if ptr8(a6)[0] == 0xff and ptr8(a6)[1] == 1 and ptr8(a6)[2] == 0xA6:
        print("ptr32 returns 16 bits, no sign propagation")
    else:
        print(f"Unexpected a4 pointer result {ptr8(a6)[0]=:x} {ptr8(a6)[1]=:x}")
        assert False
        
    
    
test_ptr_returns_int()


@micropython.viper
def test_uint_int_assignments():
    x = int(-1)
    y = uint(x)
    print(f"{x=} uint(x)={y=:08x} expected 0xffffffff")
    assert y == uint(0xffffffff)
    z = int(y)
    print(f"{y=} int(y)={y=:08x} expected 0xffffffff")
    assert z == -1
    print(f"{str(x)=} {repr(x)=}")
    assert str(x) == "-1"
    assert repr(x) == "-1"
    
test_uint_int_assignments()


