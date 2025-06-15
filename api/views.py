from django.http import JsonResponse
from django.db.models import Q
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
        sync_code = 1
        # data_list = StringToList(meds).toList()
        print(f"The _list: {type(meds)} from {request.user}")
        
        for med in meds:
            try:
                med_found = MedCollection.objects.get(Q(owner=pharma)\
                            & Q(nom_med=med.nom_med))
            except MedCollection.DoesNotExist:
                new_med = self._create_med(med=med,pharma=pharma, \
                                           sync_code=sync_code)
                continue
            else:
                med_update = self._med_updater(med_found=med_found, med=med)
        time.sleep(5)
        return JsonResponse({
            'response': 200
        })
    
    def _give_code(self, num)->int:
        codes = [1, 2, 3, 4, 5]
        if (num > 4) or (num < 0):
            num = 0
        return codes[num]
    
    def _create_med(self, med, pharma, sync_code=0)->int:
        med = {'nom_med': 'Zalain Ovule B/1', 'qte': 3, 'price': 55000, 'lot': "['09-2028']"}
        new_med = MedCollection.objects.create(owner=pharma)
        new_med.nom_med = med['nom_med']
        new_med.qte = med['qte']
        new_med.price = med['price']
        new_med.date_per = str(med['lot'])[:34]
        new_med.sync_code = sync_code
        new_med.save()
        return 200
    
    def _med_updater(self, med_found:MedCollection, med:MedCollection, sync_code:int=0)->int:
        med_found.qte = med.qte
        med_found.price = med.price
        med_found.date_per = med.date_per
        med_found.sync_code = sync_code
        med_found.save()

        return 200


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