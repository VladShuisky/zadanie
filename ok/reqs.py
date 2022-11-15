import requests
ACCESS_TOKEN = 'tkn1ECj57p4ikvTBZEG5oY9JuCdFJTsTNLBuIs2vksELxKVOX0JXV5awn1BGwGslPvFPN1'
APPLICATION_KEY = 'CCJQENKGDIHBABABA'
SECRET_APP_KEY = 'F1219CB3986EDB73D76794E2'

images = [
    'https://bipbap.ru/wp-content/uploads/2017/04/0_7c779_5df17311_orig.jpg',
    'https://www.iguides.ru/upload/medialibrary/9f8/9f8fdff471b7d281f81f694c100b5adc.png',
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4ceVv9RipRiixDZTEN_FljTyyTRCZoBLSut02tY_0&s',
    'https://st.depositphotos.com/1000618/2346/i/450/depositphotos_23462648-stock-photo-flag-of-kazakhstan-on-abstract.jpg',


]


data = {
    'message': 'HELLO',
    'group_id': '70000001154611',
    'access_token': ACCESS_TOKEN,
    'application_key': APPLICATION_KEY,
    'application_secret_key': SECRET_APP_KEY,
    'attachments': images
}

response = requests.post('http://127.0.0.1:8000/post_ok/', json=data)
print(response.json())

