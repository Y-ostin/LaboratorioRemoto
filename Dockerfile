FROM python:3.9
WORKDIR /app
COPY requeriments.txt .

RUN pip install -r requeriments.txt
COPY ..
EXPOSE 5000
CMD ["python", "app.py"]