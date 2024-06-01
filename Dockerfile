FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD Pipfile /code/
ADD Pipfile.lock /code/
RUN pip install pipenv
RUN pipenv install --system
ADD . /code

EXPOSE 8000

CMD [ "gunicorn", "--chdir", "mint_models","--access-logfile", "-", "wsgi:application", "--bind", "0.0.0.0:8000"]
