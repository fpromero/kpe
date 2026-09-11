#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, request
from transformers import BertModel
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

@app.route('/params')
def kpe():
    text = request.args.get('text', 'text not found')

    result = kpe_control.key_phrases_extraction(
        text,
        language="en",
        clustering_option="fcm",
        top_topic=0.75,
        top_kp=5,
        quantifier="pasi",
        select_option="2",
        bert_model=get_bert_model(),
    )
    key_phrases = result[2]

    output = "From text: " + text + "\n\n" + "Keyphrases: " + ",".join(key_phrases)
    return output


if __name__ == '__main__':
    # Run with: python -m ftm_kpe.legacy.kpe_flask
    #Example1: http://localhost: 5002/v2/param1_value/param2_value
    #Example2: http://localhost:5002/v2/param1_value/BAD_RESPONSE
    app.run(debug=True)
