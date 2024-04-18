There are some MicroPython viper code examples in this repository:
* signal_processing/fft_int.py: a integer FFT (Fast Fourier Transform), with von Hann windowing, in viper code
* signal_processing/autocorrelation.py: autocorrelation noise reduction algorithm, implemented in viper code


The rest are exercises to find out how viper works. The conclusions of these tests are at https://github.com/micropython/micropython/wiki/Improving-performance-with-Viper-code
* classes.py: viper decorator in the context of classes
* example.py: the examples here
* global_nonlocal.py: tests of viper for global and nonlocal variables
* int_uint_test.py: tests of int/uint behaviour
* integer_expressions.py: viper and builtins.int integer expressions
* odd_addresses.py: my ESP32-S3 crashes with this script
* testviper.py: Many tests
* tuples_and_lists.py: viper ints in tuples and lists
* viper_native.py: Comparison of times between viper and undecorated. Call function overhead.


