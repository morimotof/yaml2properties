from ihandler import IObjectHandler

class NoneHandler(IObjectHandler):
        
    def test(self,target):
        if target is None:
            return True
        else:
            return False

    def action(self,path,target):
        self.parent.print_line(path, '')
