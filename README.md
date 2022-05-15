## 初めに

YAMLファイルは構造化されていて書きやすい反面、項目を探すのに苦労することがある。
たとえば、

```yaml:sample.yml
service: 
  apply-date: 2021-06-19
application: 
  apply-date: 2021-06-20
```
というファイルがあって、applicationのapply-dateの値を探したいとき、grepで検索すると、

```grep:結果
$ grep apply-date sample.yml
  apply-date: 2021-06-19
  apply-date: 2021-06-20
```
という結果になって、ヒットしたapply-dateがserviceかapplicationのどちらのものなのか、わからないということがある。

一方、YAMLを使う前によく使っていたproperties形式では、

```properties:sample.properties
service.apply-date=2021-06-19
application.apply-date=2021-06-20
```
となっており、上記のような検索をするには便利である。

そこで、YAMLファイルを読み込んでProperties形式(風)に出力するプログラムを探してみたが、見つからなかったので、自作することにした。当方、Pythonでのプログラムつくりは経験がなかったので、勉強を兼ねてPythonで組んでみることにしようと思う。

以下のような仕様で作成する。

- YAMLファイルの読み込みはPyYAMLを使う
- 複数ファイル扱えるようにし、出力にファイル名を付加する、しないを指定できるようにする
- 検索が主な目的なので、文字列とか数値などの区別はしない
- シーケンスのindexを付ける、付けないを指定できるようにする(順番を無視したい場合を考慮する)
- 値に改行が含まれる場合は、改行を"\n"という文字列に置き換える
- 値に「#'"」などが含まれていても、そのまま出力する
- 値に漢字が含まれていてもそのまま出力する(unicode変換はしない)
- ~~標準入力を対象にしない~~
- 実行環境は~~Python 3.7.3~~ Python 3.8.3(他は検証しない)

## プログラムについて

中心となるのは、メソッドy2pである。targetは、YAMLファイルをパースして得られたオブジェクトで、YAMLの構造を表現した構造になっており、辞書型、リスト型、アトリビュートを持つオブジェクト、アトリビュートを持たないオブジェクトに部類される。アトリビュートを持たないオブジェクト以外は、ノードをもち階層を表現していて、ノードにはさらにオブジェクトが含まれる。この階層構造をたどると、最終的にはアトリビュートを持たないオブジェクトにたどり着く。アトリビュートを持たないオブジェクトは値であり、これまでたどったノード名とともに出力する。

## PyYAMLのインストール

```
$ python -m pip install pyyaml

$ python -m pip freeze | grep -i PyYAML
PyYAML==5.3.1
```
## 起動方法

```
python yaml2properties.py [-f] [-i] [-v] [file1.yml]

-f --nofilename ファイル名を出力しない
-i --noindex 配列番号を出力しない
-v --novalue 値を出力しない
[file1.yml]... ファイル名(複数可)。ファイル名を指定しない場合は標準入力から。
```

## ファイルフォーマット

ファイルフォーマットはYAML形式とjson形式を受け付ける。
たとえば、jsonを返すAPIがある場合は、
```
$ curl -s https:/api.github.com/usrs/morimotof | python yaml2properties.py
stdin:message=Not Found
stdin:documentation_url=https://docs.github.com/rest
```
とできる。


## テスト

### テストデータ

```yaml:sample.yml
simple:
  string: sample
  kanji: 漢字を表示する
  integer: 123
  float: 4.56
  true: true
  false: false
  date: 2015-7-27
  blank:
  quoted:
    integer: "789"
    true: "true"
complex:
  - name: test1
    age: 10
  - name: test2
    age: 20
  - name: test3
    age: 30
```

### unit テスト

```
$ python -m coverage run test_yaml2properties.py -v
test_parse_args (__main__.TestYaml2properties) ... ok
test_yaml2propertie_print_line (__main__.TestYaml2properties) ... ok
test_yaml2propertie_printout (__main__.TestYaml2properties) ... ok
test_yaml2propertie_y2p (__main__.TestYaml2properties) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.009s

OK
```

### 実行結果

```bash:実行結果
$ python --version
Python 3.8.3
$ python yaml2properties.py sample.yml
sample.yml:simple.string=sample
sample.yml:simple.kanji=漢字を表示する
sample.yml:simple.integer=123
sample.yml:simple.float=4.56
sample.yml:simple.True=True
sample.yml:simple.False=False
sample.yml:simple.date=2015-7-27
sample.yml:simple.blank=
sample.yml:simple.quoted.integer=789
sample.yml:simple.quoted.True=true
sample.yml:complex[0].name=test1
sample.yml:complex[0].age=10
sample.yml:complex[1].name=test2
sample.yml:complex[1].age=20
sample.yml:complex[2].name=test3
sample.yml:complex[2].age=30
```
## カバレッジ

### coverage のインストール

```
$ python -m pip install coverage

$ python -m pip freeze | grep -i coverage
coverage==6.3.3
```

### coverage の実行

```
$ python -m coverage run test_yaml2properties.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.009s

OK

$ python -m coverage report
Name                      Stmts   Miss  Cover
---------------------------------------------
test_yaml2properties.py      36      0   100%
yaml2properties.py           76     12    84%
---------------------------------------------
TOTAL                       112     12    89%

$ python -m coverage html
Wrote HTML report to htmlcov\index.html
```

### 標準入力からのunitテストが出来ていない

![image](https://user-images.githubusercontent.com/22857955/168456624-4adfe2f3-412f-4558-86b7-8de22f81ff6b.png)

