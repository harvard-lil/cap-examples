from utils import *


def check_response(response, status_code=200):
    assert response.status_code == status_code


def test_get_api_url():
    """
    Make sure we get a functioning API URL
    """
    api_url = get_api_url()
    resp = requests.get(api_url)
    check_response(resp)

    content = resp.json()
    assert "citations" in content.keys()
    assert "cases" in content.keys()

