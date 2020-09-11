# py调用动态链接库so文件

# 参考文档
https://www.cnblogs.com/huangguifeng/p/8931837.html
https://www.cnblogs.com/fariver/p/6573112.html


# go代码生成动态链接库
go build -buildmode=c-shared -o hello.so src/hello.go