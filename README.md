# How to use the viper code emitter

The viper code emitter uses special viper native data types to get faster performance. The largest advantage is for integer arithmetic, bit manipulations and integer array operations. 


Read the official documentation here: https://docs.micropython.org/en/v1.9.3/pyboard/reference/speed_python.html

This document aims to provide more detailed information about the viper code emitter.

# Notes
This document is based on the interpretation of the examples provided in this repository. Feel free to check and reproduce the examples. Please report any question or issue in the issues section of this repository.

If you like this, please star the repository.

# An example
```py
# Original Python function
def add_to_array( a, n ):
    sum_array = 0
    for i in range(len(a)):
        a[i] += n
        sum_array += a[i]
    return sum_array

# The viper function, taking advantage of the viper data types
@micropython.viper
# The function declaration uses type hints (type annotations
# to cast parameters 
# and return value to/from viper data types.
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
add_to_array( my_array, 10 )
viper_add_to_array( my_array, 10, len(my_array) )

```
This viper function is about 16 times faster on my ESP32-S3 with PSRAM wih an array of 10000. 

In this example, the original add_to_array() function with @micropython.native decorator is about 1.6 times faster than the original function.

Some have reported much higher performance gains, for example 100 times! 

# The viper decorator

The @micropython.viper decorator is applied to functions, including nested functions and methods. It also can be applied to an entire class and to interrupt service routines (ISR).

Viper code is compiled and runs very fast, especially when using the viper data types. However line by line error reporting and interrupt from the console via control-C do not work while in viper code (no problem, just reset the microcontroller when stuck in a loop).

The @micropython.viper directive is a compile-time directive and activates the viper code emitter. The viper code emitter does static (compile-time) analysis of the code do determine integer variables and emits machine code to handle integer operations. It also activates the very fast pointer data types.

All things nice that MicroPython does, will continue to work. What is affected is mostly how integer variables and access to arrays work.

# @micropython.viper vs. @micropython.native decorator

The @micropython.native decorator is another means to speeds up code, but does not require special data types or constructs. It covers most of the MicroPython language functionality without change, except a very few restrictions. 

When not using the viper data types, performance of viper and native is similar. In fact, the viper code emitter is an extension of the native code emitter. However since most code has at least some integer variables, viper code may be faster than native code, sometimes even without change.

Advantages of the @micropython.native decorator: no change to the code is needed.

Advantage of the @micropython.viper decorator: the result can be faster, especially if integer and array operations are involved. But it is necessary to change the code.


# The viper data types: int, uint, ptr32, ptr16 and ptr8

These data types are very fast. They are not implemented as an MicroPython object but as a raw variable. They can be only used within a viper decorated function.

Most of the difficulties using the viper code emitter are related to the use of these data types and their peculiarities. So here goes a lot of detail about these data types.

Viper variables are "raw" variables and are not stored as MicroPython objects. In contrast the string, tuple, list and integer variables we all know are always stored ad MicroPython objects. 

The viper code emitter detects viper variables at compile time, and generates very fast code for the operations. For example
```x = 0``` or ```x = int(myfunction())``` will make `x` viper `int` variable. Now, `x = x + 1` will be compiled around 2 or 3 machine code instructions!

Compile time means: when the .py file is analyzed by the MicroPython interpreter, or when mpy-cross is run.

Please note that once assigned, the type of a viper variable cannot be changed (unlike regular Python), which is quite reasonable since there is no underlying object:

```py
    x = 1
    x = "hello" # This changes the viper int variable x to a string object, not allowed
    # The previous line raises a compile time error:
    # ViperTypeError: local 'x' has type 'int' but source is 'object'
    # The reverse order is also not allowed.
```

Be aware: The viper code emitter analyzes of the code at compile time, determining the type of the variables. This is very unusual when coming from a Python background, where typing is dynamic and at runtime.


In case you are familiar with C: The viper data types are similar to some C language data types:

