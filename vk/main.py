from typing import Union, List
from vkrequest import VkRequest

from fastapi import FastAPI
from pydantic import BaseModel


class Data(BaseModel):
    access_token: str
    message: str
    owner_id: str     #id группы,  в которой выкладывается пост (имеет '-' перед последовательностю чисел)
    attachments: Union[List[str], str] = None


app = FastAPI()

@app.post("/post_vk/")
async def get_request(request_data: Union[list[Data], Data]):
    responses = []
    if type(request_data) != list:
        request_data = [].append(request_data)
    for request_data_body in request_data:
        vk_req = VkRequest('https://api.vk.com/method/wall.post', dict(request_data_body)).start()
        responses.append(vk_req)
    return responses
        


    

