# (c) 2023 Hermann Paul von Borries
# MIT License


# This code will most probablly lock up the microcontroller

@micropython.viper
def fun():
    x = ptr32(0)
    print(f"{x[0]=}")
    print(f"{x[1]=}")
    print(f"{x[2]=}")
    print(f"{x[3]=}")
fun()