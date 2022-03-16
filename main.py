import html_to_json
import requests


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


def get_parsed_data_by_url(url: str) -> dict:
    """return parsed html page as python dict"""
    try:
        response = requests.get(url=url, headers=HEADERS)
        if response.status_code == 200:
            html = response.text
            parsed_html = html_to_json.convert(html)

            return parsed_html
        return {}

    except Exception as err:
        raise err
