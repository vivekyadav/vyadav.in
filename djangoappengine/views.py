from django.conf import settings
from django.http import HttpResponse
from django.utils.importlib import import_module
#added hereafter
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect

from google.appengine.ext.db import djangoforms
from google.appengine.ext.db import GqlQuery
from google.appengine.ext.db import Key

import models
import re

def warmup(request):
    """
    Provides default procedure for handling warmup requests on App Engine.
    Just add this view to your main urls.py.
    """
    for app in settings.INSTALLED_APPS:
        for name in ('urls', 'views'):
            try:
                import_module('%s.%s' % (app, name))
            except ImportError:
                pass
    content_type = 'text/plain; charset=%s' % settings.DEFAULT_CHARSET
    return HttpResponse('Warmup done', content_type=content_type)

#myadditions
class ShoutForm(djangoforms.ModelForm):
	class Meta:
		model = models.Shout
		exclude = ['mtime' ,'user','slug']

 
def index(request):
	query = models.Shout.gql("ORDER BY mtime DESC")
	return render_to_response('index.html', {'shouts':query.run()})

def projects(request):
	return render_to_response('projects.html')
	
def contacts(request):
	return render_to_response('contacts.html')

def slugify(s):
	return re.sub('[^a-zA-Z0-9-]+', '-', s).strip('-')

def post(request):
	form = ShoutForm(request.POST)
	if not form.is_valid():
		return render_to_response('index.html',{'form':form})

	shout = form.save(commit=False)
	shout.slug = slugify(shout.title)
	shout.put()
	return HttpResponseRedirect('/')

#adding a new post is similar to editing a post
def addpost(request):
	return render_to_response('addpost.html',{'form':ShoutForm(),'action':'post'})

def editpost(request,slug):
	query = models.Shout.gql('WHERE slug = :1',slug)
	shout = query.fetch(1,0)
	form = ShoutForm(initial={'title':shout[0].title,'text':shout[0].text})	
	return render_to_response('editpost.html',{'form':form,'path':'../','action':'savepost','slug':slug})

def savepost(request,slug):
	#shout = models.Shout.get(Key.from_path('slug',slug))
	#return render_to_response('test.html')
	#data = ShoutForm(request.POST)
	#if data.is_valid():
		#entity = data.save(commit=False)
		#entity.slug = slugify(entity.title)
		#entity.put()
	return HttpResponseRedirect('/')

def showpost(request,slug):
	#url = request.path
	slug = m=re.findall(r'[\w-]+',slug)
	query = models.Shout.gql('WHERE slug = :1',slug)
	return render_to_response('index.html', {'shouts':query.run(),'path':'../'})

def delete(request):
	shouts = GqlQuery("SELECT * FROM Shout")
	for shout in shouts:
		shout.delete()

	return HttpResponseRedirect('/')

def test(request,slug):
	return render_to_response('test.html', {'slug':slug})
	
def aindex(request):
	query = {'shouts':models.aShout.objects.all()}
	return render_to_response('index.html',query)

def ashowpost(request,slug):
	query = {'shout':models.aShout.objects.get(slug = slug)}
	#query = {'shouts' : get_object_or_404(models.aShout,slug = slug)}
	return render_to_response('showpost.html',query)
