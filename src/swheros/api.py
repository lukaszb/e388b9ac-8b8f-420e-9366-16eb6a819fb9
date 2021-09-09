from swheros.models import Collection
from django.conf import settings
from pathlib import Path
from typing import List
import concurrent.futures
import petl
import requests
import frogress
import os


def fetch_new_collection():
    collection = create_collection()
    people = get_all_people()
    planets = get_all_planets()
    data = write_csv(filename=collection.full_filename, people=people, planets=planets)
    collection.items_count = data.nrows()
    collection.save()
    return collection


def create_collection():
    return Collection.objects.create()


def get_all_collections():
    return Collection.objects.all().order_by("-date")


def get_collection_data(filename, page=None):
    page_size = 10
    page = page or 1
    start = (page - 1) * page_size
    end = start + page_size
    table = petl.fromcsv(filename)
    return list(table.dicts()[start:end])


def get_collection_data_distinct_for_fields(filename, fields):
    table = petl.fromcsv(filename)
    data = table.cut(*fields).distinct(key=fields, count="Count")
    return list(data.dicts())


def get_all_people():
    return get_all_from_swapi("people")


def get_all_planets():
    return get_all_from_swapi("planets")


def get_all_from_swapi(resource_name):
    # could use swapi library (https://github.com/phalt/swapi-python) but it fetches pages one by one
    # and even for only 8 pages it takes significant amount of time
    print(f" => fetching all swapi resources {resource_name}")
    url = get_swapi_url(f"/api/{resource_name}")
    first_response = requests.get(url)
    if first_response.status_code != 200:
        raise Exception(f"Wrong response (expected 200, got {first_response.status_code} for url: {url})")

    total_count = first_response.json()["count"]
    all_results = first_response.json()["results"]

    total_pages = total_count // 10
    if total_count % 10 != 0:
        total_pages += 1
    pages = range(2, total_pages + 1)
    urls = [get_swapi_url(f"/api/{resource_name}?page={page}") for page in pages]
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(requests.get, url): url for url in urls}
        futures = concurrent.futures.as_completed(future_to_url)
        futures = frogress.bar(futures)
        for future in futures:
            url = future_to_url[future]
            try:
                response = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                all_results += response.json()["results"]

    return all_results


def get_swapi_url(path):
    return f"{settings.SWAPI_BASE_URL}{path}"


def write_csv(filename, people, planets):
    planets_map = {p['url']: p for p in planets}
    data = petl.fromdicts(people)
    new_data = (data
        .addfield('date', lambda p: p["edited"][:10])
        .cutout('species', 'vehicles', 'films', 'starships', 'url', 'created', 'edited')
        .convert('homeworld', lambda url: planets_map.get(url, {}).get('name'))
    )

    dirpath = Path(filename).parent
    if not dirpath.exists():
        os.makedirs(str(dirpath))

    print(f' => new csv with sw heros written to {filename}')
    new_data.tocsv(filename)
    return new_data
