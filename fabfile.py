from fabric import task


@task
def deploy(c):
    c.run("docker build -t garciadiazjaime/django-models . --platform linux/amd64")
    c.run("docker push garciadiazjaime/django-models")
    c.run('echo "docker pull garciadiazjaime/django-models"')
