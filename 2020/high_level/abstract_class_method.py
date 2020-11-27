__doc__ = """
抽象基类: 继承的约束与协议

# 抽象基类 --- 有点java的味道,也有点golang的味道,继承,协议,接口
    1.抽象基类不能实例化
    2.必要时可以要求子类实现基类指定的抽象方法

# 抽象基类的目的：
    1.处理继承问题方面更加规范、系统
    2.明确调用之间的相互关系
    3.使得继承层次更加清晰
    4.限定子类实现的方法

# 参考
https://www.osgeo.cn/cpython/library/abc.html   # 介绍
https://www.python.org/dev/peps/pep-3119/   # 缘由
https://www.cnblogs.com/traditional/p/11731676.html # 使用
"""

import abc


class Base(abc.ABC):

    @abc.abstractmethod  # 要求子类实现指定协议,抽象方法用@abstractmethod装饰器标记,而且定义体中通常只有文档字符串.
    def my_protocol(self):
        """要求子类实现的自定义协议"""

    def not_protocol(self):
        """不要求子类实现的自定义协议"""

    @classmethod
    def __subclasshook__(cls, subclass):  # 同时作用于isinstance和issubclass
        """
        此方法应返回 True ， False 或 NotImplemented .
        如果它回来 True , the 子类 被认为是ABC的一个子类。
        如果它回来 False , the 子类 不被认为是ABC的一个子类，即使它通常是ABC的一个子类。
        如果它回来 NotImplemented ，子类检查继续使用常规机制。
        """
        # print("subclass.__mro__:", subclass.__mro__)  # 继承树

        if cls is Base:
            if any("my_protocol" in B.__dict__ for B in subclass.__mro__):
                return True
            else:
                return False
        return NotImplemented


# 显式继承Base
class MyClass(Base):
    """子类"""

    def my_protocol(self):
        pass


# 显式继承Base
class MyClass2(Base):
    """子类"""

    def my_protocol(self):
        pass


@Base.register
class MyClass3():
    """虚拟子类:issubclass和isinstance等函数都能识别，但是注册的类不会从抽象基类中继承任何方法或属性."""


k = MyClass()
print(isinstance(k, Base))  # True
print(issubclass(MyClass, Base))  # True

k2 = MyClass2()
print(isinstance(k2, Base))  # True
print(issubclass(MyClass2, Base))  # True

k3 = MyClass3()
print(isinstance(k3, Base))  # False
print(issubclass(MyClass3, Base))  # False
