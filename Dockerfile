FROM python:3.13

WORKDIR /final_project 
COPY . /final_project/
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "index.py"]
# CMD for you might be python3 