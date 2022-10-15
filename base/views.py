from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import *
from base.serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
import random

def home(request):
	return render(request, 'docx.html')
	
	
@api_view(['GET', 'POST'])
def all_user(request):
	users = User.objects.all()
	s = UserS(users, many=True, context={'request':request})
	return Response(s.data)
	

@api_view(['POST'])
def signup(request):
	if request.method == 'POST':
		username= request.data.get('username')
		p= request.data.get('password')
		cp = request.data.get('confirm_password')
		mail = request.data.get('email')
		gender = request.data.get('gender')
		add = request.data.get('address')
		num = request.data.get('mobile')
		dob = request.data.get('date-of-birth')
		
		try:
			User.objects.get(username=username)
			return Response({'msg':'Username already exist'})
		except User.DoesNotExist:
			if p == cp:
				user = User.objects.create_user(username=username, password=p, email=mail, gender=gender, address=add, mobile=num, birth_date=dob)
				user.save()
				return Response({'msg': f'Hi, {username}. thanks for signup!'})
			else:
				return Reponse({'msg':'password not matched'})
				
	else:
		return Response({'msg':'Method not allowed'})
		
		
@api_view(['POST'])
def signin(request):
	if request.method == 'POST':
		u= request.data.get('username')
		p= request.data.get('password')
		
		user= authenticate(username=u, password=p)
		if user is not None:
			login(request, user)
			token = Token.objects.create(user=user)
			
			return Response({
				'token' : token.key,
				'msg' : 'login success'
			})
		else:
			return Response({
				'msg' : 'username or password invalid'
			})
			

@api_view(['GET', 'POST'])
def get_id(request, username):
	try:
		user = User.objects.get(username=username)
		s = UserS(user, many=False, context={'request':request})
		return Response(s.data)
	except User.DoesNotExist:
		return Response({'msg':'user not found'})


@api_view(['POST'])
def edit_profile(request):
	if request.user.is_authenticated:
		u = User.objects.get(username=request.user)
		if request.data.get('username'):
			u.username = request.data.get('username')
		if request.data.get('email'):
			u.email = request.data.get('email')
		if request.data.get('mobile'):
			u.mobile = request.data.get('mobile')
		if request.data.get('address'):
			u.address = request.data.get('address')
		if request.data.get('date-of-birth'):
			u.birth_date = request.data.get('date-of-birth')
		if request.data.get('gender'):
			u.gender = request.data.get('gender')
		if request.FILES.get('profile_pc'):
			u.profile_pc = request.FILES.get('profile_pc')
		
		print(request.FILES.get('profile_pc'))
		u.save()
			
		return Response({"msg":"profile data updated!"})
	else:
		return Response({"msg":"you have to login before hit this route! add your auth token on headers"})


@api_view(['POST'])
def forget(request):
	email = request.data.get('email')
	code = random.randint(1111,9999)
	try:
		user = User.objects.get(email=email)
		user.forgot_code = code
		user.save()
		send_mail(
			'You forgot password code!',
    		f'Hi, {user.username}. here is your code {code}',
    	 settings.EMAIL_HOST_USER,
    	 [email],
    	 fail_silently=False,)
		return Response({'msg':'a verification code has been sent to your email'})
	except User.DoesNotExist:
		return Response({'msg':'no user found with this email!'})


@api_view(['POST'])
def submit(request):
	code = request.data.get("code")
	np = request.data.get("new_password")
	cp = request.data.get('confirm_password')
	
	try:
		user = User.objects.get(forgot_code=code)
		if np == cp:
			user.set_password(np)
			user.forgot_code = ""
			user.save()
			return Response({'msg':'password changed'})
		else:
			return Response({'msg':'password not mached'})
	except User.DoesNotExist:
		return Response({'msg':'code not matched'})
		
		


@api_view(['POST'])
def change(request):
	if request.user.is_authenticated:
		old = request.data.get('old_password')
		new = request.data.get('new_password')
		cn = request.data.get('confirm_password')
		
		user = authenticate(username=request.user, password=old)
		if user is not None:
			user.set_password(new)
			user.save()
			return Response({'msg':'password changed'})
		else:
			return Response({'msg': 'old password is not correct'})
	else:
		return Response({'msg':'You have to authenticated before request this endpoint'})