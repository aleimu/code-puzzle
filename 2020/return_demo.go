package main

import (
	"fmt"
	"time"
)

func add_novar(a, b int) int {
	c := a + b
	defer func() {
		a++
		b++
		c++
		fmt.Println("add_novar_defer", &a, &b, &c)
	}()
	fmt.Println("add_novar_func", &a, &b, &c)
	return c
}

//add_novar_func 0xc0000100c8 0xc0000100f0 0xc0000100f8
//add_novar_defer 0xc0000100c8 0xc0000100f0 0xc0000100f8

func add_var(a int, b int) (c int) {

	defer func() {
		a++
		b++
		c++
		fmt.Println("add_var", &a, &b, &c)
	}()
	c = a + b
	fmt.Println("add_var_func", &a, &b, &c)
	return c
}

//add_var_func 0xc000010110 0xc000010118 0xc000010120
//add_var 0xc000010110 0xc000010118 0xc000010120

func add_pnovar(a, b int) *int {
	c := a + b
	defer func() {
		a++
		b++
		c++
		fmt.Println("add_pnovar_defer", &a, &b, &c)
	}()
	fmt.Println("add_pnovar_func", &a, &b, &c)
	return &c
}
func P(t time.Time) {
	fmt.Println("2", t)
	fmt.Println("3", time.Now())
}

func main() {
	a, b := 1, 2
	aa := add_novar(a, b)
	bb := add_var(a, b)
	//对照组
	c := add_pnovar(a, b)
	fmt.Println("main", &a, &b, &aa, &bb, c)
	// 执行时机
	defer P(time.Now())
	time.Sleep(5e9)
	fmt.Println("1", time.Now())

}

/*
https://my.oschina.net/henrylee2cn/blog/505535

1.多个defer的执行顺序为“后进先出”；
2.所有函数在执行RET返回指令之前，都会先检查是否存在defer语句，若存在则先逆序调用defer语句进行收尾工作再退出返回；
3.匿名返回值是在return执行时被声明，有名返回值则是在函数声明的同时被声明，因此在defer语句中只能访问有名返回值，而不能直接访问匿名返回值；
4.return其实应该包含前后两个步骤：第一步是给返回值赋值（若为有名返回值则直接赋值，若为匿名返回值则先声明再赋值）；第二步是调用RET返回指令并传入返回值，而RET则会检查defer是否存在，若存在就先逆序插播defer语句，最后RET携带返回值退出函数；
‍‍因此，‍‍defer、return、返回值三者的执行顺序应该是：return最先给返回值赋值；接着defer开始执行一些收尾工作；最后RET指令携带返回值退出函数。

# defer的作用域
0.defer声明时会先计算确定参数的值，defer推迟执行的仅是其函数体；
1. defer只对当前协程有效（main可以看作是主协程）；
2. 当panic发生时依然会执行当前（主）协程中已声明的defer，但如果所有defer都未调用recover()进行异常恢复，则会在执行完所有defer后引发整个进程崩溃；
3. 主动调用os.Exit(int)退出进程时，已声明的defer将不再被执行。
*/
