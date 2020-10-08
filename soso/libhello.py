from ctypes import *  
import ctypes

class StructPointe(Structure):  
    _fields_ = [("p", c_char_p), ("n", c_longlong)]
    
if __name__ == "__main__":  
    lib = cdll.LoadLibrary('./libhello.so')
    lib.Hello.restype =  StructPointe
    aa = lib.Hello()
    print(aa)
    aa=aa.p[:aa.n]
    print(aa)
    add= ctypes.CDLL('libhello.so').Add
    add.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    add.restype = ctypes.c_char_p
    left = b"Hello"
    right = b"World"
    bb=add(left, right)
    print(bb)
