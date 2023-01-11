import os
import json
import requests

from dotenv import load_dotenv

def generate_qmd_header(content: dict, form_data: dict):

    if form_data['thumbnail'] == None:
        form_data['thumbnail'] = 'https://upload.wikimedia.org/wikipedia/commons/5/59/Empty.png'

    content = {
                'title': form_data.get('title', ''),
                'description': form_data.get('overview', ''),
                'image': form_data.get('thumbnail', 'https://upload.wikimedia.org/wikipedia/commons/5/59/Empty.png'),
                'categories': [category.title for category in form_data['categories']] ,
                'format': {
                    'html':{
                        'df-print': 'paged',
                        'toc': True
                    }
                }
            }

    content['params'] = {
                'overview' : form_data['overview'],

                'scholar_url': form_data.get('citation', ''),
                
                'pdf_url': form_data.get('pdf', ''),
                
                'poster_url': form_data.get('poster', ''),

                'code_url': form_data.get('code', ''),

                'supplement_url': form_data.get('supplement', ''),

                'slides_url': form_data.get('slides', '')
            }

    for idx, author in enumerate(form_data['authors'], 1):
                content['params'][f'author_{idx}'] = {
                    'name': author.user,
                    'url': author.user_url
                }

    return content

def generate_page_content(content, filepath: str):

    with open(filepath, 'a') as fp:
        fp.write('\n## Tldr \n')
        overview = content['params']['overview']
        fp.write(f'{overview}\n')
        fp.write('\n## Paper-authors\n')
        for param in content['params']:
            if param.startswith('author'):
                fp.write(f'- [{{{{< meta params.{param}.name >}}}}]({{{{< meta params.{param}.url >}}}})\n')
        
        fp.write('\n## More Resources\n')

        print(content['params'])

        if content['params']['scholar_url']:
            fp.write('[![](https://img.shields.io/badge/citation-scholar-9cf?style=flat.svg)]({{< meta params.scholar_url >}})\n')
        
        if content['params']['pdf_url']:
            fp.write('[![](https://img.shields.io/badge/PDF-green?style=flat)]({{< meta params.pdf_url >}})\n')
        if content['params']['supplement_url']:
            fp.write('[![](https://img.shields.io/badge/supplement-yellowgreen?style=flat)]({{< meta params.supplement_url >}})\n')
        if content['params']['slides_url']:
            fp.write('[![](https://img.shields.io/badge/blog-blue?style=flat)]({{< meta params.slides_url >}}\n')
        if content['params']['pdf_url']:
            fp.write('[![](https://img.shields.io/badge/slides-ff69b4?style=flat)]({{< meta params.pdf_url >}})\n')
        if content['params']['poster_url']:
            fp.write('[![](https://img.shields.io/badge/poster-yellow?style=flat)]({{< meta params.poster_url >}})\n')
        if content['params']['code_url']:
            fp.write('[![](https://img.shields.io/badge/code-blueviolet?style=flat)]({{< meta params.code_url >}})\n')

def create_push_request(file_path: str):

    load_dotenv()

    user = os.getenv('GH_USER')
    auth_token = os.getenv('GH_TOKEN')
    repo = os.getenv('GH_REPOSITORY')

    header = {
        'Authorization': 'Bearer ' + auth_token
    }

    sha_last_commit_url =  f'https://api.github.com/repos/{user}/{repo}/branches/main'
    response = requests.get(sha_last_commit_url, headers= header)
    print(response.json())
    sha_last_commit = response.json()['commit']['sha']

    url = f'https://api.github.com/repos/{user}/{repo}/git/commits/{sha_last_commit}'
    response = requests.get(url, headers=header)
    sha_base_tree = response.json()['sha']

    with open(file_path, 'r') as fp:
        content = fp.read()


    data = {
    "content": content,
    "encoding": 'utf-8'
    }

    header = {
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + auth_token
    }

    url = 'https://api.github.com/repos/DelmiroDaladier/icr/git/blobs'
    response = requests.post(url, json.dumps(data), headers=header)
    blob_sha = response.json()['sha']


    data = {
        'base_tree': sha_base_tree,
        'tree': [
            {
            'path': 'content/test/index.qmd',
            'mode': '100644',
            'type': 'blob',
            'sha': blob_sha
            }
        ]
    }

    url = 'https://api.github.com/repos/Delmirodaladier/icr/git/trees'
    response = requests.post(url, json.dumps(data), headers=header)

    tree_sha = response.json()['sha']

    data = {
        "message": "Add new files at once programatically",
        "author": {
            "name": "Delmiro Daladier",
            "email": "daladiersampaio@gmail.com"
        },
        "parents": [
            sha_last_commit
        ],
        "tree": tree_sha
    }

    url = f'https://api.github.com/repos/DelmiroDaladier/icr/git/commits'
    response = requests.post(url, json.dumps(data), headers=header)
    new_commit_sha = response.json()['sha']


    data = {
        "ref": "refs/heads/main",
        "sha": new_commit_sha
    }

    url = f'https://api.github.com/repos/DelmiroDaladier/icr/git/refs/heads/main'
    response = requests.post(url, json.dumps(data), headers=header)
