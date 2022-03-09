# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=development
ENV FLASK_APP=project

COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY project/ /project/


#ENTRYPOINT ["tail", "-f", "/dev/null"]
CMD ["flask", "run", "--host", "0.0.0.0"]



