FROM python:3
WORKDIR /CloudComputing
ENV FLASK_APP run.py
ENV FLASK_RUN_HOST 0.0.0.0
COPY requirments.txt requirments.txt
RUN pip install -r requirments.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]