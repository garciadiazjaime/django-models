from django.db import models


class Category(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name

class PriceRange(models.Model):
  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name

class Gift(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  price = models.FloatField()
  store_url = models.URLField()
  image_url = models.URLField()
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  price_range = models.ForeignKey(PriceRange, on_delete=models.CASCADE)
  sha = models.CharField(max_length=64, unique=True)

  def __str__(self):
    return self.title
