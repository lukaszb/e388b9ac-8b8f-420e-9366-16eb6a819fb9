import json
import pytest
import shutil
from pathlib import Path
from rest_framework.test import APIClient
from swheros import api


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def all_people(settings):
    with open(str(settings.TEST_DATA_DIR / 'all-people.json')) as fin:
        return json.load(fin)


@pytest.fixture
def all_planets(settings):
    with open(str(settings.TEST_DATA_DIR / 'all-planets.json')) as fin:
        return json.load(fin)


@pytest.fixture
def dummy_collection(tmpdir, settings):
    settings.COLLECTIONS_DIR = Path(str(tmpdir))

    collection = api.create_collection()
    full_csv = settings.TEST_DATA_DIR / 'full.csv'
    shutil.copy(src=str(full_csv), dst=collection.full_filename)
    return collection

@pytest.fixture
def dummy_collection_first10(tmpdir, settings):
    settings.COLLECTIONS_DIR = Path(str(tmpdir))

    collection = api.create_collection()
    # api.write_csv(collection.full_filename, people=all_people, planets=all_planets)
    csv_file = settings.TEST_DATA_DIR / 'first10.csv'
    shutil.copy(src=str(csv_file), dst=collection.full_filename)
    return collection
