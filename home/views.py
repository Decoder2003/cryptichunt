from os import name
from django.db.models.fields import EmailField
from django.http.response import Http404, HttpResponseNotFound,HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import HttpResponse
import json
from datetime import datetime, tzinfo
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from home.models import cryptUser, quesAns
from django_email_verification import send_email
from ratelimit.decorators import ratelimit
from ratelimit.exceptions import Ratelimited
import re
# from django.views.decorators.cache import cache_page



def validationCheck(email, discord_id, check):
	if check == 1:
		if len(email) > 6:
			if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email) != None:
				return 0
		return 1
	else:
		# if re.match('.*#[0-9]{4}', discord_id) != None:
		# 	return 0
		return 0
def ratelimited_error(request, exception):
    if isinstance(exception, Ratelimited):
        return render(request, '429.html', status=429)
    return render(request, '403.html', status=403)

startTime = '2024-04-15 09:00:00.000000'
endTime = '2024-04-19 09:00:00.000000'

# @cache_page(60*60*24)
def home(request):
	return render(request, 'index.html')

def abcd(request):
	if request.user.current_level == 3:
		return redirect('https://www.icegif.com/wp-content/uploads/2023/01/icegif-162.gif') 
	return render(request,'404.html')

def register(request):
	# if not request.user.is_active and request.user.is_authenticated:
	# 	return redirect('dq')
	# if request.method == 'POST':
	# 	first_name =  request.POST.get('first_name')
	# 	last_name =  request.POST.get('last_name')
	# 	username =  request.POST.get('user_name')
	# 	collegeName = request.POST.get('college_name')
	# 	college_roll_number = request.POST.get('college_roll_number')
	# 	discord_id = request.POST.get('discord_id')
	# 	email =  request.POST.get('email')
	# 	password =  request.POST.get('password')
	# 	password2 = request.POST.get('password2')
	# 	errorMsgs = 0
	# 	if len(first_name.split())==0 or len(last_name.split())==0 or len(username.split())==0 or len(collegeName.split())==0 or len(discord_id.split())==0 or len(email.split())==0 or len(password.split())==0 or len(password2.split())==0:
	# 		errorMsgs = 1
	# 		messages.error(request,'All fields are required')
	# 	if validationCheck(email, discord_id,1):
	# 		errorMsgs = 1
	# 		messages.error(request,'Email is not valid')
	# 	if validationCheck(email, discord_id,0):
	# 		errorMsgs = 1
	# 		messages.error(request,'Discord id is not valid')
	# 	if password != password2:
	# 		errorMsgs = 1
	# 		messages.error(request,'Passwords do not match')
	# 	if len(password)<8 or len(password2)<8:
	# 		errorMsgs = 1
	# 		messages.error(request,'Password is less than 8 characters')
	# 	if cryptUser.objects.filter(user_name=username).exists():
	# 		errorMsgs = 1
	# 		messages.error(request, "User already exists")
	# 		print('username exists')
	# 	if cryptUser.objects.filter(email=email).exists():
	# 		errorMsgs = 1
	# 		print('email taken')
	# 		messages.error(request, "Email is taken")
	# 	if cryptUser.objects.filter(discord_id = discord_id).exists():
	# 		errorMsgs = 1
	# 		print('discord id taken')
	# 		messages.error(request, "Discord id is taken")
	# 	if errorMsgs != 0:
	# 		return HttpResponseRedirect(reverse("register"))
	# 	else:
	# 		cryptUser.objects.create_user(user_name=username, email=email, password=password, first_name=first_name, last_name=last_name, college_name = collegeName,college_roll_number=college_roll_number, discord_id = discord_id)
	# 		login(request, authenticate(username = username, password = password))
	# 		user = cryptUser.objects.get(user_name = username)
	# 		# send_email(user)
	# 		now = datetime.now()
	# 		user.date_time = json.dumps({'register': str(now)})
	# 		user.save()
	# 		print('autoLogin')
	# 		messages.success(request, "Successfully Registered")
	# 		return HttpResponseRedirect(reverse("questions"))
	# return render(request,'register.html')
	
	return render(request, 'dq.html', {'ns':2})


def cryptLogin(request):
	if request.user.is_authenticated:
		return redirect('questions')
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		print(username, password)
		try:
			user = authenticate( username = cryptUser.objects.get(email = username), password = password)
		except:
			user = authenticate( username = username, password = password)

		print(user)
		if user is not None:
			login(request, user)
			messages.error(request, 'Successfully Logged out')
			return HttpResponseRedirect(reverse("questions"))
		else:
			messages.error(request, 'Invalid creds')
			return HttpResponseRedirect(reverse("login"))
	return render(request,'login.html')

