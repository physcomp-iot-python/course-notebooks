import urequests

ADAFRUIT_IO_API_PATH = 'https://io.adafruit.com/api/v2'

class Feed:
    def __init__(self, 
                 user_name,
                 key,
                 feed_name,
                 ):
        self.headers = {'Content-Type': 'application/json',
                        'X-AIO-Key':key}
        self.post_url = '{api_path}/{user_name}/feeds/{feed_name}/data.json'.format(api_path=ADAFRUIT_IO_API_PATH,
                   user_name=user_name,
                   feed_name=feed_name)
        
    def post(self, value):
        json = dict(value=value)
        resp = urequests.post(self.post_url,json=json,headers=self.headers)
        return resp