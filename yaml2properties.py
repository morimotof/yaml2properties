import argparse
import io
import os.path
import sys
import object2properties as O2P
import yaml as YML

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
        parser.add_argument(
            '-s',
            '--separator',
            default='.',
            help='separator value')
        return parser.parse_args(args)

    # 変換開始
    def convert(self):
        o2p = O2P.Object2properties(self.fileName, self.args)
        if self.fileName == 'stdin':
            data = YML.load(sys.stdin,Loader=YML.SafeLoader)
            o2p.convert('',data)
        else:
            # ファイルが存在するかどうかチェック
            if not os.path.isfile(self.fileName):
                raise RuntimeError('file not found:' + self.fileName)
            # ファイルを開く
            with open(self.fileName, 'r', encoding='utf-8') as f:
                # PyYAMLを使ってyamlファイルをオブジェクトに変換する
                data = YML.load(f, Loader=YML.SafeLoader)
                # オブジェクトの構造を解析して、properties形式で出力する
                o2p.convert('', data)

if __name__ == '__main__':
    Yaml2Properties.main(sys.argv[1:])
