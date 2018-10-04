'''Azure Functions github webserver example'''
import logging
import requests

import azure.functions as func


HEADERS = {'Content-Type': 'text/html'}

# set this to base folder for HTML files
BASE_PATH = 'https://raw.githubusercontent.com/gbowerman/functions/master/guyfuncproj/htdocs'

def wget_path(path):
    '''Convert Azure Function path argument into a github URL and get the file'''
    # support '/' in HTML path
    if path[-1] == '/':
        path += 'index.html'
    full_path = BASE_PATH + path
    
    # get the guthub file and return contents
    logging.info(full_path)
    try:
        response = requests.get(full_path)
        return response.content
    except requests.exceptions.RequestException as err:
        # handle HTTP errors like 404 and return error text to browser
        return err
   

def main(req: func.HttpRequest) -> func.HttpResponse:
    '''Called when Azure function triggered'''
    logging.info('Python HTTP trigger function processed a request.')

    # get HTTP trigger argument 'path'
    path = req.params.get('path')
    if not path:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            path = req_body.get('path')

    if path:
        # convert path into github raw URL and get file
        html_path = wget_path(path)
        # return HTML file as function response
        return func.HttpResponse(html_path, headers=HEADERS)
    else:
        return func.HttpResponse(
             "Please pass a path on the query string or in the request body",
             status_code=400
        )
