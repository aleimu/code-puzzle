package main

func main() {
	x, y := 1, 2
	x, y = y+3, x+2

	println(x, y)
	// fmt.Print("hello world")
}

/*
方法一: go tool compile
使用go tool compile -N -l -S once.go生成汇编代码

方法二: go tool objdump
首先先编译程序: go tool compile -N -l once.go,
使用go tool objdump once.o反汇编出代码 (或者使用go tool objdump -s Do once.o反汇编特定的函数：)：

方法三: go build -gcflags -S
使用go build -gcflags -S once.go也可以得到汇编代码
*/