|viper data type | similar C data  type | size |
|----------------|----------------------|------|
|`int`   |`long int` | 32 bit signed integer|
|`uint`  | `unsigned long int`| 32 bit unsigned integer |
|`ptr32` | `*long int` |  memory pointer to a 32 bit signed integer |
|`ptr16` |`*unsigned short int` |memory pointer to a 16 bit unsigned integer |
|`ptr8`  | `*unsigned char`|memory pointer to a 8 bit unsigned integer |

## What to remember about viper data types

* The viper data types only exist in a viper function
* The viper data types are detected at compile time (statically, before the program starts to run)
* They are not MicroPython objects but raw variables
* The associated functions `int()`, `uint()`, `ptr8()`, `ptr16()` and `ptr32()` are type casts (similar to C language)
* The MicroPython `int` object we all know is different from the viper `int` inside a viper function. If needed, the MicroPython `int` can still be accessed as `builtins.int` (`import builtins` first)
* Operations are very fast

## The viper int data type

The viper ```int```data type in viper code is a special data type for fast signed integer operations. A viper `int` can hold values from -2\*\*31-1 to 2\*\*31, i.e. this is a 32 bit signed integer.

A viper `int` is different to the ```int``` we know in MicroPython, which is still available in viper decorated functions as  ```builtins.int```.  Hence this document will make a difference between a "viper ```int``` opposed to a ```builtins.int```.

It is advisable to be aware at all times that `viper int` and `builtins.int` are different data types.

### Viper integer constants
Viper integer constants are in the range -2\*\*30 to 2\*\*30-1. When you assign a viper constant to a variable, it automatically is a viper `int`.

Be aware: integer constants don't have the full range of values a viper int value can hold, they are signed 31 bit integers. 

Integer expressions are evaluated compile time and reduced to a constant.

### Create viper int by assigning a value
As it is usual in Python, a viper variable is of type viper `int when  you assign viper ```int```value, either as a constant, integer expression or with the int() function. for example:
```py
    x = 0
    y = int(some_function_returning_an_integer())
    z = 1 + y 
    # now x, y and z are viper int variables
    p = 2**3+1
```
If the variable is created by assigning an expression, the viper code emitter will evaluate the expression at compile time.

Be aware: Integer expressions outside what is called the "small integer" range of MicroPython are not viper `int` but `builtins.int`.  On most architectures a MicroPython small integer falls is -2\*\*30-1 and 2\*\*30-1. 

For example:
```py
@micropython.viper
def myfunction();
    x = 0xffffffff # this is not a viper int
    y = 1<<30 # this is not a viper int
    z = 2**31-1  # this is not a viper int
```
In all these cases a `builtins.int` variable will be created. See [here](##-making-sure-a-viper-int-is-a-viper-int) for a way prevent the problems described here.

### Create viper int with a type hint on the function parameter
A second way to get a viper `int` is with a type hint (type annotation) of a function parameter:
```py
@micropython.viper
def myfunction(x:int):
```
With the type hint, `x` is converted on the fly to the viper `int` data type using the viper int() function (see "```int()``` casting" below).


## Making sure a viper int is a viper int

There is a possible source of problems: when you initialize a viper `int` with a integer expression that falls outside of the signed 30 bit range (not the 32 bit range!), a `builtins.int` will be created instead, no warning. The same happens if you try initialize a viper int with a variable of type `builtins.int`. These errors can go unnoticed.

Solution: Except for very short viper functions, you could initialize all viper `int` variables at the beginning setting them to zero (just as you might do in C language):
```py
@micropython.viper
def myfunction(x:int)->int:
    # declare all my integer variables
    x = 0
    limit = 0
    step = 0
