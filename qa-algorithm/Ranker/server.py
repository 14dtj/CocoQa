import sys
sys.path.append("/home/user/kbqa2019/ranker")
from flask import Flask, request
from flask import jsonify
from flask_cors import *
import executor
import json

app = Flask(__name__, static_url_path='')
CORS(app, supports_credentials=True)
with open('data/template.json', "r") as f:
    template_questions = json.load(f)


# common query
@app.route('/template', methods=['POST'])
def query():
    params = request.json
    question = params['question']
    if question in template_questions:
        return make_response(template_questions[question])
    re_dict = {}
    if contain_zh(question):
        re_dict['status'] = 'fail'
    else:
        data = executor.execute(question)
        if data is None:
            re_dict['status'] = 'fail'
        else:
            re_dict['status'] = 'success'
            re_dict['data'] = data
    return make_response(re_dict)


def contain_zh(word):
    for ch in word:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


# for allow cross-region
def make_response(result_dic):
    response = jsonify(result_dic)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return response


if __name__ == '__main__':
    app.run(debug=True)

