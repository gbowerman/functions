import logging
import requests

import azure.functions as func

HEADERS = {'Content-Type': 'text/html'}
BASE_PATH = 'https://raw.githubusercontent.com/gbowerman/functions/master/guyfuncproj/htdocs'

def wget_path(path):
    if path[-1] == '/':
        path += 'index.html'
    full_path = BASE_PATH + path
    response = requests.get(full_path)
    return response.content

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    path = req.params.get('path')
    if not path:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            path = req_body.get('path')

    if path:
        html_path = wget_path(path)
        return func.HttpResponse(html_path, headers=HEADERS)
    else:
        return func.HttpResponse(
             "Please pass a path on the query string or in the request body",
             status_code=400
        )
