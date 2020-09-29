package main

import (
    "fmt"
)

func producer(ch chan<- int) {
    i := 0
    for {
        ch<-i
        i++
    }
}

func consumer(ch <-chan int) {
    for {
        fmt.Println(<-ch)   // 149637 卡主了
    }
}

func main() {
    ch := make(chan int, 100)
    go producer(ch)
    go consumer(ch)
    for {}
}

/*
Go1.13中，空的for循环扰乱调度、阻断STW，造成GC阻塞的问题
go1.14实现了真正意义上的抢占式调度

https://fengyoulin.com/for-block-all.html
https://fengyoulin.com/go-preempt.html
根本原因就是：循环中不断分配堆内存，达到GC触发条件后，新的分配需要等待GC，而GC需要STW，而main函数中的for循环，就像一个未释放的自旋锁，一直在那里循环，阻止了STW完成，进而阻止了GC，所以程序就卡住了。
Go语言编译器在函数入口处插入的栈增长代码，同时被运行时用来执行协程调度。

*/