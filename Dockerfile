FROM runpod/pytorch:1.0.3-cu1290-torch280-ubuntu2204

WORKDIR /app

RUN pip3 install -U "huggingface_hub"

RUN hf download openai/privacy-filter --local-dir /root/.opf/privacy_filter

COPY . .

RUN pip3 install -e .

RUN chmod +x start.sh

CMD ["bash", "start.sh"]