# © 2020-2023 Didotech srl <info@didotech.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
import requests
from requests.exceptions import ConnectionError


def get_oca_repositories():
    #The api needs to be iterated through pages because it returns max only 100 records at a time
    page_counter = 1
    list_repos = []
    tup = ('','')
    """This is the personal access token used to make requests to the github api, which allows us to make 30 requests per minute.
    If an access token is not provided, you are limited to max. 60 requests per hour and if you exceed that limit a 403 error
    is returned"""
    #oauth_token = ''
    #header = {'Authorization': f'token {oauth_token}'}
    while True:
        try:
            req = requests.get(f'https://api.github.com/orgs/OCA/repos?per_page=100&page={page_counter}')
            if not req.json() or req.status_code == 403:
                break
            else:
                list_repos = list_repos + req.json()
            page_counter += 1
            sorted_list = sorted(list_repos, key=lambda k: k['name'])
            tup = tuple([(repo['name'], repo['name']) for repo in sorted_list])
        except ConnectionError as e:
            break
        except Exception as e:
            pass

    return tup
