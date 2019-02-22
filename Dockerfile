FROM python:3.6-alpine
ADD . /code
WORKDIR /code
RUN apt update && apt install -y libsm6 libxext6
RUN pip install -r requirements.txt
RUN pip install -e .
CMD ["python", "vl/app.py"]
