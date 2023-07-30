import requests
import json
from datetime import datetime
from tqdm import tqdm
from time import sleep


class VK:

  def __init__(self, access_token, user_id, version='5.131', q_ph=5):
    self.token = access_token
    self.version = version
    self.q_photo = q_ph
    self.params = {'access_token': self.token, 'v': self.version}

    if user_id.isdigit() == True:
      self.id = user_id
    else:
      url = 'https://api.vk.com/method/utils.resolveScreenName'
      params = {
      'screen_name': user_id
      }
      response = requests.get(url, params={**self.params, **params})
      self.id = response.json()['response']['object_id']


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

    for photo in tqdm(data, desc='Получаем информацию о фото'):
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
