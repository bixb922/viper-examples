# (c) 2023 Hermann Paul von Borries
# MIT License
  
# Autocorrelation algorithm, see https://en.wikipedia.org/wiki/Autocorrelation
# Autocorrelation is a random noise filtering algorithm

# signal: a array of signed 32 bit integers with the input signal
#         i.e. an array.array("l", ...)
# size: size of the array
# auto_signal: array of signed 32 bit integers for the output

# This example shows the use of pointer arithmetic in viper code
# There are no overflow checks, so you have to calculate previously
# the maximum value possible of the signal to prevent overflow.
# Since raw ADC signals are many times unsigned 12 bits, it can be better
# to scale those values to be from -2047 to +2048 or to scale those down
# so no overflow will occur.

@micropython.viper
def autocorrelation( signal:ptr32, size:int, auto_signal:ptr32):
    i:int = 0
    while i < size:
        auto_signal[i] = 0
        i += 1
    lag:int = 0
    while lag < size:
        sum_signal: int = 0
        p1:uint = uint(signal)
        p2:uint = uint(signal)+lag*4
        lim_p1:uint = p1 + (size-lag)*4
        while p1 < lim_p1:
            # this loop consumes all of the CPU
            sum_signal += ptr32(p1)[0] * ptr32(p2)[0]
            p1 += 4
            p2 += 4
        auto_signal[lag] +=  sum_signal
        lag += 1

