from ctypes import *

call = cdll.LoadLibrary('./hello.so')
a = call.add(100)
print(a)


class StructPointer(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]


# lib.Hello.restype = StructPointer


# str = lib.Hello()
# print(str)
call.more()
