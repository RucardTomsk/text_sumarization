# -*- coding: utf-8 -*-
import logging

from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from baseline_summarizer import Summarizer

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', filemode='a')

logger = logging.getLogger(__name__)

app = Flask(__name__)

_sum = Summarizer()

cors = CORS(app, resource={
    r"/*": {"origins": "*"}
})


@app.route('/summarize/<string:language_iso>', methods=['POST'])
def summarize(language_iso):
    if not request.json or not 'request_text' in request.json:
        logging.info(f"BAD REQUEST: not request_text")
        abort(400)
    if language_iso != "en" and language_iso != "ru":
        logging.info(f"BAD REQUEST: bad language")
        abort(400)
    language = "ENGLISH"
    if language_iso == "en":
        language = "ENGLISH"
    if language_iso == "ru":
        language = "RUSSIAN"
    finale_text = _sum.summarize(request.json['request_text'], language)
    logging.info(f"Text summarizer")
    return jsonify({'sum_text': finale_text})


if __name__ == '__main__':
    app.run(debug=True)
