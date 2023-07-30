import requests
from tqdm import tqdm
from time import sleep


class YD:

  def __init__(self, yd_token, list_data):
    self.yd_token = yd_token
    self.list_data = list_data

  def download_photos(self):
    url_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
    params_f = {'path': '/'+'new_folder'}
    headers_f = {'Authorization': 'OAuth '+self.yd_token}
    requests.put(url_folder, headers=headers_f, params=params_f)
    for photo_info in tqdm(self.list_data, desc='Загружаем фото'):
      url_photos = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
      params_p = {
        'path': '/new_folder/'+str(list(photo_info.keys())[0]),
        'url': list(photo_info.values())[0]
        }
      headers_p = {'Authorization': 'OAuth '+self.yd_token}
      requests.post(url_photos, headers=headers_p, params=params_p)
      sleep(2)
