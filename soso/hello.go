package main

import "C"
import (
	"fmt"
)

//export Sum
func Sum(a int, b int) int { //最简单的计算和
	return a + b
}

//export Show
func Show(str string) { //显示传入的字符串
	fmt.Print(str)
}

func main() {
}
