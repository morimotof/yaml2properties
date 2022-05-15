import argparse
import io
import os.path
import re
import sys
import yaml
#import traceback


# yamlファイルを読み込んでproperties形式で出力する
class Yaml2Properties:
    # ファイル名と引数オプションを使って生成する
    def __init__(self, fileName, args):
        self.fileName = fileName
        self.args = args

    # このオブジェクトを生成して値として返すファクトリメソッド
    @classmethod
    def of(cls, fileName, args):
        obj = Yaml2Properties(fileName, args)
        return obj

    # メイン
    @classmethod
    def  main(cls,argv):

        # 標準入出力の文字コードを設定
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

        # 引数の処理
        args = Yaml2Properties.parse_args(argv)

        # 与えられたファイル名すべてを処理する
        for fileName in args.fileName:
            try:
                Yaml2Properties.of(fileName, args).convert()
            except Exception as e:
                print('error:' + str(e))

    @classmethod
    def parse_args(cls, args):
        parser = argparse.ArgumentParser(description='Yaml to Properties')
        parser.add_argument('fileName', nargs='*',  default=['stdin'],help='ex:yaml-file.yml or stdin')
        parser.add_argument(
            '-f',
            '--nofilename',
            action='store_true',
            help='no file name')
        parser.add_argument(
            '-i',
            '--noindex',
            action='store_true',
            help='no index of array')
        parser.add_argument(
            '-v',
            '--novalue',
            action='store_true',
            help='no data value')
        return parser.parse_args(args)

    # 変換開始
    def convert(self):
        if self.fileName == 'stdin':
            data = yaml.load(sys.stdin,Loader=yaml.SafeLoader)
            self.y2p('',data,'.')
        else:
            # ファイルが存在するかどうかチェック
            if not os.path.isfile(self.fileName):
                raise RuntimeError('file not found:' + self.fileName)
            # ファイルを開く
            with open(self.fileName, 'r', encoding='utf-8') as f:
                # PyYAMLを使ってyamlファイルをオブジェクトに変換する
                data = yaml.load(f, Loader=yaml.SafeLoader)
                # オブジェクトの構造を解析して、properties形式で出力する
                self.y2p('', data, '.')

    # targetに含まれるオプジェクトを解析する
    # オブジェクトが含まれる場合は再帰的に呼び出す
    def y2p(self, path, target, separator):
        try:
            # 辞書型
            if isinstance(target, dict):
                for key, value in target.items():
                    self.y2p(path + separator + str(key), value, separator)
            # None型
            elif target is None:
                self.print_line(path, '')
            # list型
            elif isinstance(target, list):
                for i, item in enumerate(target):
                    if(self.args.noindex):
                        index = ''
                    else:
                        index = str(i)
                    self.y2p(path + '[' + index + ']', item, separator)
            # アトリビュートを持つ
            elif hasattr(target, '__dict__'):
                for key, value in target.__dict__.items():
                    self.y2p(path + separator + str(key), value, separator)
            # アトリビュートを持たない、すなわち値
            else:
                if (not self.args.novalue):
                    self.print_line(path, target)
                else:
                    self.print_line(path,'')
        # 再帰の呼び出し元で受けたRuntimeErrorは呼び出し先で発生させたものなので
        # そのまま通知する
        except RuntimeError as e:
            raise RuntimeError(e)
        except Exception as e:
            #traceback.print_tb(sys.exc_info())
            raise RuntimeError(
                'unknown object type:' +
                "{0}".format(type(e)) +
                '\n,at:' +
                path +
                '\n,target:' +
                str(target))

    # pathとtarget(値)をフォーマットする
    def print_line(self, path, target):
        # ファイル名を出力しない
        if self.args.nofilename:
            f = ''
        # ファイル名を出力する
        else:
            f = self.fileName + ':'
        # pathから先頭の'.'を取り除く
        p = re.sub('^\\.', '', path)
        # targetに含まれる改行を置き換える
        t = str(target).replace('\n', '\\n')
        self.printout(f + p + '=' + t)

    # 出力する
    def printout(self, msg):
        print(msg)

if __name__ == '__main__':
    Yaml2Properties.main(sys.argv[1:])
