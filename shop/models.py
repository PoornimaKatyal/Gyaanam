from django.db import models

from django.utils import timezone
from django.urls import reverse



class Publisher(models.Model):
	publisher_name = models.CharField(max_length=250)
	Location = models.CharField(max_length=50, blank = True, null = True)

	def __str__(self):
		return self.publisher_name


class Genre(models.Model):
	genre_name = models.CharField(max_length=250)

	def __str__(self):
		return self.genre_name



class Author(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)

	def __str__(self):
		return self.first_name +' '+ self.last_name


class Books(models.Model):
	title = models.CharField(max_length=50)
	subtitle = models.TextField()
	description = models.TextField()
	author = models.ManyToManyField(Author, blank = True, null = True)
	price = models.FloatField(blank=True, null=True)
	num_pages = models.IntegerField(blank=True, null=True)
	publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
	binding = models.CharField(max_length=50)
	genre = models.ManyToManyField(Genre, blank = True, null = True)
	edition = models.CharField(max_length=50)
	language = models.CharField(max_length=50)
	date_added = models.DateTimeField(default=timezone.now)
	cover_image = models.ImageField(blank = True, null = True, upload_to = "covers/%Y/%m/%D/")

	def __str__(self):
		return 'Title: {}, ID: {}'.format(self.title, self.id)

	def get_absolute_url(self):
		return reverse("bookdetail", kwargs={"id": self.id})




