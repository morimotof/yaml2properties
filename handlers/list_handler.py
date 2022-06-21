import ihandler as IOC

class ListHandler(IOC.IObjectHandler):

    def test(self,target):
        if isinstance(target, list):
            return True
        else:
            return False

    def action(self,path,target):
        for i, item in enumerate(target):
            if(self.parent.args.noindex):
                index = ''
            else:
                index = str(i)
            self.parent.convert(path + '[' + index + ']', item)
