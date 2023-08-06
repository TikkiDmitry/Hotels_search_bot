import requests


def request_city(data):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": data[1], "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}

    headers = {
        "X-RapidAPI-Key": "1e397c7f89msh6f293dccbf0ba22p103cb7jsn06a89940fed6",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    id_city = ''

    response = requests.get(url, headers=headers, params=querystring)
    result = response.json()['sr']

    for i in result:
        id_city = i['gaiaId']
        break

    return request_hotels(id_city, data)


def request_hotels(id_city, data):
    many_hotel = []

    if data[0] == '/lowprice':
        sort = 'PRICE_LOW_TO_HIGH'
    elif data[0] == '/highprice':
        sort = '-PRICE_LOW_TO_HIGH'
    else:
        sort = 'PRICE_LOW_TO_HIGH'

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {'currency': 'USD',
               'eapid': 1,
               'locale': 'ru_RU',
               'siteId': 300000001,
               'destination': {
                   'regionId': id_city  # id из первого запроса
               },
               'checkInDate': {'day': 7, 'month': 12, 'year': 2023},
               'checkOutDate': {'day': 9, 'month': 12, 'year': 2023},
               'rooms': [{'adults': 1}],
               'resultsStartingIndex': 0,
               'resultsSize': 10,
               'sort': sort,
               'filters': {'availableFilter': 'SHOW_AVAILABLE_ONLY'}
               }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "1e397c7f89msh6f293dccbf0ba22p103cb7jsn06a89940fed6",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)
    result = response.json()['data']['propertySearch']['properties']

    for i in result:
        one_hotel = []
        one_hotel.append(i['name'])
        one_hotel.append(f"https://www.hotels.com/h{i['id']}.Hotel-Information")

        many_hotel.append(one_hotel)

    return many_hotel[:int(data[2])]


def request_detail_hotels(id_city, data):
    pass
