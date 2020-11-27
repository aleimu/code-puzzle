package main

import (
	"context"
	"fmt"
	"github.com/gin-gonic/gin"
	"io"
	"log"
	"net/http"
	"os"
	"os/signal"
	"time"
)

func BeforeRequest() gin.HandlerFunc {
	return func(c *gin.Context) {
		method := c.Request.Method
		ip := c.Request.Host
		log.Print("method:" + method + ",ip:" + ip)
		log.Printf("c.Request.Method: %v", c.Request.Method)
		log.Printf("c.Request.ContentType: %v", c.ContentType())
		log.Printf("c.Request.Body: %v", c.Request.Body)
		log.Printf("c.Request.Form: %v", c.Request.PostForm)

		for k, v := range c.Request.PostForm { //动态获取未知参数
			log.Printf("k:%v\n", k)
			log.Printf("v:%v\n", v)
		}

		// 在gin上下文中定义变量
		c.Set("example", "12345")
		// 请求前
		c.Next() //处理请求,Next很特殊,之前的语句都是在进入handler之前执行的before_request,之后的语句是after_request执行的
		// 请求后
		log.Print("请求后")
		// access the status we are sending
		status := c.Writer.Status()
		log.Println(status)
	}
}

func main() {
	// 开启日志
	// Disable Console Color, you don't need console color when writing the logs to file.
	gin.DisableConsoleColor()

	// Logging to a file.
	f, _ := os.Create("D:\\Go\\go_test\\dome\\gin.log")
	gin.DefaultWriter = io.MultiWriter(f)

	// Use the following code if you need to write the logs to file and console at the same time.
	gin.DefaultWriter = io.MultiWriter(f, os.Stdout)

	//router := gin.Default() // 使用Default的话,就不用设置控制台日志打印格式了
	router := gin.New()
	// 自定义控制台日志打印格式
	// LoggerWithFormatter middleware will write the logs to gin.DefaultWriter
	// By default gin.DefaultWriter = os.Stdout
	router.Use(gin.LoggerWithFormatter(func(param gin.LogFormatterParams) string {

		// your custom format
		return fmt.Sprintf("%s - [%s] \"%s %s %s %d %s \"%s\" %s\"\n",
			param.ClientIP,
			param.TimeStamp.Format(time.RFC1123),
			param.Method,
			param.Path,
			param.Request.Proto,
			param.StatusCode,
			param.Latency,
			param.Request.UserAgent(),
			param.ErrorMessage,
		)
	}))
	router.Use(gin.Recovery())
	router.Use(BeforeRequest()) // 使用自定义中间件

	// This handler will match /user/john but will not match neither /user/ or /user
	router.GET("/user/:name", func(c *gin.Context) {
		log.Printf("get name start!")
		name := c.Param("name") // api 参数通过Context的Param方法来获取
		c.String(http.StatusOK, "Hello %s", name)
		log.Printf("get name end!")
	})

	// However, this one will match /user/john/ and also /user/john/send
	// If no other routers match /user/john, it will redirect to /user/john/
	router.GET("/user/:name/*action", group_dome)

	// url 为 http://localhost:8080/welcome?name=ningskyer时
	// 输出 Hello ningskyer
	// url 为 http://localhost:8080/welcome时
	// 输出 Hello Guest
	router.GET("/welcome", func(c *gin.Context) {
		name := c.DefaultQuery("name", "Guest") //可设置默认值
		last_name := c.Query("lastname")        // 是 c.Request.URL.Query().Get("lastname") 的简写
		fmt.Println("Hello ", name, last_name)
	})

	// 上传文件
	// Set a lower memory limit for multipart forms (default is 32 MiB)
	// router.MaxMultipartMemory = 8 << 20  // 8 MiB
	router.POST("/upload", func(c *gin.Context) {
		// single file
		file, _ := c.FormFile("file")
		log.Println(file.Filename)

		// Upload the file to specific dst.
		// c.SaveUploadedFile(file, dst)

		c.String(http.StatusOK, fmt.Sprintf("'%s' uploaded!", file.Filename))
	})

	//form
	router.POST("/form", func(c *gin.Context) {
		name := c.DefaultPostForm("name", "alert") //可设置默认值
		msg := c.PostForm("msg")                   //表单参数通过 PostForm 方法获取
		title := c.PostForm("title")
		fmt.Println("type is %s, msg is %s, title is %s", name, msg, title)
	})
	// 群组 /v1/Get ;/v1/Post
	someGroup := router.Group("/v1")
	{
		someGroup.GET("/Get", group_dome)
		someGroup.POST("/Post", group_dome)

	}
	// JSON/XML/YAML响应
	router.GET("/moreJSON", func(c *gin.Context) {
		// You also can use a struct
		var msg struct {
			Name    string `json:"user" xml:"user"`
			Message string
			Number  int
		}
		msg.Name = "Lena"
		msg.Message = "hey"
		msg.Number = 123
		// 注意 msg.Name 变成了 "user" 字段
		// 以下方式都会输出 :   {"user": "Lena", "Message": "hey", "Number": 123}
		c.JSON(http.StatusOK, gin.H{"user": "Lena", "Message": "hey", "Number": 123})
		c.JSON(http.StatusOK, msg)
		c.XML(http.StatusOK, gin.H{"user": "Lena", "Message": "hey", "Number": 123})
		c.XML(http.StatusOK, msg)
		c.YAML(http.StatusOK, gin.H{"user": "Lena", "Message": "hey", "Number": 123})
		c.YAML(http.StatusOK, msg)
		names := []string{"lena", "austin", "foo"}
		// Will output  :   while(1);["lena","austin","foo"]
		c.SecureJSON(http.StatusOK, names) //使用 SecureJSON 防止 json 劫持
		data := map[string]interface{}{
			"foo": "bar",
		}
		//callback is x
		// Will output  :   x({\"foo\":\"bar\"})
		c.JSONP(http.StatusOK, data)
	})

	//加载模板 --路径有问题..............
	//router.LoadHTMLGlob("D:\\Go\\go_test\\dome_file\\gin_dome\\templates\\*")
	//router.LoadHTMLFiles("D:\\Go\\go_test\\dome_file\\gin_dome\\templates\\index.html")
	//定义路由
	router.GET("/index", func(c *gin.Context) {
		//根据完整文件名渲染模板，并传递参数
		c.HTML(http.StatusOK, "index.tmpl", gin.H{
			"title": "Main website",
		})
	})
	// 重定向
	router.GET("/redirect", func(c *gin.Context) {
		//支持内部和外部的重定向
		c.Redirect(http.StatusMovedPermanently, "http://www.baidu.com/")
	})

	//1. 异步
	router.GET("/long_async", func(c *gin.Context) {
		// goroutine 中只能使用只读的上下文 c.Copy()
		cCp := c.Copy()
		go func() {
			time.Sleep(5 * time.Second)

			// 注意使用只读上下文
			log.Println("Done! in path " + cCp.Request.URL.Path)
		}()
		c.JSON(http.StatusOK, gin.H{"user": gin.H{"a": gin.H{"b": "b",}, "Number": 123}, "Message": "hey", "Number": 123})
	})
	// {"Message":"hey","Number":123,"user":{"Number":123,"a":{"b":"b"}}} --- json可以嵌套使用
	//2. 同步
	router.GET("/long_sync", func(c *gin.Context) {
		time.Sleep(5 * time.Second)

		// 注意可以使用原始上下文
		log.Println("Done! in path " + c.Request.URL.Path)
	})
	router.Any("/", any)
	router.NoRoute(go404) // 定义404

	/* 使用结构体绑定请求------对比json嵌套
	curl "http://localhost:8080/getb?field_a=hello&field_b=world"
	{"a":{"FieldA":"hello"},"b":"world"}
	$ curl "http://localhost:8080/getc?field_a=hello&field_c=world"
	{"a":{"FieldA":"hello"},"c":"world"}
	$ curl "http://localhost:8080/getd?field_x=hello&field_d=world"
	{"d":"world","x":{"FieldX":"hello"}}
	*/

	router.GET("/getb", GetDataB)
	router.GET("/getc", GetDataC)
	router.GET("/getd", GetDataD)

	// 使用参数校验
	type Login struct {
		User     string `form:"user" json:"user" xml:"user"  binding:"required"`
		Password string `form:"password" json:"password" xml:"password" binding:"required"`
	}
	// Example for binding JSON ({"user": "manu", "password": "123"})
	router.POST("/loginJSON", func(c *gin.Context) {
		var json Login
		if err := c.ShouldBindJSON(&json); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		if json.User != "manu" || json.Password != "123" {
			c.JSON(http.StatusUnauthorized, gin.H{"status": "unauthorized"})
			return
		}

		c.JSON(http.StatusOK, gin.H{"status": "you are logged in"})
	})
	//curl -X POST http://172.16.2.192:8083/loginJSON -H 'content-type: application/json' -d '{ "user": "manu" }'
	//{"error":"Key: 'Login.Password' Error:Field validation for 'Password' failed on the 'required' tag"}
	// curl -X POST http://172.16.2.192:8083/loginJSON -H 'content-type: application/json' -d '{ "user": "manu","password":"123"}'
	//{"status":"you are logged in"}

	router.Any("/testing", startPage)
	// curl "http://172.16.2.192:8083/testing?name=123&address=213143141dadad&birthday=2006-01-03"

	router.GET("/cookie", func(c *gin.Context) {
		cookie, err := c.Cookie("gin_cookie") // 获取cookie
		if err != nil {
			cookie = "NotSet"
			c.SetCookie("gin_cookie", "test", 3600, "/", "localhost", false, true)
			c.JSON(http.StatusOK, gin.H{"code": 200, "mgs": "登录成功", "data": nil})
		} else {
			c.JSON(http.StatusOK, gin.H{"code": 200, "mgs": "你已登录", "data": nil})
		}

		fmt.Printf("Cookie value: %s \n", cookie)

	})
	//curl -v "http://172.16.2.192:8083/cookie"
	//curl -v -b "gin_cookie=test" "http://172.16.2.192:8083/cookie"

	// 处理header
	router.GET("/header", func(c *gin.Context) {
		header := c.GetHeader("context")
		if header != "haha" {
			c.Header("context", "haha")
			c.JSON(http.StatusOK, gin.H{"code": 200, "mgs": "设置header成功", "data": nil})
		} else {
			c.JSON(http.StatusOK, gin.H{"code": 200, "mgs": "header已存在", "data": nil})
		}
	})
	//curl  "http://172.16.2.192:8083/header"
	//{"code":200,"data":null,"mgs":"设置header成功"}
	//curl -H 'context:haha' "http://172.16.2.192:8083/header"
	///{"code":200,"data":null,"mgs":"header已存在"}

	//启动单个服务的两种方式
	//router.Run("127.0.0.1:8083") // 也可以如下定义

	s := &http.Server{
		Addr:           ":8083",
		Handler:        router,
		ReadTimeout:    10 * time.Second,
		WriteTimeout:   10 * time.Second,
		MaxHeaderBytes: 1 << 20,
	}
	go func() {
		// service connections
		if err := s.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("listen: %s\n", err)
		}
	}()

	//启用多个服务
	//var (
	//	g errgroup.Group
	//)
	//server01 := &http.Server{
	//	Addr:         ":8080",
	//	Handler:      router,
	//	ReadTimeout:  5 * time.Second,
	//	WriteTimeout: 10 * time.Second,
	//}
	//
	//server02 := &http.Server{
	//	Addr:         ":8081",
	//	Handler:      router,
	//	ReadTimeout:  5 * time.Second,
	//	WriteTimeout: 10 * time.Second,
	//}
	//
	//g.Go(func() error {
	//	return server01.ListenAndServe()
	//})
	//
	//g.Go(func() error {
	//	return server02.ListenAndServe()
	//})
	//
	//if err := g.Wait(); err != nil {
	//	log.Fatal(err)
	//}
	// Wait for interrupt signal to gracefully shutdown the server with
	// a timeout of 5 seconds.

	//优雅重启或停止
	quit := make(chan os.Signal)
	signal.Notify(quit, os.Interrupt)
	<-quit
	log.Println("Shutdown Server ...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := s.Shutdown(ctx); err != nil {
		log.Println("Server Shutdown:", err)
	}
	log.Println("Server exiting")
}