```
This defines the type of the variable clearly as viper `int`. Any attempt to change the type later will give a nice compile-time message `ViperTypeError: local 'x' has type 'int' but source is 'object'`, for example:
```py
    x = 0
    y = 0
    ...some code ...
    x = 2**30 #  2**30 yields a builtins.int
    ... some more code ...
    y = "hello"  # oh, some confusion here, can't change viper int to string
```

Another way to make sure viper variables are always of the intended type, is to use the type cast:
```py
    x = int(some expression)
```
But this is a perhaps a little bit less readable.

### Differences of viper int and builtins.int data types

Viper ```int``` variables allow values from -2\*\*31 to 2\*\*31-1, whereas ```builtins.int``` variables have no practical range limit. For a `builtins.int`, if the value grows a lot, more memory will be allocated as needed.

As a result, arithmetic operations on viper variables behave like operations in the C language 32 bit signed integer operations, for example:
* Adding and subtracting wrap around if exceeding the range
* Shift left (```x<<1```): the bits shifted beyond the 32 most significant bit get lost. 
* No overflow exception

Arithmetic and logic operations for viper ```int``` are very fast, since there is no need to check for data types, conversion rules and other conditions at runtime, and the necessary code can be generated at compile time.


There are no automatic conversion rules if a viper ```int``` is used together with other data types. For example, this code will raise a compile time error: "ViperTypeError: can't do binary op between 'object' and 'int'":
```py
@micropython.viper
def myfunction(my_argument):
    x:int = 2
    x = my_argument + 1 # <- ViperTypeError: local 'x' has type 'int' but source is 'object'

    my_float_variable = 1.0
    my_float_variable = my_float_variable + x # <-- ViperTypeError: can't do binary op between 'object' and 'int'
myfunction(1)
```
The 'object' in the error message refers to `my_argument` and `my_float_variable`. The 'int' in the error message refers to the `1` viper int constant.

To avoid that error message, the viper ```int```variable x must be converted explicitly to float, and my_argument cast to a viper `int`.
```py
@micropython.viper
def myfunction(my_argument):
    x:int = 2
    x = int(my_argument) + 1 # <- ViperTypeError: local 'x' has type 'int' but source is 'object'

    my_float_variable = 1.0
    my_float_variable = my_float_variable + float(x) # <-- ViperTypeError: can't do binary op between 'object' and 'int'
myfunction(1)
```

A viper ```int``` is not an object, and thus does not support methods such as ```from_bytes()```or ```to_bytes()```. 

The \*\* operator (exponentiation, `__pow__`) is not implemented for viper ```int```.

### int() casting

Within viper decorated functions, the int() function will cast an expression o a viper `int`. Examples:
```py
   x = int(len(some_array)) # Many MicroPython functions return builtins.int
   x = int(2**30) # \*\* is not implemented for viper int and returns a builtins.int
   x = int(1) # Here int() is not necessary
   x = int(1+2) # Here int() is not necessary, 1+2 is a viper int expression
   x = int(my_int_function())+1 # Use int() for any external function that returns a integer
 ```
```int("123")``` is rejected, the argument has to be a viper `uint` or a `builtins.int`.

The int() function will return the 4 least significant bytes of the integer, similar to a C language expression: ```x && 0xffffffff```. If it is unclear that the input value is in the viper ```int``` range, the value has to be tested before casting. But in many practical applications, you can know beforehand the acceptable value ranges, and no additional overhead is incurred.

In other words, beware: `int()` just truncates values outside of the viper int range chopping off the excessive bytes, no exception raised.

int() casting is very fast in viper code. 

## The viper uint data type

This data type is in most aspects similar to viper `int` but the range is 0 to 2\*\*32-1, i.e. it's a unsigned 32 bit integer.

The uint() cast function will return the last 4 bytes of `builtins.int` as a unsigned 32 bit int.

Viper `uint` does not support `//` (integer division) nor `%` (module) operators

