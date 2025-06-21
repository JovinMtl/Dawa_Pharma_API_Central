from rest_framework import serializers

from app.models import MedCollection, Pharma


class MedCollectionSeria(serializers.ModelSerializer):
    class Meta:
        model = MedCollection
        fields = '__all__'


class PharmaSeria(serializers.ModelSerializer):
    class Meta:
        model = Pharma
        fields = '__all__'