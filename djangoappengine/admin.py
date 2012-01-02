from django.contrib import admin
from models import aShout
from views import slugify

class aShoutAdmin(admin.ModelAdmin):
	fields = ('title','text','slug')
	list_display = ('title','author','pub_date')
	data_hierarchy = 'pub_date'
	
	def save_model(self,request, obj,form,change):
		if not change:
			obj.author = request.user
		obj.save()

# we define our resources to add to admin pages
class CommonMedia:
  js = (
    'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
    '/media/admin/js/editor.js',
  )
  css = {
    'all': ('/media/admin/css/editor.css',),
  }

# let's add it to this model
admin.site.register(aShout,aShoutAdmin,Media = CommonMedia,)
