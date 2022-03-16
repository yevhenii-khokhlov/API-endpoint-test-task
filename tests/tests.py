import unittest
from dataclasses import dataclass
from unittest.mock import patch

from main import get_parsed_data_by_url


@dataclass
class MockResponseObject:
    text: str
    status_code: int


class GetParsedDataByUrlTest(unittest.TestCase):
    def setUp(self) -> None:
        self.url = 'fake_url'

        with open("test_1.html") as fp_1:
            html_1 = fp_1.read()
            self.response_ok_1 = MockResponseObject(html_1, 200)
            self.response_not_found = MockResponseObject(html_1, 404)

        with open("test_2.html") as fp_2:
            html_2 = fp_2.read()
            self.response_ok_2 = MockResponseObject(html_2, 200)

    @patch('main.requests.get')
    def test_call_url_html_1(self, mock_get):
        mock_get.return_value = self.response_ok_1
        expected = {'html': [{'_attributes': {'lang': 'en'}, 'head': [{'title': [{'_value': "Head's title"}]}], 'body': [{'p': [{'_attributes': {'class': ['title']}, 'b': [{'_value': "Body's title"}]}, {'_attributes': {'class': ['story']}, '_value': 'line begins', 'a': [{'_attributes': {'href': 'http://example.com/element1', 'class': ['element'], 'id': 'link1'}, '_value': '1'}, {'_attributes': {'href': 'http://example.com/element2', 'class': ['element'], 'id': 'link2'}, '_value': '2'}, {'_attributes': {'href': 'http://example.com/avatar1', 'class': ['avatar'], 'id': 'link3'}, '_value': '3'}]}, {'_value': 'line ends'}]}]}]}
        res = get_parsed_data_by_url(self.url)
        self.assertEqual(res, expected)

    @patch('main.requests.get')
    def test_call_url_html_2(self, mock_get):
        mock_get.return_value = self.response_ok_2
        expected = {'_value': 'html', 'html': [{'_attributes': {'lang': 'ua'}, 'body': [{'div': [{'_attributes': {'style': 'position:relative;'}, 'div': [{'_attributes': {'style': 'opacity:0.5;position:absolute;left:50px;top:-30px;width:300px;height:150px;background-color:#40B3DF'}}, {'_attributes': {'style': 'opacity:0.3;position:absolute;left:120px;top:20px;width:100px;height:170px;background-color:#73AD21'}}, {'_attributes': {'style': 'margin-top:30px;width:360px;height:130px;padding:20px;border-radius:10px;border:10px solid #EE872A;font-size:120%;'}, 'h1': [{'_value': 'CSS = Styles and Colors'}], 'div': [{'_attributes': {'style': 'letter-spacing:12px;font-size:15px;position:relative;left:25px;top:25px;'}, '_value': 'Manipulate Text'}, {'_attributes': {'style': 'color:#40B3DF;letter-spacing:12px;font-size:15px;position:relative;left:25px;top:30px;'}, '_value': 'Colors,', 'span': [{'_attributes': {'style': 'background-color:#B4009E;color:#ffffff;'}, '_value': 'Boxes'}]}]}]}]}]}]}
        res = get_parsed_data_by_url(self.url)
        self.assertEqual(res, expected)

    @patch('main.requests.get')
    def test_call_url_404(self, mock_get):
        mock_get.return_value = self.response_not_found
        expected = {}
        res = get_parsed_data_by_url(self.url)
        self.assertEqual(res, expected)

    @patch('main.requests.get', side_effect=Exception)
    def test_call_url_exception(self, mock_get):
        with self.assertRaises(Exception):
            get_parsed_data_by_url(self.url)
