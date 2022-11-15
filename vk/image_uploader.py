import vk_api, os
from vk_api import VkUpload
import requests

class Vk_Api:
    def __init__(self, token, album_id, link_to_upload, owner_id:str):
        self.session = vk_api.VkApi(token=token)
        self.token = token
        self.album_id = album_id
        self.owner_id = owner_id.replace('-', '')
        self.url = link_to_upload

    def uploadImage(self):
        print('upload_image')
        upload = VkUpload(self.session)
        r = requests.get(self.url).content
        image = open('image.jpg', 'wb')
        image.write(r)
        print(self.album_id, self.owner_id, self.url)
        photo_list = upload.photo(photos='image.jpg', album_id=self.album_id, group_id=int(self.owner_id))
        image.close()
        os.remove('image.jpg')
        print('end_upload_image')
        return photo_list

