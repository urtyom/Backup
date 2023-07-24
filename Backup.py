import requests
import json
from datetime import datetime
from tqdm import tqdm
from time import sleep


class VK:

  def __init__(self, access_token, user_id, y_token, version='5.131', q_ph=5):
    self.token = access_token
    self.id = user_id
    self.yd_token = y_token
    self.version = version
    self.q_photo = q_ph
    self.params = {'access_token': self.token, 'v': self.version}

  def photos_info(self):
    url = 'https://api.vk.com/method/photos.get'
    params = {
      'owner_id': self.id,
      'album_id': 'profile',
      'rev': '0',
      'extended': '1',
      'count': self.q_photo
      }
    response = requests.get(url, params={**self.params, **params})
    data = response.json()['response']['items']
    list_data = []
    list_likes = []
    for like in data:
      list_likes.append(like['likes']['count'])

    for photo in tqdm(data, desc='Получаем информации о фото'):
      dict_data = {}
      date_u = int(photo['date'])
      date = datetime.utcfromtimestamp(date_u).strftime('%Y-%m-%d')
      like = photo['likes']['count']
      likes_count = list_likes.count(photo['likes']['count'])
      type_size = photo['sizes'][-1]['type']
      if likes_count > 1:
        dict_data[f"{like}, {date}"] = photo['sizes'][-1]['url']
        dict_data['size'] = type_size
      elif likes_count < 2:
        dict_data[like] = photo['sizes'][-1]['url']
        dict_data['size'] = type_size
      list_data.append(dict_data)
      sleep(2)

    with open('new_file_json', 'w') as f:
      json.dump(list_data, f)
      
    return list_data

  def download_photos(self):
    url_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
    params_f = {'path': '/'+'new_folder'}
    headers_f = {'Authorization': 'OAuth '+self.yd_token}
    requests.put(url_folder, headers=headers_f, params=params_f)
    for photo_info in tqdm(vk.photos_info(), desc='Загружаем фото'):
      url_photos = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
      params_p = {
        'path': '/new_folder/'+str(list(photo_info.keys())[0]),
        'url': list(photo_info.values())[0]
        }
      headers_p = {'Authorization': 'OAuth '+self.yd_token}
      requests.post(url_photos, headers=headers_p, params=params_p)
      sleep(2)


yd_token = open('yd_token.txt').read()
access_token = open('vk_token.txt').read()
user_id = open('user_id.txt').read()
q_ph = 3
vk = VK(access_token, user_id, yd_token, q_ph=q_ph)
vk.download_photos()
