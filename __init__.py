from VK import VK
from YD import YD
import configparser


if __name__ == '__main__':
  config = configparser.ConfigParser()
  config.read('settings.ini')
  yd_token = config['Backup']['yd_token']
  access_token = config['Backup']['vk_token']
  user_id = input('Ведите id или короткий id: ')
  q_ph = 3
  vk = VK(access_token, user_id, q_ph=q_ph)
  yd = YD(yd_token, vk.photos_info())
  result = yd.download_photos()
