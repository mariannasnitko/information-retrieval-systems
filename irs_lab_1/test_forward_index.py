import unittest
from unittest.mock import patch
import os
import json

import forward_index

class TestToolset(unittest.TestCase):
    def __setup_input(self):
        file1 = open('.tmp1.txt', 'w')
        file1.write('Valuable information to search')
        file1.close()
        file2 = open('.tmp2.txt', 'w')
        file2.write('Some other information')
        file2.close()

    def __remove_leftovers(self):
        os.remove('.tmp1.txt')
        os.remove('.tmp2.txt')
        os.remove('.tmp.json')

    def test_index(self):
        self.__setup_input()
        forward_index.index('.tmp1.txt', db_file_loc='.tmp.json')
        file = open('.tmp.json')
        result = json.load(file)
        expected = {'.tmp1.txt': ['valuable', 'information', 'search']}
        self.assertEqual(result, expected)
        self.__remove_leftovers()

    def test_search(self):
        self.__setup_input()
        forward_index.index('.tmp1.txt', '.tmp.json')
        forward_index.index('.tmp2.txt', '.tmp.json')
        query = 'Valuable information'
        result = forward_index.search(query, db_file_loc='.tmp.json')
        expected = {'valuable': ['.tmp1.txt'], 'information': ['.tmp1.txt', '.tmp2.txt']}
        self.assertEqual(result, expected)
        self.__remove_leftovers()

    def test_search_fail(self):
        self.__setup_input()
        forward_index.index('.tmp1.txt', '.tmp.json')
        forward_index.index('.tmp2.txt', '.tmp.json')
        query = 'something'
        result = forward_index.search(query, db_file_loc='.tmp.json')
        expected = {'something': []}
        self.assertEqual(result, expected)
        self.__remove_leftovers()

if __name__ == '__main__':
    unittest.main()