FROM pytorch/pytorch:2.11.0-cuda13.0-cudnn9-devel

WORKDIR /app

RUN apt update && apt install -y git wget curl

RUN pip3 install -U "huggingface_hub" --break-system-packages

RUN hf download openai/privacy-filter --local-dir /root/.opf/privacy_filter

COPY . .

RUN pip3 install --ignore-installed -e . --break-system-packages

RUN chmod +x start.sh

CMD ["bash", "start.sh"]