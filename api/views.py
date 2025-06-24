from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
# from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny,\
    IsAdminUser

from app.models import MedCollection, Pharma

from .serializers import MedCollectionSeria, PharmaSeria

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
    
    @action(methods=['post', 'get'], detail=False,\
             permission_classes= [IsAuthenticated])
    def search_meds(self, request):
        """
        gives the length of the collection.
        """
        # meds_len = MedCollection.objects.filter(qte__gte=1).count()
        query = request.data.get("imiti", {'value':{"query":''}}).get('value', {'query':''}).get('query')
        query = str(query).strip()
        print(f"the query: {query}")
        queryset = MedCollection.objects.filter(nom_med__icontains=query)
        queryset_s = MedCollectionSeria(queryset, many=True)
        
        if queryset_s.is_valid:
            return Response({
                'response': queryset_s.data
            })
    
    @action(methods=['post', 'get'], detail=False,\
             permission_classes= [ IsAuthenticated ])
    def get_pharmas(self, request):
        user = request.user
        pharma = Pharma.objects.all()

        pharma_obj = {}

        for pha in pharma:
            pha_s = PharmaSeria(pha)
            if pha_s.is_valid:
                pharma_obj[pha.id] = pha_s.data
        
        return Response({
            'response': pharma_obj
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
        sync_code = request.data.get("sync_code", 1)
        
        counter = 1
        for med in meds:
            try:
                med_found = MedCollection.objects.get(Q(owner=pharma)\
                            & Q(nom_med=med['nom_med']))
            except MedCollection.DoesNotExist:
                new_med = self._create_med(med=med,pharma=pharma, \
                                           sync_code=sync_code)
            else:
                med_update = self._med_updater(med_found=med_found, \
                    med=med, sync_code=sync_code)
            
            counter += 1
        
        pharma.last_connected = timezone.now()
        pharma.save()

        return JsonResponse({
            'response': 200
        })
    
    def _create_med(self, med, pharma, sync_code=0)->int:
        # med = {'nom_med': 'Zalain Ovule B/1', 'qte': 3, 'price': 55000, 'lot': "['09-2028']"}
        new_med = MedCollection.objects.create(owner=pharma)
        new_med.nom_med = med['nom_med']
        new_med.qte = med['qte']
        new_med.price = med['price']
        new_med.date_per = str(med['lot'])[:34]
        new_med.sync_code = sync_code
        new_med.save()
        return 200
    
    def _med_updater(self, med_found:MedCollection, med:dict, sync_code:int=0)->int:
        med_found.qte = med['qte']
        med_found.price = med['price']
        med_found.date_per = str(med['lot'])[:34]
        med_found.sync_code = sync_code
        med_found.save()

        return 200
    
    @action(methods=['post', 'get'], detail=False,\
             permission_classes= [ IsAuthenticated ])
    def clean_outdated(self, request):
        # needs to delete untouched instances / garbage
        user = request.user
        pharma = Pharma.objects.get(owner=user)
        sync_code = request.data.get("sync_code", 1)
        unsync_meds = MedCollection.objects.filter(owner=pharma)\
            .exclude(sync_code=sync_code).delete()
        return Response({
            'response': 1
        })
    
    @action(methods=['post', 'get'], detail=False,\
             permission_classes= [ IsAuthenticated ])
    def request_code_sync(self, request):
        user = request.user
        pharma = Pharma.objects.get(owner=user)
        med = MedCollection.objects.filter(owner=pharma).first()
        sync_code = med.sync_code or 0
        return Response({
            'response': sync_code
        })
    
    @action(methods=['post', 'get'], detail=False,\
             permission_classes= [ IsAuthenticated ])
    def update_infos(self, request):
        # needs to delete untouched instances / garbage
        user = request.user
        infos = request.data.get("imiti", {'value':{"query":''}})
        print(f"The infos to update are: {infos}")
        if not infos:
            return Response({
                'response': 0
            })
        code_pharma = infos.get('code_pharma')
        if int(code_pharma) and code_pharma > 1000:
            # update username, password, and pharma
            update_pharma = self._update_pharma(infos=infos)
            pass
        elif int(code_pharma) and code_pharma == 1000:
            # new user and pharma
            new_pharma = self._new_pharma(infos=infos)
            pass
        return Response({
            'response': 1
        })
    
    def _new_pharma(self, infos)->int:
        infos = {'name_pharma': 'Pharma', \
                 'tel': 0, 'loc_street': '13', \
                    'loc_quarter': 'Kamenge', \
                    'loc_commune': 'Ntahangwa', \
                    'loc_Province': 'Bujumbura', \
                    'remote_password': 'done', \
                    'remote_password2': 'done', \
                    'code_pharma': 1000}
        last_pharma = Pharma.objects.last()
        last_code = 1001
        name_pharma = infos.get("name_pharma", '')
        is_new_pharma = self.__check_pharma(name_pharma=name_pharma)
        remote_password = infos.get("remote_password", 'j')
        remote_password2 = infos.get("remote_password2", 'j_')
        password = ''
        if remote_password == remote_password2:
            password = remote_password
        if last_pharma:
            last_code = int(last_pharma.code_pharma)
        new_user = None
        if len(password) >= 8 and len(name_pharma) >= 5:
            new_user = self.__create_user(username=name_pharma, password=password)
        new_pharma = Pharma.objects.create()

        return 0
    
    def __create_user(self, username='pharma', password="pharma1212")->User:
        new_user = User.objects.create(username=username)
        new_user.set_password(password)
        new_user.save()

        return new_user
    def __check_pharma(self, name_pharma='pharma')->int:
        is_new_pharma = Pharma.objects.filter(name_pharma=name_pharma)
        if len(is_new_pharma):
            return False
        return True


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