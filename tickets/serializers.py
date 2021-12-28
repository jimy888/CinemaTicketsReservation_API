from django.db.models import fields
from rest_framework import serializers
from tickets.models import Guest, Movie, Post, Reservation

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['pk', 'reservation', 'name', 'mobile'] # ممنوع خروج أي serialize data خارج قاعدة البيانات ومنها الـ pk ولكن هنا مشيناها 
        #في المشاريع الحقيقية نستخدم uuid, slug

        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
