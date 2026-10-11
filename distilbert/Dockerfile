# DistilBERT tool-call classifier: CPU image, model pulled from the Hugging Face Hub at run time.
#
#   docker build -t mayi-distilbert .
#   echo "### PROPOSED TOOL CALL ..." | docker run -i --rm -v hf-cache:/cache mayi-distilbert --text -
#   docker run --rm -v hf-cache:/cache -v "$PWD/data:/data" mayi-distilbert \
#       --input /data/test.csv.gz --out /data/predictions/test.csv
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/cache/huggingface \
    MODEL_ID=akifkulll/mayi-distilbert-b

WORKDIR /app

# CPU-only torch is ~200 MB instead of ~2.5 GB with CUDA; installed first so code changes don't redo it.
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY predict.py evaluate_predictions.py ./

# Model files are not baked into the image: the first run downloads them into /cache.
VOLUME ["/cache"]
ENTRYPOINT ["python", "predict.py"]
CMD ["--help"]
