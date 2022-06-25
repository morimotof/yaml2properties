from ihandler import IObjectHandler

class ValueHandler(IObjectHandler):

    def test(self,target):
        return True

    def action(self,path,target):
        if (not self.parent.args.novalue):
            self.parent.print_line(path, target)
        else:
            self.parent.print_line(path,'')
