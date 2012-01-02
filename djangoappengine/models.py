from google.appengine.ext import db
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Shout(db.Model):
	title = db.StringProperty(required=True)
	text = db.TextProperty()
	mtime = db.DateTimeProperty(auto_now_add=True)
	user = db.UserProperty()
	slug = db.StringProperty()

class aShout(models.Model):
	author = models.ForeignKey(User, related_name = 'shouts')
	title = models.CharField(max_length = 200)
	text = models.TextField()
	slug = models.SlugField(max_length = 100,blank=True)
	pub_date = models.DateTimeField('Date Published',auto_now_add = True)
	def __unicode__(self):
		return self.title
	
	def save(self):
		self.slug = slugify(self.title)
		super(aShout,self).save()

	def get_absolute_url(self):
		return "/blog/%s/" % self.slug

