from rest_framework import serializers

from app.models import MedCollection


class MedCollectionSeria(serializers.ModelSerializer):
    class Meta:
        model = MedCollection
        fields = '__all__'
