from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import api
from . import serializers


def html_app(request):
    return render(request, 'app.html')


@api_view(["POST"])
def collection_create(request):
    collection = api.fetch_new_collection()
    return Response({
        "id": collection.id,
        "date": collection.date,
    })


@api_view(["GET"])
def collection_list(request):
    collections = api.get_all_collections()
    serializer = serializers.Collection(collections, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def collection_details(request, collection_id):
    collections = api.get_all_collections()
    collection = get_object_or_404(collections, id=collection_id)
    serializer = serializers.Collection(collection)
    return Response(serializer.data)
    # items = api.get_collection_data(collection.full_filename)
    # return Response({
    #     "id": collection.id,
    #     "date": collection.date,
    #     # "items": items,
    # })


@api_view(["GET"])
def collection_data(request, collection_id):
    page = get_page_param(request)
    collections = api.get_all_collections()
    collection = get_object_or_404(collections, id=collection_id)
    items = api.get_collection_data(collection.full_filename, page=page)
    return Response({
        "items": items,
    })


@api_view(["GET"])
def collection_data_distinct(request, collection_id):
    collections = api.get_all_collections()
    collection = get_object_or_404(collections, id=collection_id)
    fields = request.query_params.get('fields').split(',')
    data = api.get_collection_data_distinct_for_fields(collection.full_filename, fields=fields)
    return Response(data)


def get_page_param(request):
    page_param = request.query_params.get('page')
    try:
        page = int(page_param)
    except (TypeError, ValueError) as err:
        page = None
    return page
