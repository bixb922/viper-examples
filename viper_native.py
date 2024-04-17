# (c) 2023 Hermann Paul von Borries
# MIT License

# Viper example to measure time
import machine
machine.freq(240_000_000)
import time
class MeasureTime:
    def __init__(self, title ):
        self.title = title
    def __enter__( self ):
        self.t0 = time.ticks_ms()
        return self
    def __exit__( self, exc_type, exc_val, exc_traceback ):
        self.time_msec = time.ticks_diff( time.ticks_ms(), self.t0 )
        print(f"MeasureTime {self.title} {self.time_msec} msec" )

@micropython.viper
def v_no_hints(limit:int)->int:
    x = 0
    while x < limit:
        x = x + 1
    return x

@micropython.viper
def v_range(limit:int)->int:
    x = 0
    for i in range(limit):
        x = x + 1
    return x
    
@micropython.viper
def v_hints(limit:int)->int:
    x:int = 0 # this type hint does nothing
    while x < limit:
        x = x + 1
    return x

@micropython.native
def native_fun(limit):
    x = 0
    while x < limit:
        x = x + 1
    return x

def undecorated_fun(limit):
    x = 0
    while x < limit:
        x = x + 1
    return x

print("Comparison of viper with hints, no hints, range and native")
limit = 5_000_000
with MeasureTime("viper, no hints"):
    assert v_no_hints(limit) == limit

with MeasureTime("viper, with hints"):
    assert v_hints(limit) == limit
    
with MeasureTime("using range"):
    assert v_range(limit) == limit

with MeasureTime("native"):
    assert native_fun(limit) == limit

#with MeasureTime("undecorated"):
#    assert undecorated_fun(limit) == limit

# Result on ESP32-S3 with PSRAM at 240 Mhz
#MeasureTime viper, no hints 271 msec
#MeasureTime viper, with hints 271 msec
#MeasureTime using range 563 msec
#MeasureTime native 3231 msec
#MeasureTime undecorated 8920 msec
    
print("")
print("Function call overhead")

def undecorated_fun(a,b,c,d,e):
    return

@micropython.viper
def viper_fun(a,b,c,d,e):
    return

@micropython.viper
def viper_fun_hints(a:int,b:int,c:int,d:int,e:int):
    return

@micropython.viper
def viper_fun_no_args():
    return

def call_funs(limit):
    with MeasureTime( "range only") as range_only:
        for i in range(limit):
            pass

    with MeasureTime("undecorated function") as undecorated:
        for i in range(limit):
            undecorated_fun(1,2,3,4,5)

    with MeasureTime("viper function") as viper:
        for i in range(limit):
            viper_fun(1,2,3,4,5)

    with MeasureTime("viper with hints function") as viper_hints:
        for i in range(limit):
            viper_fun_hints(1,2,3,4,5)

    with MeasureTime("viper with hints function") as no_args:
        for i in range(limit):
            viper_fun_no_args()


    undecorated_time = undecorated.time_msec - range_only.time_msec
    viper_time = viper.time_msec - range_only.time_msec
    viper_hints_time = viper_hints.time_msec - range_only.time_msec
    viper_fun_no_args_time = no_args.time_msec - range_only.time_msec
    print(f"{limit} function calls")
    print(f"{undecorated_time=}, {undecorated_time/limit*1000:.2f} usec per call")
    print(f"{viper_time=} {viper_time/limit*1000:2f} usec per call")
    print(f"{viper_hints_time=} {viper_hints_time/limit*1000:2f} usec per call")
    print(f"{viper_fun_no_args_time=} {viper_fun_no_args_time/limit*1000:2f} usec per call")

call_funs(1_000_000)