from rest_framework import serializers


class Collection(serializers.Serializer):
    id = serializers.ReadOnlyField()
    date = serializers.ReadOnlyField()
    items_count = serializers.ReadOnlyField()
