__doc__ = """
元类: 用来拦截和修改 继承此元类 的子类的 创建

# 为一个类定义确定适当的元类是根据以下规则:
    1.如果没有基类且没有显式指定元类，则使用 type()；
    2.如果给出一个显式元类而且 不是 type() 的实例，则其会被直接用作元类；
    3.如果给出一个 type() 的实例作为显式元类，或是定义了基类，则使用最近派生的元类。

# 目的
    了解元类的目的前需要先知道普通继承的作用与特点:
    继承的特点：
        <1>减少代码量和灵活指定型类
        <2>子类具有父类的方法和属性
        <3>子类不能继承父类的私有方法或属性
        <4>子类可以添加新的方法
        <5>子类可以修改父类的方法
        
    可以看到所有涉及到变动的特点都需要子类中实现,这样的话,对于某些固定模式的变动就需要子类中重复实现,增加子类中的代码量,
    或者所有子类固定继承某一个中间类,并在中间类的__new__中根据子类模式去创建,元类就可以理解为python中单独提出来的中间类,
    而一切类的创建最终都会调用type.__new__(cls, classname, bases, attrs)
    元类的使用就是在子类创建时拦截并修改,可以依据子类的特点增加或修改属性.

# 参考:
https://docs.python.org/zh-cn/3/reference/datamodel.html#object.__new__
https://docs.python.org/zh-cn/3/reference/datamodel.html#metaclasses

"""

import abc
from six import add_metaclass, with_metaclass  # py2和py3的桥梁,元类相关的变化很大,可通过six做兼容.

Meta = abc.ABCMeta


# 通用做法。
@add_metaclass(Meta)
class MyClass(object):
    pass


# 在Python 3 等价于
class MyClass(object, metaclass=Meta):
    pass


# 在Python 2.x (x >= 6)中等价于
class MyClass(object):
    __metaclass__ = Meta
    pass


# 或者直接调用装饰器，这里也能看出来装饰器就是个方法包装而已。
class MyClass(object):
    pass


MyClass = add_metaclass(Meta)(MyClass)


# 再或者用 with_metaclass
class MyClass(object, with_metaclass(Meta)):
    pass


def with_metaclass(meta, *bases):  # 代码摘自sqlalchemy中对元类的包装,采用了类似six.with_metaclass的方式
    """Create a base class with a metaclass.

    Drops the middle class upon creation.

    Source: http://lucumr.pocoo.org/2013/5/21/porting-to-python-3-redux/

    """

    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__

        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)

    return metaclass("temporary_class", None, {})


# 继承type 创建元类
class SayMetaClass(type):
    # 用type动态生成类的的三个重要参数：类名称、父类、属性
    def __new__(cls, name, bases, attrs):
        # 创造"天赋"
        attrs['say_' + name] = lambda self, value, saying=name: print(saying + ',' + value + '!')
        # 类名称、父类、属性 生成元类
        return type.__new__(cls, name, bases, attrs)


# 继承元类 创建类
# class Hello(object, metaclass=SayMetaClass):
class Hello(object, with_metaclass(SayMetaClass)):
    pass


# 创建实列
hello = Hello()
# 调用实例方法
hello.say_Hello('world!')


# 普通类的创建与继承
class Man:
    def __new__(cls, name, age):  # 静态方法
        print('Man.__new__ called.', getattr(cls, 'work_copy'))  # 能传过来
        return super(Man, cls).__new__(cls)  # -->self


# 对比普通类的继承与创建

class Person(Man):
    """普通继承
    对象是由 __new__() 和 __init__() 协作构造完成的 (由 __new__() 创建，并由 __init__() 定制)，
    所以 __init__() 返回的值只能是 None，否则会在运行时引发 TypeError。
    """

    def __new__(cls, name, age, work):  # 可以不写,默认继承了Man.__new__
        print('Person.__new__ called.')
        cls.work_copy = work
        # return super(Person, cls).__new__(cls, name, age)  # -->Man.__new__
        cls = super(Person, cls).__new__(cls, name, age)  # 根据需要修改新创建的实例再将其返回
        cls.work = work  # 可以看到,__new__也是可以做__init__的数值绑定的
        return cls

    def __init__(self, name, age, work):  # 参数与__new__必须一致,__new__的后续构造
        print('Person.__init__ called.')
        self.name = name
        self.age = age
        # self.work = work

    def __str__(self):
        return '<Person: %s %s %s>' % (self.name, self.age, self.work)


zhangsan = Person('zhangsan', 24, '张三')
print(zhangsan)
