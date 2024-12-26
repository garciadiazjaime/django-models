FROM python:3.11
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pipenv

WORKDIR /code

COPY Pipfile Pipfile.lock /code/


RUN pipenv install --system --deploy

ADD . /code

EXPOSE 8000

CMD [ "gunicorn", "--chdir", "mint_models","--access-logfile", "-", "wsgi:application", "--bind", "0.0.0.0:8000"]
