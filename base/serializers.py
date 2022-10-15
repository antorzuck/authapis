from rest_framework import serializers
from base.models import *


class UserS(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'gender', 'birth_date','address','mobile','profile_pc']
		