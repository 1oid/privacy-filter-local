FROM pytorch/pytorch:2.11.0-cuda12.8-cudnn9-runtime

WORKDIR /app

RUN apt update && apt install -y git wget curl

RUN pip3 install -U "huggingface_hub"

RUN hf download openai/privacy-filter --local-dir /root/.opf/privacy_filter

COPY . .

RUN pip3 install --ignore-installed -e .

RUN chmod +x start.sh

CMD ["bash", "start.sh"]