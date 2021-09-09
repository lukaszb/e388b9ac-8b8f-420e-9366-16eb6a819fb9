import pytest
from django.utils import timezone
from freezegun import freeze_time
from swheros import api


pytestmark = pytest.mark.django_db


def test_collection_list(api_client):
    col1 = api.create_collection()
    col2 = api.create_collection()
    col3 = api.create_collection()

    response = api_client.get('/api/collections')
    assert response.status_code == 200
    assert response.data == [
        {"id": col3.id, "date": col3.date, "items_count": 0},
        {"id": col2.id, "date": col2.date, "items_count": 0},
        {"id": col1.id, "date": col1.date, "items_count": 0},
    ]


def test_collection_details(api_client):
    with freeze_time('2021-09-08 15:00Z'):
        col = api.create_collection()

    response = api_client.get(f'/api/collections/{col.id}')
    assert response.status_code == 200
    assert response.data == {
        "id": col.id,
        "date": timezone.make_aware(timezone.datetime(2021, 9, 8, 15)),
        "items_count": 0,
    }

def test_collection_data(api_client, dummy_collection):
    response = api_client.get(f'/api/collections/{dummy_collection.id}/data')
    assert response.status_code == 200
    items = response.data["items"]
    assert [item["name"] for item in items] == [
        "Luke Skywalker",
        "C-3PO",
        "R2-D2",
        "Darth Vader",
        "Leia Organa",
        "Owen Lars",
        "Beru Whitesun lars",
        "R5-D4",
        "Biggs Darklighter",
        "Obi-Wan Kenobi",
    ]

    response = api_client.get(f'/api/collections/{dummy_collection.id}/data?page=2')
    assert response.status_code == 200
    items = response.data["items"]
    assert [item["name"] for item in items] == [
        "Anakin Skywalker",
        "Wilhuff Tarkin",
        "Chewbacca",
        "Han Solo",
        "Greedo",
        "Jabba Desilijic Tiure",
        "Wedge Antilles",
        "Jek Tono Porkins",
        "Yoda",
        "Palpatine",
    ]


@pytest.mark.parametrize("fields, expected_data", [
    ("gender,date", [
        {"gender": "female", "date": "2014-12-20", "Count": 2},
        {"gender": "male", "date": "2014-12-20", "Count": 5},
        {"gender": "n/a", "date": "2014-12-20", "Count": 3},
    ]),
    ("homeworld,date", [
        {"homeworld": "Alderaan", "date": "2014-12-20", "Count": 1},
        {"homeworld": "Naboo", "date": "2014-12-20", "Count": 1},
        {"homeworld": "Stewjon", "date": "2014-12-20", "Count": 1},
        {"homeworld": "Tatooine", "date": "2014-12-20", "Count": 7},
    ]),
    ("homeworld,birth_year", [
        {'Count': 1,
        'birth_year': '19BBY',
        'homeworld': 'Alderaan'},
        {'Count': 1,
        'birth_year': '33BBY',
        'homeworld': 'Naboo'},
        {'Count': 1,
        'birth_year': '57BBY',
        'homeworld': 'Stewjon'},
        {'Count': 1,
        'birth_year': '112BBY',
        'homeworld': 'Tatooine'},
        {'Count': 1,
        'birth_year': '19BBY',
        'homeworld': 'Tatooine'},
        {'Count': 1,
        'birth_year': '24BBY',
        'homeworld': 'Tatooine'},
        {'Count': 1,
        'birth_year': '41.9BBY',
        'homeworld': 'Tatooine'},
        {'Count': 1,
        'birth_year': '47BBY',
        'homeworld': 'Tatooine'},
        {'Count': 1,
        'birth_year': '52BBY',
        'homeworld': 'Tatooine'},
        {'Count': 1,
        'birth_year': 'unknown',
        'homeworld': 'Tatooine'},
    ]),
])
def test_collection_data(fields, expected_data, api_client, dummy_collection_first10):
    url = f'/api/collections/{dummy_collection_first10.id}/data/distinct?fields={fields}'
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data == expected_data