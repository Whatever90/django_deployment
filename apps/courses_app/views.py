from django.shortcuts import render, redirect
from .models import Course


def index(request):
	context = {
		"course": Course.objects.all(),
		}
	print "we are in courses"
	return render(request, "courses_app/index.html", context)

def new(request):
	errors = Course.objects.basic_validator(request.POST)
	request.session['error'] = ""
	if len(errors)>0:
		request.session['error'] = errors
		return redirect('/')
	else:
		create = Course.objects.create(name=request.POST['name'], desc=request.POST['desc'])
		create.save()
		request.session['error'] = ''
		return redirect('/')
	print "created a new course"
	
	
	return redirect('/')

def destroy(request, user_id):
	print "confirm deletion"
	context = {
		'course': Course.objects.get(id=user_id)
	}
	return render(request, 'courses_app/index2.html', context)
def destroy_confirm(request, user_id):
	print "terminating course"
	destroy = Course.objects.get(id=user_id)
	#print destroy.first_name
	destroy.delete()
	return redirect('/')
