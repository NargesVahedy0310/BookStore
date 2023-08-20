from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    authors = models.ManyToManyField('Author')
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13)  # شابک کتاب
    price = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title
class Author(models.Model):
    name = models.CharField(max_length=255)
    birth_city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
