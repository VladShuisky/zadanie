import vk_api, os
from vk_api import VkUpload
from image_uploader import Vk_Api
import requests
import logging
TOKEN = 'vk1.a.cZdUGMMdwKfgfvxjID0O3PK6PMFE1rrfeSRf3HR7opxxkMjJB-QMCmRwj_IySxQ5OObP-sNOUbkqwWu-Y9f1otuGjjGi95gSPzLskRbBoQ3WMrtKYcwfslqdyAQ72oE37Ay48OVbSC2mukqxAn6yRHoyd2CRJYSaoxMLW8xc6ZUq7_HunO3B4AROoc41A79ERhcyxut2jGwIx-p76EtOtw'
API_VERSION = '5.131'

logging.basicConfig(level=logging.DEBUG)
URL =   'https://api.vk.com/method/wall.post'

class VkRequest:
    def __init__(self, url, data):
        self.data = data
        self.url = url

    def local_images_download(self, attachments):
        local_images_list = []
        if type(attachments) == str:
            attachments = attachments.split()
        for i in range(0, len(attachments)):
            image_name = f'image{i}'
            image_bytes = requests.get(attachments[i]).content
            image_draft = open(f'{image_name}.jpg', 'wb')
            image_draft.write(image_bytes)
            image_draft.close()
            local_images_list.append(f'{image_name}.jpg')
        return local_images_list


    def images_wall_save(self):
        data = self.data
        attachments, owner_id=data['attachments'], int(data['owner_id'].replace('-', ''))
        session = vk_api.VkApi(token=self.data['access_token'])
        upload = VkUpload(session)
        local_images_list = self.local_images_download(attachments)
        vk_server_loaded_images = upload.photo_wall(photos=local_images_list, group_id=owner_id)   #photos, group_id, caption-описание
        for image in local_images_list:
            os.remove(image)
        image_urls = ['photo' + str(image['owner_id']) + '_' + str(image['id']) for image in vk_server_loaded_images]
        image_urls = ','.join(image_urls)
        return image_urls

    def send_request(self):
        data = self.data
        print(data)
        response = requests.post(self.url, data)
        return response

    def send_full_post(self):
        data = self.data
        if type(data['attachments']):    
            image_links = self.images_wall_save()
            data['attachments'], data['owner_id'] = image_links, '-' + data['owner_id']
            print(data)
        response = self.send_request()
        return response.json()

    def start(self):
            self.data['v'] = API_VERSION
            response = self.send_full_post()
            return response




























    # def upload_images(self):
    #     album, photo, token, owner_id = self.data['album_id'], self.data['photo_attachments'], self.data['access_token'], self.data['owner_id'] 
    #     image = Vk_Api(token, album, photo, owner_id).uploadImage()
    # def images_wall_save(self):
    #     place_for_image_data = {
    #         'v': '5.131',
    #         'access_token': self.data['access_token'],
    #         'group_id': self.data['owner_id']
    #     }
    #     place_for_image = requests.post('https://api.vk.com/method/photos.getWallUploadServer', place_for_image_data)
    #     place_for_image = place_for_image.json()
    #     print(place_for_image)
    #     load_data = {
    #         'photo': open('image1.jpg', 'rb')
    #     }
    #     uploaded = requests.post(place_for_image['response']['upload_url'], files=load_data)
    #     uploaded = uploaded.json()
    #     data = {
    #         'v': '5.131',
    #         'access_token': self.data['access_token'],
    #         'group_id': self.data['owner_id'],
    #         'photo': uploaded['photo'],
    #         'server': uploaded['server'],
    #         'hash': uploaded['hash'],
    #     }
    #     saving = requests.post('https://api.vk.com/method/photos.saveWallPhoto', data=data)
    #     response = saving.json()['response'][0]
    #     image_link = 'photo' + str(response['owner_id']) + '_' + str(response['id'])
    #     publication_data = {
    #         'v': '5.131',
    #         'access_token': self.data['access_token'],
    #         'owner_id': '-' + self.data['owner_id'],
    #         'message': '123',
    #         'attachments': image_link

    #     }
    #     publication = requests.post('https://api.vk.com/method/wall.post', publication_data)
        
        
    # def upload_images(self):
    #     data = self.data
    #     attachments, owner_id, album_id = data['photo_attachments'], int(data['owner_id'].replace('-', '')), data['album_id']
    #     session = vk_api.VkApi(token=self.data['access_token'])
    #     upload = VkUpload(session)
    #     local_images_list = self.local_images_download(attachments)
    #     print(local_images_list)
    #     print(owner_id, album_id)
    #     vk_server_loaded_images = upload.photo(local_images_list, album_id, owner_id)
    #     return vk_server_loaded_images
    #     image = image[0]
    #     owner_id, id = image['owner_id'], image['id']
    #     image_link = f'photo{owner_id}_{id}'
    #     return image_link