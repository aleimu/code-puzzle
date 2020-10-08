import ctypes

#load the shared object file
adder = ctypes.cdll.LoadLibrary('./adder.so')

#Find sum of integers
res_int = adder.add_int(4,5)
print("4 + 5 = " + str(res_int))

#Find sum of floats
a = ctypes.c_float(5.5)
b = ctypes.c_float(4.1)

add_float = adder.add_float
add_float.restype = ctypes.c_float

print("5.5 + 4.1 = " + str(add_float(a, b)))