Casting from `uint` to `int` and back just changes the type. There is no change in the data itself, the `int()` and `uint()` functions are a no-op for this case.
Example:
```py
@micropython.viper
def test_uint_int_assignments():
    x = int(-1)
    y = uint(x)
    print(f"{x=} uint(x)={y=:08x}, expected 0xffffffff")
    z = int(y)
    print(f"{y=} int(y)={y=:08x}, expected 0xffffffff")
```

## The viper ptr32, ptr16 and ptr8 data types
These data types are pointers to memory, similar to a C language `long *p;` or `unsigned char *p`. This is rather unusual for Python, where no pointers exist and memory access is well hidden within objects that protect that access.

If x is for example a ptr32, x[0] is the four bytes at the address the pointer is pointing to, x[1] the next four bytes, etc. 

You can assign to x[n], modifying the memory contents. There is no bounds checking, so a runaway index can destroy unintended memory locations. This could  block the microcontroller. Don't panic: this is recoverable with a hard reset. In very bad cases, it might be required to flash the MicroPython image again, but there is nothing to worry: it´s not feasible to brick the microcontroller with a runaway pointer.

### Declaration of pointer variables with type hints on function argument
```py
@micropython.viper
def myfunction( x:ptr32 )->int:
    print(x[0], x[1], x[2] ) # will print 1, 2, 3, 4
    return x[1]
myfunction( array.array("l", (1,2,3,4)))
```

## Declaration of pointer variables with ptr32(), ptr16() and ptr8()
```py
@micropython.viper
def myfunction( )->int:
    int32_array = array.array("l", (1,2,3,4))
    x = ptr32( int32_array )
    print(x[0], x[1], x[2] ) # this will print 1, 2, 3, 4
    ba = bytearray(10)
    y = ptr8(ba)
    y[0] = 1 # This will change ba[0]
    return x[1]
```

You can also cast a integer to a pointer:
```py
@micropython.viper
def myfunction()->int:
    GPIO_OUT = ptr32(0x60000300) # GPIO base register
    GPIO_OUT[2] = 0x10 # clear pin 4
```

The argument to `ptr32()`, `ptr16()` or `ptr8()` can be a viper int, a uint or a bultins.int, no difference. Only the part needed for an address will be extracted.

You will have to search the microcontroller data sheet for the correct locations and meaning of each bit of the device registers. However, this type of manipulation can be very fast. Be aware: on a ESP32, MicroPython runs on top of FreeRTOS, which steals some CPU cycles every now and then, and can cause small but unwanted delays in viper code.

The `uctypes` module has an `addressof()` function. The result can also be converted to a pointer:
```py
import uctypes
@micropython.viper
def fun():
    ba = bytearray(10)
    pba = ptr8( uctypes.addressof(ba) )
```
This also can be used to point at uctypes structures.


### Viper pointers and arrays

* ptr32 allows to manipulate elements of array.array of type "l" (signed 32 bit integer)
* ptr16 allows to manipulate elements of array.array of type "H" (unsigned 16 bit integer)
* ptr8 allows to manipulate elements of a bytearray or array.array of type "B" (unsigned 8 bit integer)

Be aware: A `bytes` object could be cast to a ptr8, but bytes objects are meant to be readonly, not to be modified.


### Values of indexed pointers
 
If x is a ptr32, ptr16 or ptr8, x[n] will return a viper 32 bit signed integer.

The type of the object pointed to by the ptr variable is irrelevant. You could, for example, retrieve two elements of a "h" array with a single ptr32 x[n] assignment.

If x is a ptr16, x[n] will always be between 0 and 2\*\*16-1.

If x is a ptr8, x[n] will always be between 0 and 255.

### Assigning to a indexed pointer

* If x is a ptr8, `x[n] = v` will extract the least significant byte of the viper integer `v`and modify the byte at x[n]

* If x is a ptr16, `x[n] = v` will extract the least two significant bytes of the viper integer `v`and modify the two byte at x[n]

