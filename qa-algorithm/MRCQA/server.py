from flask import Flask, request

from utils.mrc_input import mrc

app = Flask(__name__)
m = mrc("config/id19.yaml")

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/mrcqa", methods=['POST'])
def mrcqa():
    params = request.json
    contexts = params['contexts']
    question = params['question']
    questions = []
    for i in range(len(contexts)):
        questions.append(question)
    return m.mrcqa_batch(contexts,questions)