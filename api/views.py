# api.views
from django.contrib.auth.models import User, Group
from django.db.models import Count
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from elasticsearch import Elasticsearch
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from accounts.permissions import IsOwnerOrReadOnly, IsOwner
from api.serializers import UserSerializer, GroupSerializer, DatasetSerializer, \
    PlaceSerializer, PlaceGeomSerializer, AreaSerializer
from areas.models import Area
from datasets.models import Dataset
from places.models import Place, PlaceGeom

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000
    
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'datasets': reverse('dataset-list', request=request, format=format)
        #'datasets': reverse('dataset-list', request=request, format=format)
    })

class PlaceDetail(APIView):
    """
    Retrieve a single place database record.
    """
    def get_object(self, pk):
        print('PlaceDetail.get_object()',pk)
        try:
            return Place.objects.get(pk=pk)
        except Place.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        place = self.get_object(pk)
        serializer = PlaceSerializer(place,context={'request': request})
        return Response(serializer.data)
    
    def foo(self, pk):
        return JsonResponse({"id":pk})
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

class PlaceList(APIView):
    """
    List all places in dataset
    """
    pagination_class = StandardResultsSetPagination
    
    def get(self, request, *args, **kwargs):
        ds= kwargs['pk']
        places=get_object_or_404(Dataset,pk=ds).places.all()
        serializer = PlaceSerializer(places, many=True,context={'request': request})
        return Response(serializer.data) 
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]



class DatasetAPIView(generics.ListAPIView):
    """    List public datasets    """
    serializer_class = DatasetSerializer
    
    def get_queryset(self):
        qs = Dataset.objects.all().filter(public=True).order_by('label')
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(description__icontains=query)
        return qs
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    authentication_classes = []

class DatasetDetailAPIView(generics.RetrieveAPIView):
    """    Retrieve dataset record by id   """

    queryset = Dataset.objects.all().filter(public=True).order_by('label')
    serializer_class = DatasetSerializer
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    authentication_classes = []
    
class DatasetDetail(APIView):
    """
    Retrieve a single dataset record.
    """
    def get_object(self, pk):
        try:
            return Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dataset = self.get_object(pk)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#
# in use pre-Apr 2020
class DatasetViewSet(viewsets.ModelViewSet):
    # print('in DatasetViewSet()')
    queryset = Dataset.objects.all().filter(public=True).order_by('label')
    serializer_class = DatasetSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list','retrieve']:
            print(self.action)
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    
class indexAPIView(View):
    @staticmethod
    def get(request):
        print('in indexAPIView, GET =',request.GET)
        """
        args in request.GET:
        [string] idx: latest name for whg index
        [string] _id: same as whg_id in index
        """
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        idx = request.GET.get('idx')
        _id = request.GET.get('_id')
        q={"query": {"bool": {"must": [{"match":{"_id": _id }}]}}}
        res = es.search(index=idx, doc_type='place', body=q)
        # single hit (it's a unique id after all)
        hit = res['hits']['hits'][0]
        print('hit[_id] from indexAPIView()',hit['_id'])
        # now get traces
        # does hit have children?
        
        #qt={"query": {"bool": {"must": [{"match":{"_id": _id }}]}}}
        #res_t = es.search(index="traces", doc_type='trace', body=q)
        #print('indexAPIView _id',_id)
        print('indexAPIView hit',hit)
        return JsonResponse(hit, safe=True)
        
class GeomViewSet(viewsets.ModelViewSet):
    queryset = PlaceGeom.objects.all()
    serializer_class = PlaceGeomSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def get_queryset(self):
        dslabel = self.request.GET.get('ds')
        dsPlaceIds = Place.objects.values('id').filter(dataset = dslabel)
        qs = PlaceGeom.objects.filter(place_id_id__in=dsPlaceIds)
        return qs
    
# populates drf table in dataset.detail#browse
class PlaceTableViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all().order_by('title')
    serializer_class = PlaceSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        print('PlaceViewSet.get_queryset()',self.request.GET)
        qs = Place.objects.all()
        query = self.request.GET.get('q')
        ds = self.request.GET.get('ds')
        if ds is not None:
            qs = qs.filter(dataset = ds)
        if query is not None:
            qs = qs.filter(title__istartswith=query)
        return qs

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list','retrieve']:
            print(self.action)
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all().order_by('title')
    serializer_class = AreaSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list','retrieve']:
            print(self.action)
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

#@api_view(['GET'])
#def dataset_list(request, format=None):
    #"""
    #List all datasets
    #"""
    #if request.method == 'GET':
        #datasets = Dataset.objects.all()
        #serializer = DatasetSerializer(datasets, many=True)
        #return JsonResponse(serializer.data, safe=False)
    

#@api_view(['GET'])
#def dataset_detail(request, pk, format=None):
    #"""
    #Retrieve, update or delete a code snippet.
    #"""
    #try:
        #dataset = Dataset.objects.get(pk=pk)
    #except Dataset.DoesNotExist:
        #return Response(status=status.HTTP_404_NOT_FOUND)

    #if request.method == 'GET':
        #serializer = DatasetSerializer(dataset)
        #return JsonResponse(serializer.data)

