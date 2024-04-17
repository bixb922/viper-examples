# (c) 2023 Hermann Paul von Borries
# MIT License
import builtins

# Class with viper methods
# Is the decorator recognized for methods?
class Viper_class:
    @micropython.viper
    def __init__(self):
        print("Viper_class __init__ called")
        x = 1
        x = x << 31
        assert x < 0 # x must be viper int
    @micropython.viper
    def method(self):
        print("Viper_class.method called")
        x = 1
        x = x << 31
        assert x < 0 # x must be viper int
        
vc = Viper_class()
vc.method()

# Is the decorator recognized for a complete class, does
# that apply to methods?
@micropython.viper
class MyClass:
    def __init__( self ):
        print("MyClass __init__ called")
        x = 1
        assert x<<31 < 0
        
    def mymethod(self):
        x = 1
        assert x << 31 < 0 # check if viper is applying to mymethod
    @classmethod
    def myclassmethod(cls):
        print("MyClass myclassmethod called")
        x = 1
        assert x << 31 < 0 # check if viper is applying to mymethod
        
    @staticmethod
    def mystaticmethod():
        print("MyClass mystaticmethod called")
        x = 1
        assert x << 31 < 0 # check if viper is applying to mymethod

mc = MyClass()
mc.mymethod()
mc.myclassmethod()
mc.mystaticmethod()


# Instance variable manipulation
@micropython.viper
class InstClass:
    def __init__(self):
        self.a = 1
        self.b = None
        print("InstClass __init__ called")
        
    def mymethod(self):
        self.a = self.a + builtins.int(1)
        assert self.a == builtins.int(2)
        viperint = 1
        assert viperint << 31 < 0
        viperint = 111
        self.b = viperint
        assert self.b == builtins.int(111)
        
        # Create a variable
        viperint = 333
        self.c = viperint
        assert self.c == builtins.int(333)
        print("InstClass mymethod called")
mc = InstClass()
mc.mymethod()
assert mc.a == 2
assert mc.b == 111
assert mc.c == 333
print("test end")