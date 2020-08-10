from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import random
from string import digits
from .models import Library, File, DownloadLot, Like, Visitor
from datetime import datetime
from hashlib import sha224

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = ["hid", "username", "password", "email"]
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
        }

    def create(self, data):
        return Visitor.objects.create(hid= data["hid"], username = data["username"], email = data["email"], password = make_password(data["password"]))

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = "__all__"
        extra_kwargs = {
            'user': {
                'write_only': True
            }
        }
    
    def create(self, data):
        return Library.objects.create(**data)

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = "__all__"

        extra_kwargs = {
            '_file': {
                'write_only': True,
            },
        }

    def create(self, data):
        return File.objects.create(**data)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"

    def create(self, data):
        print (data)
        return Like.objects.create(**data)   