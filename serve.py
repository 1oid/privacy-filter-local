from flask import Flask, request, jsonify
import json
import os
from opf._api import OPF

os.environ['OPF_MOE_TRITON'] = ''

app = Flask(__name__)

@app.route("/redactor", methods=["POST"])
def redactor():
    if request.method == 'POST':
        json_data = json.loads(request.data)
        text = json_data.get('text', None)

        if not text:
            return jsonify({"error": "No text provided"})

        redc = OPF(
            device='mps',
            decode_mode='viterbi',
            output_mode='typed',
            discard_overlapping_predicted_spans=False,
        )
        result = redc.redact(text)
        return jsonify(result)
    return "ok"