FROM python:3.8-slim-buster
WORKDIR /Cell_shape_detection

RUN python3 -m pip install --upgrade pip
RUN pip3 install flask scikit-learn


COPY . .
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]