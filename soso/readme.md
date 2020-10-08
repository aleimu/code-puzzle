# 参考文档
https://blog.csdn.net/qq_30549833/article/details/86157744 golang学习笔记-生成windows平台的dll文件
https://blog.csdn.net/qq_38883889/article/details/108019364 python调用golang动态链接库.so和.dll

# 总结
1.动态链接库在Windows中为.dll文件，在linux中为.so文件
1、package main和func main()必须有，导出的包必须是含有main的
2、导出的函数前面用//export +函数名声明，表示需要导出该函数
3、引用包import "C"
