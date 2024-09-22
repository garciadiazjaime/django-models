from fabric import task


@task
def deploy(c):
    c.run("docker build -t garciadiazjaime/django-models . --platform linux/amd64")
    c.run("docker push garciadiazjaime/django-models")
    c.run('echo "docker pull garciadiazjaime/django-models"')


@task
def model(c):
    c.run("./manage.py report")
    c.run("./manage.py artist_popularity_model")
    c.run(
        "tensorflowjs_converter --input_format=tf_saved_model data/model/saved_model data/public"
    )
