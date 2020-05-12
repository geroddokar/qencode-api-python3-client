from tusclient import client
from . utils import get_tus_from_url

class UploadStatus(object):
  def __init__(self, error = None, url= None, status= None):
    self.url = url
    self.error = error
    self.status = status


def upload(file_path=None, url=None, chunk_size=None, log_func=None):
    
    try:
        my_client = client.TusClient(url=url)
        uploader = my_client.uploader(file_path=file_path, chunk_size=chunk_size, log_func=log_func)
        uploader.upload()
        url_storage = uploader.url
        tus_url = get_tus_from_url(url_storage)
        return UploadStatus(url=tus_url, status='Ok')
    except:
       print('Error uploading file to ' + url)
       raise