import json
import random
from imgurpython import ImgurClient


class GetRandomImage:

    def __init__(self):
        with open("client.json", 'r')as f:
            self.client_info = json.load(f)
        f.close()

        with open("data.json", "r")as data_f:
            self.albums = json.load(data_f)
        data_f.close()

        self.client_secret = self.client_info['info']['secret']
        self.client_id = self.client_info['info']['id']

        self.client = ImgurClient(self.client_id, self.client_secret)

        self.current_album = None

    def load_album(self):
        album_id = random.choice(self.albums['albums'])

        album = self.client.get_album(album_id)
        album_images = self.client.get_album_images(album_id)
        album_data = {'title': album.title,
                      'id': album_id,
                      'size': len(album_images),
                      'images': []}
        for image in album_images:
            album_data['images'].append({'url': image.link,
                                         'title': image.title if image.title else 'Untitled'})
        self.current_album = album_data

    def custom_album(self, imgur_album_id):
        if type(imgur_album_id) is not str:
            raise ValueError('imgur_album_id must be type: str not: {} '.format(str(type(imgur_album_id))))
        if imgur_album_id is None:
            raise ValueError('imgur_album_id can not be NoneType')

        album = self.client.get_album(imgur_album_id)
        album_images = self.client.get_album_images(imgur_album_id)
        album_data = {'title': album.title,
                      'id': imgur_album_id,
                      'size': len(album_images),
                      'images': []}
        for image in album_images:
            album_data['images'].append({'url': image.link,
                                         'title': image.title if image.title else 'Untitled'})
        self.current_album = album_data
