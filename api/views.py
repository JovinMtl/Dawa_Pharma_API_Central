from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny,\
    IsAdminUser

from app.models import MedCollection, User, Pharma

# Create your views here.


class GeneralOperations(viewsets.ViewSet):
    @action(methods=['post'], detail=False,\
             permission_classes= [IsAdminUser])
    def collection_len(self, request):
        """
        Cancel the operation of Sell, for a given 
        ID in umutiSold.
        """
        meds_len = MedCollection.objects.all()
        return JsonResponse({
            'response': 403
        })

class InputOperations(viewsets.ViewSet):
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