* If x is a ptr32, `x[n] = v` will extract modify the four bytes at `x[n]` with the viper integer v.

In all cases you will need to convert to a viper `int` first.

### Relationship with mem8, mem16 and mem32 functions

These functions are similar to ptr8, ptr16 and ptr32, but the viper pointers are significantly faster.


### Viper pointer casting and pointer arithmetic

Viper pointers can be cast to a ```uint``` and back to `ptr32`, enabling to do pointer arithmetic. For example:
```py
@micropython.viper
def fun():
    a = array("i", (11,22,33,44))
    len_of_array:int = 4
    x:ptr32 = ptr32(a)
    pointer_to_second_half_of_a:ptr32 = ptr32(uint(x) + (int(len(a))//2)*4 )
```

Note that since the array element length is 4 bytes, you have to multiply by 4 yourself. The ptr32, ptr16 and ptr8 addresses are byte addresses. 

Be aware: Some architectures may reject ptr32 access of pointers that are not multiple of four. Accessing odd bytes will most probably crash the program, no way to trap that as an exception.

# Viper function parameters and return values

For arrays and bytearrays, use the ptr32, ptr16 and ptr8 type hints in the function parameters to get fast access to the arrays. 

For integer parameters, use the `int` or `uint` type hint to get automatic conversion to a viper int. The conversion is done internally by MicroPython using the `int()` or `uint()` cast operator respectively.

If the function returns a value, a return type hint must be supplied, example:
```py
@micropython.viper
function returns_integer(param1:int)->int:
    return 1
```
The conversion of the return value back to `builtins.int` is done automatically.

If the value returned by the function is any other object, use `object` as return type annotation:
```py
def function_returns_object(x)->object:
    return x
h = function_returns_object("a string")
assert isinstance(h,str)
h = function_returns_object((1,2,3))
assert isinstance(h,tuple)
h = function_returns_object([1,2,3])
assert isinstance(h,list)
```
Viper functions do not accept keyword arguments nor optional arguments.

Somewhere the docs state a maximum of 4 arguments for a viper function, that seems not to be a restriction anymore.



# Other topics

## Passing a viper variable to a function
In a viper decorated function, you can certainly call another function. The called function can be @micropython.viper decorated, @micropython.native decorated or plain (undecorated), a bound or unbound method, there is no difference. 

However, call overhead for a viper function is lower than call overhead for a undecorated function.

If you pass a viper variable as argument to a function, it gets converted to a `builtins.int` on the fly:
* A viper `int` is treated as signed.
* A  `ptr32`, `ptr16`, `ptr8` and `uint` always leaves a positive result, no sign.

```py
@micropython.viper
def viperfun():
    x = int(1) # x now is a viper int
    some_function(x) # some_function will get 1
    y = uint(0xffffffff) 
    some_function(y) # some_function will get 0xffffffff == 4294967295
    z = int(-1)
    some_function(, z) # some_function will get a -1
    ba = bytearray(10)
    pba = ptr8(ba)
    some_function(pba) # #  # some_function will get a number like 1008145600, which is the address of ba, no sign
```

The rationale here is that the viper data types don't make sense outside the viper function, so they are converted to standard MicroPython int.  The pointers don't carry information about the type, so they can't be cast back to an array.

A nice effect of this is that you can pass a pointer down to a viper function:
```py
@micropython.viper
def fun1():
    ba = bytearray(10)
    pba = ptr8(ba)
    # Call another viper function, pass a pointer
    fun2(pba)
@micropython.viper
def fun2( mypointer:ptr8 ):
    # mypointer is now pointing to the bytearray ba
    x = mypointer[0] 
```

A side effect of this behaviour is that `type(viper_variable)` always returns class `builtins.int`

Talking about detecting type: `isinstance(viper_variable,int)` will give a compile-time error `NotImplementedError: conversion to object`, since `int` is a viper data type, not a MicroPython class. However, `isinstance(viper_variable, builtins.int)` will return `True` since the viper_variable has been converted to a MicroPython int. 


