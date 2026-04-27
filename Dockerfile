FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

WORKDIR /app

RUN pip3 install -U "huggingface_hub"

RUN hf download openai/privacy-filter /root/.opf/privacy_filter

COPY . .

RUN pip3 install -e .

RUN chmod +x start.sh

CMD ["bash", "start.sh"]