import abc

class BaseService(metaclass=abc.ABCMeta):  # 元类编程metaclass
    @abc.abstractmethod #抽象方法
    def login(self):
        pass
    @abc.abstractmethod
    def check_cookie(self,cookie_dict):
        pass
