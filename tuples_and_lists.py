@micropython.viper
def fun():
    x = 1
    y = 2
    z = 3
    mytuple = (x,y,z)
    print(f"viper {mytuple=}")
    assert mytuple == (1,2,3)
    mylist = [x,y,z]
    assert tuple(mylist) == (1,2,3)
    x = x + 1
    print(f"viper {mylist=}")
    # Ensure list does not mutate
    assert tuple(mylist) == (1,2,3)
    
fun()

    