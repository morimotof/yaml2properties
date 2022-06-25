from ihandler import IObjectHandler

class AttrHandler(IObjectHandler):
    
    def test(self,target):
        if hasattr(target, '__dict__'):
            return True
        else:
            return False

    def action(self,path,target):
        for key, value in target.__dict__.items():
            self.parent.convert(path + self.parent.args.separator + str(key), value)
