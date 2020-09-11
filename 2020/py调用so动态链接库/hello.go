package main

import "C"
import "time"

//指定那些函数能被外部调用,下面这句是必须的
//export hello
func hello() string {
	return "Hello"
}

//export add
func add(n int) int {
	var s int
	for a := 0; a <= n; a++ {
		s += a
	}
	return s
}

```
//export employee    Go type not supported in export: struct  不支持
type employee struct {
	A int
	B string
	C []int
	D time.Time
	E map[string]int
}
```

//export more
func more(a int, b string, c []int, d map[string]int) employee {
	f := employee{}
	f.A = a
	f.B = b
	f.C = []int{1, 2, 3, 4, 5, 6}
	f.E = map[string]int{"a": 1, "b": 2, "c": 3}
	return f
}

func main() {
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
