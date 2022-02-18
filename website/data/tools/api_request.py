import requests

URL = 'https://pxnet2.stat.fi:443/PXWeb/api/v1/en/Postinumeroalueittainen_avoin_tieto/2022/paavo_pxt_12f7.px'
r = requests.get(URL)
data = r.json()

postcodes = data['variables'][0]['values']
value_texts = data['variables'][0]['valueTexts']


