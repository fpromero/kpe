#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, Response, request, jsonify
from transformers import BertModel
import json
from . import kpe_control

app = Flask(__name__)
_bert_model = None


def get_bert_model():
        """Load the legacy embedding model once, on first use."""
        global _bert_model
        if _bert_model is None:
                _bert_model = BertModel.from_pretrained(
                        "bert-base-uncased", output_hidden_states=True
                )
        return _bert_model

@app.route('/akpe/<path:text>', methods=['GET','POST'])
def kpe(text):
        print(text)
        result = kpe_control.key_phrases_extraction(
                text, language="en", clustering_option="fcm", top_topic=0.75, top_kp=15,
                quantifier="pasi", select_option="2", bert_model=get_bert_model()
        )
        key_phrases = result[2]
        kp_relevance = result[3]

        print(",".join(key_phrases))
        output = {}
        for kp in key_phrases:
            output.update({kp: kp_relevance[kp]})

        response_pickled = json.dumps(output)
        return Response(response=response_pickled, status=200, mimetype="application/json")


@app.route('/akpe', methods=['GET','POST'])
def scored_kpe():
        texts = request.get_json()
        text = texts['text1']
        print(text)
        result = kpe_control.key_phrases_extraction(
                text, language="en", clustering_option="fcm", top_topic=0.75, top_kp=15,
                quantifier="pasi", select_option="2", bert_model=get_bert_model()
        )
        key_phrases = result[2]
        kp_relevance = result[3]
        print(",".join(key_phrases))
        output = {}
        for kp in key_phrases:
            output.update({kp: kp_relevance[kp]})

        response_pickled = json.dumps(output)
        return Response(response=response_pickled, status=200, mimetype="application/json")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
