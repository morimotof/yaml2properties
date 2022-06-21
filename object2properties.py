import re
# handler
import handlers.dict_handler as DH
import handlers.none_handler as NH
import handlers.list_handler as LH
import handlers.attr_handler as AH
import handlers.value_handler as VH
#import sys
#import traceback

# Objectの構造をproperties形式で出力する
class Object2properties:

    # ファイル名と引数オプションを使って生成する
    def __init__(self, fileName, args):
        self.args = args
        # ファイル名を出力しない
        if self.args.nofilename:
            self.fileName = ''
        # ファイル名を出力する
        else:
            self.fileName = fileName + ':'
        # handlerを登録する
        self.handlers=[
            DH.DictHandler(self),
            NH.NoneHandler(self),
            LH.ListHandler(self),
            AH.AttrHandler(self),
            VH.ValueHandler(self), #これは最後に定義すること
        ]
    
    # targetに含まれるオプジェクトを解析する
    # 子オブジェクトが含まれる場合はhandler内から再帰的にconvertを呼び出す
    def convert(self, path, target):
        for handler in self.handlers:
            # いずれかのhandlerで処理する
            # handlerで処理できる場合はtestでTrueが返る
            if handler.test(target):
                handler.action(path,target)
                break

    # pathとtarget(値)をフォーマットする
    def print_line(self, path, target):
        # pathから先頭のセパレータを取り除く
        if len(self.args.separator) >0 :
            path = re.sub('^\\'+self.args.separator, '', path)
        target = str(target).replace('\n', '\\n')
        self.printout(self.fileName + path + '=' + target)

    # 出力する
    def printout(self, msg):
        print(msg)
