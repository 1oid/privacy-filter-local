from opf._api import OPF
import os

os.environ['OPF_MOE_TRITON'] = ''

redactor = OPF(
    device='mps',
    decode_mode='viterbi',
    output_mode='typed',
    discard_overlapping_predicted_spans=False,
)

result = redactor.redact('Alice was born on 1990-01-02')
print(result.redacted_text)

