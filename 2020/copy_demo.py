from multiprocessing import shared_memory
shm_a = shared_memory.SharedMemory(create=True, size=10)
type(shm_a.buf)
buffer = shm_a.buf
len(buffer)
buffer[:4] = bytearray([22, 33, 44, 55])  # Modify multiple at once
buffer[4] = 100                           # Modify single byte at a time
# Attach to an existing shared memory block
shm_b = shared_memory.SharedMemory(shm_a.name)


import array
array.array('b', shm_b.buf[:5])  # Copy the data into a new array.array
shm_b.buf[:5] = b'howdy'  # Modify via shm_b using bytes
bytes(shm_a.buf[:5])      # Access via shm_a
shm_b.close()   # Close each SharedMemory instance
shm_a.close()
shm_a.unlink()  # Call unlink only once to release the shared memory

a = 1
b = "b"
c = [1, 2, 3, 4, 5, [6]]
d = type("aaa")

print(id(a), id(b), id(c), id(d))


def test(a, b, c, d):
    print(id(a), id(b), id(c), id(d))


test(a, b, c, d)

from copy import copy, deepcopy


def copytest(a, b, c, d):
    print(id(a), id(b), id(c), id(d))


copytest(copy(a), copy(b), copy(c), copy(d))
copytest(deepcopy(a), deepcopy(b), deepcopy(c), deepcopy(d))

c[5] = 7
print(id(a), id(b), id(c), id(d))
copytest(copy(a), copy(b), copy(c), copy(d))
copytest(deepcopy(a), deepcopy(b), deepcopy(c), deepcopy(d))