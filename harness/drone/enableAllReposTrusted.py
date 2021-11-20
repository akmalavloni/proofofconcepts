# potentially for https://harnesssupport.zendesk.com/agent/tickets/20499
import json
import requests


api_token = 'api token'
api_url_base = 'https://drone.server.url.com/api/'
headers = {'Content-Type': 'application/json',
           'Authorization': 'Bearer {0}'.format(api_token)}

def response_status(response):
  if response.status_code >= 500:
    print('[!] [{0}] Server Error'.format(response.status_code))
    return None
  elif response.status_code == 404:
    print('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url))
    return None
  elif response.status_code == 401:
    print('[!] [{0}] Authentication Failed'.format(response.status_code))
    return None
  elif response.status_code == 400:
    print('[!] [{0}] Bad Request'.format(response.status_code))
    return None
  elif response.status_code >= 300:
    print('[!] [{0}] Unexpected Redirect'.format(response.status_code))
    return None
  elif response.status_code == 200:
    setResponseStatus = json.loads(response.content.decode('utf-8'))
    return setResponseStatus
  else:
    print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(response.status_code, response.content))
  return None

def check_all_repos():
  api_url = '{0}user/repos'.format(api_url_base)

  response = requests.get(api_url, headers=headers)

  return response_status(response)

def set_repo_as_trusted(slug):
  api_url = '{0}repos/{1}'.format(api_url_base, slug)

  response = requests.patch(api_url, headers=headers, data='{"trusted":true}')

  return response_status(response)

def set_repos_as_trusted():
  repo_list = check_all_repos()

  for repo in repo_list:
    if repo["trusted"] is False:
      set_repo_as_trusted(repo["slug"])

set_repos_as_trusted()
print(json.dumps(check_all_repos(), indent=4))
