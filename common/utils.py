from typing import Any
#from django.utils.deconstruct import deconstructible
from dataclasses import dataclass
from datetime import datetime

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@dataclass
class Response:
    status: bool
    message: str
    data: dict

#@deconstructible
#이거 이해하고싶다.
#deconstructible 안 써도 되는데 왜 써놓은건지..
#__call__에 A에는 모델, B에는 파일명이 들어가는 이유는 뭔지..
class Test(object):
    def __init__(self, sub_path):
        self.path = sub_path
    
    def __call__(self, wtf, filename):
        print(self.path)
        format = filename.split('.')[1]
        result = '/'+self.path+'-'+str(datetime.utcnow().strftime('%Y%m%d-%H%M%S-%f')[:-3])+'.'+format
        return self.path+result