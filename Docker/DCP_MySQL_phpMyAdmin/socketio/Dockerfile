FROM dev_python:0.1
ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt

#Never stop the container
# ENTRYPOINT ["tail", "-f", "/dev/null"]

# CMD ["python", "test.py"]
