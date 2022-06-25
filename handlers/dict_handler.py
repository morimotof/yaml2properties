from ihandler import IObjectHandler

class DictHandler(IObjectHandler):

    def test(self,target):
        if isinstance(target, dict):
            return True
        else:
            return False

    def action(self,path,target):
        for key, value in target.items():
            self.parent.convert(path + self.parent.args.separator + str(key), value)