@ratelimit(key='post:username',rate='700/h', block = True)
def questions(request):
	return render(request, 'dq.html', {'ns':2})
	# if str(datetime.now()) >= startTime and str(datetime.now()) <= str(endTime):
	# 	l = []
	# 	data = {}
	# 	username = None
	# 	if request.user.is_authenticated:
	# 		if not request.user.is_active or not request.user.is_verified:
	# 			return redirect('dq')
	# 		username = request.user.user_name
	# 		user = cryptUser.objects.get(user_name = username)
	# 		# if user.rank > 0:
	# 		# 	return redirect('winner')
	# 		if request.method == "POST":
	# 			answer = request.POST.get('answer')
	# 			print(answer)
	# 			print(username)
	# 			print(user.current_level)
	# 			print(user.score)
	# 			prevData = json.loads(user.answers)
	# 			if len(answer.split())!=0:
	# 				if not prevData.get(str(user.current_level), False):
	# 					prevData[user.current_level] = [answer]
	# 					user.answers = json.dumps(prevData)
	# 					user.save()
	# 				else:
	# 					l = prevData[str(user.current_level)]
	# 					l.append(answer)
	# 					prevData[str(user.current_level)] == l
	# 					user.answers = json.dumps(prevData)
	# 					user.save()
	# 				question = quesAns.objects.get(question_number = user.current_level)
	# 				if question.answer == answer:
	# 					user.score += 10
	# 					user.current_level += 1
	# 					# if user.current_level == 5:
	# 					# 	if not cryptUser.objects.filter(rank = 3):
	# 					# 		if not cryptUser.objects.filter(rank = 2):
	# 					# 			if not cryptUser.objects.filter(rank = 1):
	# 					# 				user.rank = 1
	# 					# 			else:
	# 					# 				user.rank = 2
	# 					# 		else:
	# 					# 			user.rank = 3
	# 					# 	else:
	# 					# 		user.rank = 4
	# 					# 	user.save()
	# 					# 	return redirect('winner')
						
	# 					user.start_date = datetime.now()
	# 					date_Data = json.loads(user.date_time)
	# 					date_Data[str(user.current_level)] = str(timezone.now())
	# 					user.date_time = json.dumps(date_Data)
	# 					user.save()
	# 					messages.success(request, 'Correct Answer!!')
	# 				else:
	# 					messages.error(request,'Incorrect Answer!!')
	# 				return HttpResponseRedirect(reverse("questions"))
	# 			else:
	# 				messages.error(request,'Incorrect Answer!!')
	# 				return HttpResponseRedirect(reverse("questions"))
	# 		return render(request,'level.html',{'level':user.current_level})
	# 	else:
	# 		return redirect('login')
	# else:
	# 	return HttpResponseRedirect(reverse("dq"))

# @cache_page(60*10)
def leaderboard(request):
	if str(datetime.now()) >= startTime:
		all_users = cryptUser.objects.all().exclude(is_active = False).exclude(is_verified = False).exclude(is_staff = True).exclude(user_name = "ShreyashTrivedi").exclude(user_name = "kritikagiri").order_by('-score','start_date')
		return render(request,'leaderboard.html',{'all_users':all_users})
	else:
		return HttpResponseRedirect(reverse("dq"))

def logoutUser(request):
	if request.user.is_authenticated:
		logout(request)
	return redirect('login')

def dq(request):
	try:
		if not request.user.is_active and request.user.is_authenticated or not request.user.is_verified:
			return render(request, 'dq.html')
	except:
		if str(datetime.now()) >= startTime  and str(datetime.now()) <= endTime:
			if not request.user.is_active and request.user.is_authenticated or not request.user.is_verified:
				return render(request, 'dq.html')
			return redirect('home')
		elif str(datetime.now()) >= endTime :
			return render(request, 'dq.html', {'ns':2})
		else:
			return render(request, 'dq.html', {'ns':1})
	if str(datetime.now()) >= endTime :
			return render(request, 'dq.html', {'ns':2})
	return render(request, 'dq.html', {'ns':1})

# @cache_page(60*60*24)
def rules(request):
	return render(request, 'rules.html')
	
def logs(request):
	if request.user.is_authenticated and request.user.is_staff:
		if request.method == "POST":
			userName = request.POST.get('userName')
			userData = cryptUser.objects.get(user_name = userName)
			listData = []
			listData2 = []
			answers = json.loads(userData.answers)
			dates = json.loads(userData.date_time)
			for i in dates:
				listData2.append(dates[i])
			for var in answers:
				listData.append(answers[var])
			# print(listData)
			# print(listData2)
			return render(request, 'data.html', {'userData':zip(listData,listData2), 'userName':userName})
		users = cryptUser.objects.all()
		return render(request, 'logs.html',{'users':users})
	else:
		return HttpResponseNotFound(request)


def winner(request):
	# if request.user.is_authenticated and request.user.rank > 0:
	# 	return render(request, 'winner.html')
	# else:
	return HttpResponseNotFound(request)

def lvl16(request):
	if request.user.current_level == 16:
		return HttpResponse("Vapis jayo ekk ganna dundho..")
	return render(request,'404.html')

def lvl20(request):
	if request.user.current_level == 20:
		return redirect("https://lh3.googleusercontent.com/u/0/drive-viewer/AKGpihYZcA9ZjXtvmlKxhFXyq9P4AZjQCqIqXuqh-DBhSzrsOjVqu0F3koVpGSIN-RF9gR1IIaQ021p-kzUW5dfw4YHWVWQzU3F5vH4=w1920-h868")
	return render(request,'404.html')

def lvl29(request):
	if request.user.current_level == 29:
		return HttpResponse("why?")
	return render(request,'404.html')