## Range vs. while

`range()` does work under viper, so you could write: ```for x in range(10)```. It is a bit faster to use a while loop, with viper ints for j, limit and step.
```py
    limit:int = 100
    step:int = 2
    j:int = start
    while j < limit:
           ...loop body....
        j += step
```

## Global variables
If you need to do integer arithmetic with a global variable, this works:
```py
import builtins
x = 1
g = None
@micropython.viper
def global_test():
    global x, g
    viper_int:int = 333
    g = viper_int
    x = x + builtins.int(10)
print(x) # x now is 11 and g is now 333

```
You can assign a viper integer to a global variable, it gets converted to a `builtins.int`.

The global variable `x` is of type `builtins.int` and you cannot mix viper `int` with `builtins.int`. In the example, `10` is a viper `int` constant and has to be converted to a `builtins.int` before operating.


## Example of nonlocal and closure with viper functions

If you access nonlocal integer variables that belong to a non-viper function, make sure the expression you assign to that is a `builtin.int`. Assigning a viper int to a nonlocal variable does nothing.

Here is a working example of a closure:
```py
import builtins
def foo():
    x = 0
    @micropython.viper
    def inner() -> int:
        nonlocal x
        x = builtins.int( int(x)+1 )
        return int(x)
    return inner
bar = foo()
bar()
bar()
bar()
```
Since x is a non-viper integer, we have to use non-viper arithmetic in the inner function to make this work.

In the previous example, if `foo()` is decorated with `@micropython.viper`, we get a compile time message complaining about x (ViperTypeError: local 'x' used before type known). Since x is not an object but a raw viper variable, it cannot be referred to as a `nonlocal`. 

You can't make a viper variable nonlocal (compile-time error `ViperTypeError: local 'x' used before type known`)

Beware: You can't change the type of a nonlocal variable inside a viper function to an integer. Example:
```py
def nonlocal_fails():
    y = None
    @micropython.viper
    def internal_viper():
        nonlocal y
        viperx:int = 111
        y = viperx # <--- this assignment will not work!
        return y
    return internal_viper()
print(nonlocal_fails(), "expected result 111")
```
The actual result is 55, but depends on the value assigned (111). The device may freeze or give any error, so don't do this.

## Viper in classes
A specific method (including `__init__`, `@staticmethod` and `@classmethod`) can have the @micropython.viper decorator.

The complete class can be decorated:
```py
@micropython.viper
class MyClass:
    def __init__( self ):
        self.a = 10
        # __init__ will be a viper decorated function, by inclusion
```
Instance variables such as ```self.a``` can only be MicroPython objects and can never be of a viper data type (remember that a viper `int` is not an object). 

You can assign a viper `int ` to a instance variable like self.x. The viper int gets converted to a `builtins.int` automatically, Operations such `self.x = self.x + viper_integer` requiere to convert the viper integer to a `builtins.int`: `self.x = self.x + builtins.int(viper_integer)`


## Slices
Viper integers cannot be used in slices. This is a restriction. The following code will not work:
```py
    x = bytearray((1,2,3,4,5))
    print("function slice", x[0:2])
```
This is a workaround: `x[builtins.int(0):builtins.int(2)]`

## async and generators

Viper decorated functions cannot have the async attribute (it crashes) nor be generators (`NotImplementedError: native yield` compile time error)

Workaround: async functions and generators can call viper functions.


## Type hints in the body of a viper function

Type hints in the body of the of a viper function are not required, but add nicely to readability. So although not mandatory, it's perhaps more readable to declare the variables with type hints:
```py
@micropython.viper
def myfunction():
    # declare all my integer variables
    x:int = 0
    limit:int = 0
    step:int = 0
```

You can't use `builtins.int` as type hint, and there is no `type` statement in MicroPython. So `builtins.int` will be always without type hint.

