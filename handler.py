import os
from opf._api import OPF
import runpod

os.environ['OPF_MOE_TRITON'] = ''


def handler(event):
    """
    This is the handler function that will be called by RunPod serverless.
    """

    job_input = event.get('input', None)

    if job_input is None:
        return {
            "status": 500,
            "message": "input is null"
        }

    text = job_input.get('text', None)
    redc = OPF(
        device='mps',
        decode_mode='viterbi',
        output_mode='typed',
        discard_overlapping_predicted_spans=False,
    )
    result = redc.redact(text)

    return {
        "resp": result,
        "status": 200,
        "message": "success"
    }