//********************************************************************************************************************//
//自定义 函数,HandlerFunc
func group_dome(c *gin.Context) {
	name := c.Param("name")
	action := c.Param("action")
	message := name + " is " + action
	c.String(http.StatusOK, message)
}
func any(c *gin.Context) {
	method := c.Request.Method
	ip := c.Request.Host
	c.JSON(http.StatusOK, gin.H{
		"method": method,
		"ip":     ip,
	})
}

type Person struct {
	Name     string    `form:"name"`
	Address  string    `form:"address"`
	Birthday time.Time `form:"birthday" time_format:"2006-01-02" time_utc:"1"`
}

func startPage(c *gin.Context) {
	var person Person
	if c.ShouldBindQuery(&person) == nil {
		fmt.Println("====== Only Bind By Query String ======")
		fmt.Println(person.Name, person.Address, person.Birthday)
	}
	c.String(200, "Success")
}
func go404(c *gin.Context) {
	c.JSON(http.StatusNotFound, gin.H{"code": "404", "msg": "page not found!", "data": nil})
}

type StructA struct {
	FieldA string `form:"field_a"`
}

type StructB struct {
	NestedStruct StructA
	FieldB       string `form:"field_b"`
}

type StructC struct {
	NestedStructPointer *StructA
	FieldC              string `form:"field_c"`
}

type StructD struct {
	NestedAnonyStruct struct {
		FieldX string `form:"field_x"`
	}
	FieldD string `form:"field_d"`
}

func GetDataB(c *gin.Context) {
	var b StructB
	c.Bind(&b)
	c.JSON(200, gin.H{
		"a": b.NestedStruct,
		"b": b.FieldB,
	})
}

func GetDataC(c *gin.Context) {
	var b StructC
	c.Bind(&b)
	c.JSON(200, gin.H{
		"a": b.NestedStructPointer,
		"c": b.FieldC,
	})
}

func GetDataD(c *gin.Context) {
	var b StructD
	c.Bind(&b)
	c.JSON(200, gin.H{
		"x": b.NestedAnonyStruct,
		"d": b.FieldD,
	})
}

// 关于中间件的部分,参考官方README
