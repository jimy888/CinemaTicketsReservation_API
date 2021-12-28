from re import search
from django.db.models.fields.related import RECURSIVE_RELATIONSHIP_CONSTANT
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.serializers import Serializer
from .models import Guest, Movie, Reservation, Post
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.authentication import  BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins, viewsets
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer, PostSerializer
from tickets import serializers
from .permissions import IsAuthorOrReadOnly
# Create your views here.

#1 without REST and no model query (Function based view FBV)
def no_rest_no_model(request):
    guests = [
        {
            'id': 1,
            'Name': 'Omar',
            'mobile': 5589643,
        },
        {
            'id': 2,
            'Name': 'imam',
            'mobile': 8236975
        }
    ]
    return JsonResponse (guests, safe=False)

#2 model data default django without rest
def no_rest_from_model(request):
    # make a query set
    data = Guest.objects.all()
    response = {
        'guests': list(data.values('name', 'mobile'))
    }
    return JsonResponse(response)

# List == GET request (.e.g list products)
# Create == POST request (.e.g from control panel)
# pk query == GET request
# Update == PUT request (.e.g modify something)
# Delete/destroy == DELETE request

#3 Function based views 

#3.1 GET POST
@api_view(['GET', 'POST']) # run before the following function
def FBV_List(request):
    #GET
    if request.method == 'GET':
        guests = Guest.objects.all() #query set
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    #POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 
            status= status.HTTP_201_CREATED)
        return Response(serializer.data,
        status= status.HTTP_400_BAD_REQUEST)
    



#3.2 GET PUT DELETE
@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    #GET
    if request.method == 'GET':
        serializer = GuestSerializer(guest) #note: guest not guests
        return Response(serializer.data)
    #PUT
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    #DELETE
    if request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
# class based views (CBV)
#4.1 List and Create == GET and POST
class CBV_List(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


#4.2 GET PUT DELETE class based views -- pk
class  CBV_pk(APIView):# define the query set(the guest we want)(APIView):
    
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk) #define the query set(the guest we want)
        Serializer = GuestSerializer(guest)
        return Response(Serializer.data)
    def put(self, request, pk):
        guest = self.get_object(pk)  # define the query set(the guest we want)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Mixins
#5.1 mixins list
class mixins_list(mixins.ListModelMixin,  mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)

#5.2 mixins get put delete
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    def get(self, request, pk):
        return self.retrieve(request)
    def put(self, request, pk):
        return self.update(request)
    def delete(self, request, pk):
        return self.destroy(request)

# 6 Generics
# 6.1 get and post
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    

# 6.2 get put delete
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

#7 Viewsets (one for all operations)
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backend = [filters.SearchFilter]
    search_fields = ['movieName']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
                  
                  
#8 Find movie (function based method)
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(name=request.data['movieName'])
      
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


#9 create new reservation     
@api_view(['POST'])
def new_reservation(request):
    movie = Movie.objects.get(
        movie=request.data['movieName'],
        hall =request.objects.get(['hall'])
    )
    guest = Guest()
    guest.name= request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation    = Reservation()
    reservation.guest = guest 
    reservation.movie = movie 
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)     



#10 post author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer







