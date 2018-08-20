"""
Tests CNJ fetcher.
"""

import unittest
import fetcher_cnj
import requests

class CNJTestCase(unittest.TestCase):
    """
    tests the CNJ fetcher and associated methods
    """
    @classmethod
    def setUpClass(cls):
        cls.cnj = fetcher_cnj.Fetcher()
        cls.spreadsheet_mime_types = [
            'application/vnd.ms-excel', 
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ]
    
    def test_extracts_xls_paths(self):
        """
        _get_file_urls() returns list of links that point to .xls or .xlsx files
        """
        bogus_list_of_links = [
            'https://www.disney.com',
            'https://www.twitter.com',
            'https://www.example.com',
            'http://www.cnj.jus.br/files/conteudo/arquivo/2018/07/be0c705a49f8097edc22c95ddda1a6da.xlsx'
        ]
        clean_links = self.cnj._get_file_urls(links = bogus_list_of_links)

        self.assertEqual(len(clean_links), 1)

        self.assertIn(requests.get(url=clean_links[0]).headers['Content-Type'],
                      self.spreadsheet_mime_types)
        