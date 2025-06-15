from django.http import JsonResponse
# from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny,\
    IsAdminUser

from app.models import MedCollection, Pharma
from .shared.strToList import StringToList
import time

# Create your views here.


class GeneralOperations(viewsets.ViewSet):
    """
    Handles general operations
    """
    @action(methods=['get'], detail=False,\
             permission_classes= [IsAdminUser])
    def collection_len(self, request):
        """
        gives the length of the collection.
        """
        meds_len = MedCollection.objects.filter(qte__gte=1).count()
        return Response({
            'response': meds_len
        })

class InputOperations(viewsets.ViewSet):
    @action(methods=['post', 'get'], detail=False,\
             permission_classes= [ IsAuthenticated ])
    def updateCollection(self, request):
        """
        Cancel the operation of Sell, for a given 
        ID in umutiSold.
        """
        meds = request.data.get('data', None)
        if not meds:
            print(f"THe failed user: {(request.user)}")
            return JsonResponse({
                'response': 403
            })
        user = request.user
        pharma = Pharma.objects.get(owner=user)
        # data_list = StringToList(meds).toList()
        print(f"The _list: {type(meds)} from {request.user}")
        time.sleep(5)
        return JsonResponse({
            'response': 200
        })
    def _give_code(self, num)->int:
        codes = [1, 2, 3, 4, 5]
        if (num > 4) or (num < 0):
            num = 0
        return codes[num]


class OutputOperations(viewsets.ViewSet):
    @action(methods=['post'], detail=False,\
             permission_classes= [IsAdminUser])
    def cancelSell(self, request):
        """
        Cancel the operation of Sell, for a given 
        ID in umutiSold.
        """
        return JsonResponse({
            'response': 403
        })