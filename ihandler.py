import abc

class IObjectHandler(metaclass=abc.ABCMeta):
    def __init__(self,parent):
        self.parent = parent

    # このhandlerでtargetを処理するかどうか判定する
    @abc.abstractmethod
    def test(self, target)->bool:
        raise NotImplementedError()
    
    # testでtrueを返すと続いてactionが呼び出される
    @abc.abstractmethod
    def action(self,path,target)->None:
        raise NotImplementedError()
