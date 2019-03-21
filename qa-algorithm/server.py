import sys
sys.path.append("/home/user/kbqa2019/code-convention-robot")
from flask import Flask, request
from flask import jsonify
from flask_cors import *
from sub_graph import execution, construction
import json
import sparql
import getopt
from checkCode import checkstyle

app = Flask(__name__,static_url_path='')
CORS(app, supports_credentials=True)

@app.route('/test')
def hello_world():
    print sparql.full_text_search('declare variables in the smallest scope possible')
    return 'hello'

@app.route('/ordinary')
def ordinary():
    return app.send_static_file('ordinary.html')


@app.route('/advance')
def advance():
    return app.send_static_file('advance.html')


@app.route('/code')
def code():
    return app.send_static_file('code.html')

# query by uri
@app.route('/accurate', methods=['POST'])
def search_by_uri():
    params = request.json
    url = params['url']
    results = sparql.search_by_url(url)
    try:
        if results:
            re_dict = {'data': results, 'status': 'success'}
        else:
            re_dict = {'status': 'fail'}
    except Exception:
        re_dict = {'status': 'fail', 'error_msg': "Invalid uri!"}

    return make_response(re_dict)


# common query
@app.route('/ordinarySearch', methods=['POST'])
def query():
    params = request.json
    question = params['question']
    command = question.split(' ')
    command = merge_blank(command)
    try:
        opts, args = getopt.getopt(command, "n:r:b:w:e:")
        params = {}
        for name, value in opts:
            if name == '-n':
                params['name'] = value
            elif name == '-r':
                params['rule'] = value
            elif name == '-b':
                params['benefit'] = value
            elif name == '-w':
                params['weakness'] = value
            elif name == '-e':
                params['exception'] = value
        if params:
            return search_by_params(params)
    except getopt.GetoptError:
        print('get opt error')
    re_dict = {}
    if contain_zh(question):
        re_dict['status'] = 'fail'
        re_dict['error_msg'] = "Please enter english question~ "
        return json.dumps(re_dict)

    results = execution.execute(str(question))
    if results == -1:
        re_dict['status'] = 'fail'
    else:
        re_dict['data'] = results
        re_dict['status'] = 'success'
    construction.clear_global_variables()
    return make_response(re_dict)


# query similar entities
@app.route('/similar', methods=['POST'])
def query_similar():
    params = request.json
    uri = str(params['url'])
    results = sparql.search_similar(uri)
    re_dict = {}
    try:
        if results == -1:
            re_dict['status'] = 'fail'
        else:
            re_dict['data'] = results
            re_dict['status'] = 'success'
    except Exception:
        re_dict['status'] = 'fail'
        re_dict['error_msg'] = "Can't find similar entities"
    return make_response(re_dict)


# advanced search by idiom
@app.route('/advanceSearch', methods=['POST'])
def advanced_search():
    return search_by_params(request.json)


@app.route('/checkCode', methods=['POST'])
def check_code():
    params = request.json
    code = str(params['code'])
    re_dict = {}
    if code == None:
        re_dict['status'] = 'fail'
        re_dict['error_msg'] = "Code can't be empty!"
    else:
        try:
            results = checkstyle.checkCode(code)
            re_dict['data'] = results
            re_dict['status'] = 'success'
        except Exception:
            re_dict['status'] = 'fail'
            re_dict['error_msg'] = "Ops! An internal error has occurred."
    return make_response(re_dict)


def contain_zh(word):
    for ch in word:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def search_by_params(params):
    name = rule = benefit = weakness = exception = None

    if 'name' in params:
        name = str(params['name'])
    if 'rule' in params:
        rule = str(params['rule'])
    if 'benefit' in params:
        benefit = str(params['benefit'])
    if 'weakness' in params:
        weakness = str(params['weakness'])
    if 'exception' in params:
        exception = str(params['exception'])

    results = sparql.advanced_search(name, rule, benefit, weakness, exception)
    re_dict = {}
    try:
        if results == -1:
            re_dict['status'] = 'fail'
            re_dict['error_msg'] = "Sorry, please check your input."
        else:
            re_dict['data'] = results
            re_dict['status'] = 'success'
    except Exception:
        re_dict['status'] = 'fail'
        re_dict['error_msg'] = "Sorry, we can't find the answer."
    return make_response(re_dict)


# for allow cross-region
def make_response(result_dic):
    response = jsonify(result_dic)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


def merge_blank(arr):
    i = 0
    while i < len(arr):
        if arr[i].startswith("'"):
            j = i
            while j < len(arr) and not arr[j].endswith("'"):
                j += 1
            param = ' '.join(arr[i:j + 1])[1:-1]
            arr[i] = param
            del arr[i + 1:j + 1]
        i += 1
    return arr
