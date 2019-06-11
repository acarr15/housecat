from django.db import models


class region(models.Model):
	region = models.CharField(max_length=50)

	def __str__(self):
		return self.region

class tag(models.Model):
	tag = models.CharField(max_length=20)

	def __str__(self):
		return self.tag

class status(models.Model):
	desc = models.CharField(max_length=20)

	def __str__(self):
		return self.desc

	class Meta:
		verbose_name_plural="statuses"

class artist(models.Model):
	name = models.CharField(max_length=50)
	genre = models.CharField(max_length=20)
	region_id = models.ForeignKey(region, on_delete=models.SET_NULL, null=True)
	hometown = models.CharField(max_length=50)
	email = models.EmailField()
	status = models.ForeignKey(status, on_delete=models.SET_DEFAULT, default=1)

	def __str__(self):
		return "%s, %s" % (self.name, self.hometown)

class media(models.Model):
	artist = models.ForeignKey(artist, on_delete=models.CASCADE)
	facebook = models.URLField(max_length=2083, null=True)
	instagram = models.URLField(max_length=2083, null=True)
	twitter = models.URLField(max_length=2083, null=True)
	bandcamp = models.URLField(max_length=2083, null=True)
	soundcloud = models.URLField(max_length=2083, null=True)
	tumblr = models.URLField(max_length=2083, null=True)
	patreon = models.URLField(max_length=2083, null=True)
	website = models.URLField(max_length=2083, null=True)

	class Meta:
		verbose_name_plural="media"

	def __str__(self):
		return "%s, %s" % (self.artist.name, self.artist.hometown)

class artist_tag(models.Model):
	artist = models.ForeignKey(artist, on_delete=models.CASCADE)
	tag = models.ForeignKey(tag, on_delete=models.CASCADE)

	def __str__(self):
		return "%s, %s: %s" % (self.artist.name, self.artist.hometown, self.tag.tag)

