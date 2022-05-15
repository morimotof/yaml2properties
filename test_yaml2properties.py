import unittest
from unittest import mock
import yaml2properties
import datetime

class TestYaml2properties(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.outmap = {}
        cls.outlist = []

    def setUp(self):
        TestYaml2properties.outmap = {}
        TestYaml2properties.outlist = []

    # 引数の処理を検証する
    def test_parse_args(self):
        args = yaml2properties.Yaml2Properties.parse_args(['-f','-i','sample.yml'])

        assert args.nofilename == True
        assert args.noindex == True
        assert args.novalue == False
        assert args.fileName == ['sample.yml']

    def _mock_print_line(self, path, target):
        TestYaml2properties.outmap[path]=target
    
    # sample.ymlを変換した結果を検証する
    @mock.patch("yaml2properties.Yaml2Properties.print_line", new=_mock_print_line)
    def test_yaml2propertie_print_line(self):
        map = {
             '.simple.string':'sample'
            ,'.simple.kanji':'漢字を表示する'
            ,'.simple.integer':123
            ,'.simple.float':4.56
            ,'.simple.True':True
            ,'.simple.False':False
            ,'.simple.date':'2015-7-27'
            ,'.simple.blank':''
            ,'.simple.quoted.integer':'789'
            ,'.simple.quoted.True':'true'
            ,'.complex[0].name':'test1'
            ,'.complex[0].age':10
            ,'.complex[1].name':'test2'
            ,'.complex[1].age':20
            ,'.complex[2].name':'test3'
            ,'.complex[2].age':30
        }
        yaml2properties.Yaml2Properties.main(['-f','sample.yml'])
        for k in map:
            v1 = map[k]
            v2 = TestYaml2properties.outmap.get(k,"")
            assert v1 == v2, 'check key:' + k

    def _mock_printout(self, msg):
        TestYaml2properties.outlist.append(msg)

    # sample.ymlを変換した結果を検証する
    @mock.patch("yaml2properties.Yaml2Properties.printout", new=_mock_printout)
    def test_yaml2propertie_printout(self):
        list = [
             'sample.yml:simple.string=sample'
            ,'sample.yml:simple.kanji=漢字を表示する'
            ,'sample.yml:simple.integer=123'
            ,'sample.yml:simple.float=4.56'
            ,'sample.yml:simple.True=True'
            ,'sample.yml:simple.False=False'
            ,'sample.yml:simple.date=2015-7-27'
            ,'sample.yml:simple.blank='
            ,'sample.yml:simple.quoted.integer=789'
            ,'sample.yml:simple.quoted.True=true'
            ,'sample.yml:complex[0].name=test1'
            ,'sample.yml:complex[0].age=10'
            ,'sample.yml:complex[1].name=test2'
            ,'sample.yml:complex[1].age=20'
            ,'sample.yml:complex[2].name=test3'
            ,'sample.yml:complex[2].age=30'
        ]
        yaml2properties.Yaml2Properties.main(['sample.yml'])
        for k in list:
            assert k in TestYaml2properties.outlist, 'check key:' + k

    def _mock_printout2(self, msg):
        TestYaml2properties.outlist.append(msg)

    class Inner:
        def __init__(self):
            self.caption = 'inner class caption'
            self.date = datetime.date.today()

    @mock.patch("yaml2properties.Yaml2Properties.printout", new=_mock_printout2)
    def test_yaml2propertie_y2p(self):
        list = [
             'a.caption=inner class caption'
            ,'a.date=2022-05-15'
            ,'b[]=1'
            ,'c=string'
        ]
        args = yaml2properties.Yaml2Properties.parse_args(['-f','-i','test.yml'])
        yaml2properties.Yaml2Properties.of('test.yml',args).y2p('',{'a': self.Inner(),'b':[1],'c':'string'},'.')
        for k in list:
            assert k in TestYaml2properties.outlist, 'check key:' + k

if __name__ == "__main__":
    unittest.main()
