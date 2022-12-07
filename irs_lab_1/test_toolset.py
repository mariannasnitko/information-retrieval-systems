import json
import os
import unittest

import toolset

class TestToolset(unittest.TestCase):

    def test_read_txt(self):
        ref = 'some text'
        file_loc = '.tmp_file.txt'
        file = open(file_loc, 'w')
        file.write(ref)
        file.close()

        result = toolset.read_txt(file_loc)
        self.assertEqual(result, ref)
        
        os.remove(file_loc)

    def test_read_db(self):
        ref = {'key': 'value'}
        file_loc = '.tmp_file.json'
        file = open(file_loc, 'w')
        file.write(json.dumps(ref))
        file.close()

        result = toolset.read_db(file_loc)
        self.assertEqual(result, ref)

        os.remove(file_loc)

    def test_write_db(self):
        ref = {'key': 'value'}
        file_loc = '.tmp_file.json'
        toolset.write_db(file_loc, data=ref)

        file = open(file_loc, encoding='utf8')
        result = json.load(file)

        self.assertEqual(result, ref)

        os.remove(file_loc)

    def test_tokenize(self):
        ref = 'There is a part of text, that will be tokenized'
        expected = ['part', 'text', 'tokenized']
        result = toolset.tokenize(ref)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()