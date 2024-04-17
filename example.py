class MeasureTime:
    def __init__(self, title ):
        self.title = title
    def __enter__( self ):
        self.t0 = time.ticks_us()
        return self
    def __exit__( self, exc_type, exc_val, exc_traceback ):
        self.time_usec = time.ticks_diff( time.ticks_us(), self.t0 )
        print(f"\tMeasureTime {self.title} {self.time_usec} usec" )


import time
import array

# Original python function
def add_to_array( a, n ):
    sum_array = 0
    for i in range(len(a)):
        a[i] += n
        sum_array += a[i]
    return sum_array

@micropython.native
def native_add_to_array( a, n ):
    sum_array = 0
    for i in range(len(a)):
        a[i] += n
        sum_array += a[i]
    return sum_array

@micropython.viper
# The function declaration uses type hints to cast parameters 
# and return value to/from viper data types
# pa is a pointer to memory (very fast)
# Since pa does not carry information about the array length,
# a third argument with the length is needed
def viper_add_to_array( pa:ptr32, n:int, length:int)->int:
    sum_array = 0
    i = 0
    while i < length: # while is a bit faster than for...range
        # Same instructions now use fast integer arithmetic
        pa[i] += n  # Pointers are used like arrays
        sum_array += pa[i]
        i += 1
    return sum_array
    
    
my_array = array.array("l", (i for i in range(10000)))
with MeasureTime("Plain") as plain:
    print(add_to_array( my_array, 10 ))

with MeasureTime("Native") as native:
    print(native_add_to_array( my_array, 10 ))

with MeasureTime("Viper") as viper:
    print(viper_add_to_array( my_array, 10, len(my_array) ))

print(f"plain/native {plain.time_usec/native.time_usec}")
print(f"plain/viper {plain.time_usec/viper.time_usec}")
                       