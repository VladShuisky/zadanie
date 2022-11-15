import requests, json, os
from fastapi import FastAPI
from ok_api import OkApi, Upload
from pydantic import BaseModel
from typing import Union, List

class ApiOkSession:
    def __init__(self, data):
        self.ok_session=OkApi(access_token=data['access_token'], 
                            application_key=data['application_key'], 
                            application_secret_key=data['application_secret_key'])
        self.data = data
        self.upload = Upload(self.ok_session)

    def local_images_download(self):
        attachments = []
        local_images_list = []
        if type(self.data['attachments']) == str:
            attachments = self.data['attachments'].split()
        for i in range(0, len(self.data['attachments'])):
            image_name = f'image{i}'
            image_bytes = requests.get(self.data['attachments'][i]).content
            image_draft = open(f'{image_name}.jpg', 'wb')
            image_draft.write(image_bytes)
            image_draft.close()
            local_images_list.append(f'{image_name}.jpg')
        return local_images_list

    def add_photos_to_attachments(self):
        local_images = self.local_images_download()
        response = self.upload.photo(photos=local_images, group_id=self.data['group_id'])
        print(local_images)
        print(response)
        tokens = [el['token'] for el in response['photos'].values()]
        for image in local_images:
            os.remove(image)
        return tokens

    def get_attachment(self):
        attachment_photos_tokens = self.add_photos_to_attachments()
        attachments = {
            'media': [
                {
                    'type': 'text',
                    'text': self.data['message']
                },
                {
                    'type': 'photo',
                    'list': [{'id': token} for token in attachment_photos_tokens] 
                }
            ]
        }
        print(attachments)
        return attachments

    def publish_to_group(self):
        attachments = self.get_attachment()
        response = self.ok_session.mediatopic.post(
            type='GROUP_THEME',
            gid=self.data['group_id'],
            attachment = json.dumps(attachments)
        )
        return response

    def start(self):
        response = self.publish_to_group()
        return response.json()



class Data(BaseModel):
    message: str
    group_id: str
    access_token: str
    application_key: str
    application_secret_key: str
    attachments: Union[List[str], str]

app = FastAPI()
@app.post('/post_ok/')
async def get_request(request_data: Data):
    ok_response = ApiOkSession(dict(request_data)).start()
    return ok_response

