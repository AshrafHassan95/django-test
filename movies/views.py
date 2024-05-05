from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from .models import Movie
from .serializers import MovieSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



def movies(request):
    data = Movie.objects.all()
    return render(request, 'movies/movies.html', {'movies':data})

def home(request):
    return HttpResponse("Home page")

@api_view(['GET', 'POST'])
def movie_list(request):

    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return JsonResponse({"movies":serializer.data})
    if request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def detail(request, id):

    try:
        data = Movie.objects.get(pk=id)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MovieSerializer(movies)
        return Response(serializer.data)
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass

    return render(request, 'movies/detail.html', {'movie':data})

def add(request):
    title = request.POST.get('title')
    year = request.POST.get('year')

    if title and year:
        movie = Movie(title=title, year=year)
        movie.save()
        return HttpResponseRedirect('/movies')  
    return render(request, 'movies/add.html')

def delete(request, id):
    try:
        Movie.objects.get(pk=id)
    except:
        raise Http404('Movie does not  exist')
    movies.delete()
    return HttpResponseRedirect('/movies')