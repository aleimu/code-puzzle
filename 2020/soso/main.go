//main.go
package main

import "C"

//下面这句很重要，对外开放Hello方法 不加这个外部无法访问该方法
//export Hello
func Hello() string {
	return "Hello"
}

//下面这句很重要，对外开放Hello方法 不加这个外部无法访问该方法
//export Add
func Add(left, right *C.char) *C.char {
	// bytes对应ctypes的c_char_p类型,翻译成C类型就是 char *指针
	merge := C.GoString(left) + C.GoString(right)
	return C.CString(merge)
}

//export Test
func Test() {
	println("test")
}

func main() {
}