## Test if a variable is of type viper int
In compile time:
```py
    # Test if x is a viper int variable
    x = "hello"
```
If x is a viper variable, the assignment will fail at compile time.

In runtime, to distinguish between a viper int and a `builtins.int`:
```py
    x = 1
    if x << 31 < 0:
       print("x is a viper int")
```
The expression in the if statement will be true if x is a signed viper `int`, as opposed to a `builtins.int`. A `builtins.int` will remain positive, no matter how many times you shift the value.



## Source code of the viper code emitter
The viper code emitter is in the MicroPython code repository in `py/emitnative.c`, embedded in the native code emitter.


# Some error messages

## ViperTypeError: can't do binary op between 'int' and 'object'

This is a compile time error

In this context, 'int' means a viper `int` and 'object' any other MicroPython object including a `builtins.int`. The most common cause is trying to do an arithmetic or logic operation of a viper `int` and a `builtins.int`.

Another example for this error message is to combine a viper int with a float: if `x` is a viper `int`, then `f = 1.0 + x` will raise this error. Use `f = 1.0 + float(x)` instead. Similarly with


## ViperTypeError: local 'x' has type 'int' but source is 'object'

This compile time error happens when `x` is of type viper `int` but an object is later assigned to x, for example:
```py
   x = 0
   x = "hello"
```
It's likely that the 'object'  is `builtins.int`. You have to cast that with int() to a viper `int`.


`
## TypeError: can't convert str to int
A cause of this can be doing, for example, `int("1234")`. The viper `int()` is a casting operator and does not convert. A workaround could be `int(builtins.int("1234"))`


# Official viper documentation

* https://docs.micropython.org/en/v1.9.3/pyboard/reference/speed_python.html

# Some interesting links

Damien George's talk on MicroPythgon performance: https://www.youtube.com/watch?v=hHec4qL00x0

Interesting discussion about viper, parameters and optimization. Also see Damien George's comment on viper data types and casting: https://forum.micropython.org/viewtopic.php?f=2&t=1382

How to use the viper decorator. Several examples of viper and GPIO registers. https://forum.micropython.org/viewtopic.php?f=6&t=6994

Closure and some interesting low level stuff: https://github.com/micropython/micropython/issues/8086

Slices and viper: https://github.com/micropython/micropython/issues/6523

32 bit integer operations: https://github.com/orgs/micropython/discussions/11259

Another example manipulating manipulating GPIO: https://forum.micropython.org/viewtopic.php?f=18&t=8266

A TFT display driver using viper code, look at TFT_io.py: https://github.com/robert-hh/SSD1963-TFT-Library-for-PyBoard-and-RP2040

Use of viper decorator: https://github.com/orgs/micropython/discussions/11157

Step by step with a real problem: https://luvsheth.com/p/making-micropython-computations-run

The MicroPython tests for viper have some examples, see all cases prefixed by "viper_": https://github.com/micropython/micropython/tree/master/tests/micropython

Viper code examples in this repository:
* more_examples/fft_int.py: a integer FFT (Fast Fourier Transform), with von Hann windowing, in viper code
* more_examples/autocorrelation.py: autocorrelation noise reduction algorithm, implemented in viper code
* classes.py: viper decorator in the context of classes
* example.py: the examples here
* global_nonlocal.py: tests of viper for global and nonlocal variables
* int_uint_test.py: tests of int/uint behaviour
* integer_expressions.py: viper and builtins.int integer expressions
* odd_addresses.py: my ESP32-S3 crashes with this script
* testviper.py: Many tests
* tuples_and_lists.py: viper ints in tuples and lists
* viper_native.py: Comparison of times between viper and undecorated. Call function overhead.


# Copyright notice
This document is (c) Copyright Hermann Paul von Borries.

The Python code in this repository is copyright (c) Hermann Paul von Borries, available under MIT License




