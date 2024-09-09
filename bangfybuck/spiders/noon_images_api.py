import requests
import json
def noon_api(query):
  url = f"https://www.noon.com/_next/data/schmatalog-781e01b930ebecec8176c4a750aecc023d8fb574/egypt-en/search.json?limit=50&originalQuery={query}&page=1&q={query}&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc&catalog=search"

  payload = {}
  headers = {
    'accept': '*/*',
    'accept-language': 'en',
    'cookie': 'visitor_id=9b77294a-d3a1-4ddf-8d9c-3e58a660fcce; _gcl_au=1.1.765823531.1719747009; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22XUCdu88fEm8ER8GJBQFp%22%7D; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3Anull%7D; _ga=GA1.2.217995138.1719747010; _fbp=fb.1.1719747009856.11405598015434404; _scid=361025dc-9126-45cf-9045-8e350573afa5; _tt_enable_cookie=1; _ttp=Uc0S0m67yVSGh66RyU-GMLKHDgw; th_capi_em=a737cf27d809ac461dc048a9a4feaa10aea3a5afe757378240fbcf981e4e763f; _ScCbts=%5B%22289%3Bchrome.2%3A2%3A5%22%5D; _sctr=1%7C1725397200000; _gid=GA1.2.1627730137.1725603851; ZLD887450000000002180avuid=99bf297c-b285-423d-8efd-345cb8403eda; review_lang=xx; isAppInstallBannerDismissed=true; _clck=16mgfyj%7C2%7Cfp1%7C0%7C1642; nloc=en-eg; AKA_A2=A; bm_mi=858FE2894B34356AFB5164000A171A05~YAAQTOF6XLTof5qRAQAAVP2i1RmSKfQxeovxu4yD0UCSXQ+igqzwRhsB+aF3txy5SpsK8qJfBisHtP2Jyi8UBRJeybx04AEpB4dDJ71JzH0rW9O9y435Qzpc4VJpQylPHsYg+pt2xCk1Y3FLruO0hCSqLTnKnCz5VXyDpWCtPUOJFs9ZltxEXDkq+eWkQg56mHNW5Ev6PcYc6Myu7D5eUCWwYc/gOIMCf2e72eZ5HOJvEk/O68BNcAajYA5bwcBT2v0uwu5rvPYUDw8LMeGSPai/crUvPy5AxujcivKMD/lf2Atmqsco4Wm/T6tBkNgJuKZzUc7LN4Vps2/lCrMGqP6ZGPPv92gA~1; __gads=ID=85d574fcddb86eca:T=1724084524:RT=1725866115:S=ALNI_MbO4EOjejxwJELAfX7xUNiKAkY2dQ; __gpi=UID=00000ed14de9b1d3:T=1724084524:RT=1725866115:S=ALNI_MZSV7fgURU4dOSe_tnjqjTjTI-rFw; __eoi=ID=9963782eee074acd:T=1724084524:RT=1725866115:S=AA-AfjaPsIPnVHL43RRxYMILlu5a; ak_bmsc=B067A45EF97F84156B971C8506652A30~000000000000000000000000000000~YAAQJ1CMTx/kSMCRAQAA4fup1RmnYCX1ik2KIbEYJfXso230h3427NK2ASI0A3CZEPlDsQ10lrVL5vQME3Jf7n1AdktBw4NBQi7GS6LT0LQoNDf0lxvcTlejMIRbqnTEiizuRvj7+vX2ZGVLShLQ5T0wSMNNldQTHdimiYnaQojKpO4hACALdqLHi5pHd9R7llnZtMNaum9PUjbzUQDFxo6+OHpTmC08XQUPMBc0F4K64jHAXfVVSyIjjdtC8BPT4DQeU66VhHn6ESMPk0PlcmDtDFnT9eDdl3BByIRnACkzx92DyTlnUX8Qh6nTxdmjljC4ljAV/YVnk/w8CZna3qUVWZTkOMnM9Ic+d6jun2956Z7qqMq5/jGcNR2C2CjbyuaWTpM5xpvBj1dtyz/QcPLecNWYz3+XqWjCsRlyjmn/F3qpE1Olpfu+WpaQe4V4FvhIVVYz+I+y8A3d/sLajHdEz91DxuQldSJlhQaj4o2ojQ3qdkHe2etZXbXUA+OavqTwketD6mWY/iUZKQ==; ZLDsiq663f5c2580454f7ed6b7bbe12e575c5570eb9b21832ce32b902ca6cbca6ffc2bavuid=99bf297c-b285-423d-8efd-345cb8403eda; _etc=IyYy1fNEG9alqU6U; _scid_r=eBA2ECXckSbPz5BFjjUFc6-l8pn4Gw3fSS0SDA; _uetsid=a0f077f06c1811ef8d9f8b316358e56a; _uetvid=1bbdceb036d411efb2efef34a68aeb67; _clsk=xp0pje%7C1725866737163%7C15%7C0%7Cn.clarity.ms%2Fcollect; nguestv2=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJraWQiOiIyNjE0YzQ4NTM4YTk0MjE0ODBlNDJjZDBhZmIzN2EyZiIsImlhdCI6MTcyNTg2NjkwMCwiZXhwIjoxNzI1ODY3MjAwfQ.8PTASswVOvan0_Ai4IAS5vR9AFS6Wcf6C98uC3HqvJ4; bm_sv=7571026074041505C70A3590314B70EB~YAAQJ/hVaPh5YcKRAQAABDKv1Rkiq0podlfRH5rhHnaByPv0y6Lb4X9NZPfNEfNw9GnjTvjHzP9X7DpJMXQ4bQ9j8YZUUqW4XWETrrSsvdJ/fdeUcOfI4i9lvoQ2j06walz/8DlMt1KcYs+7uZXAZLVoA48lafEEGmzUOhrJl3otBQKhRMh9riiSZNWS1G8mblKUipMlFH2xltISgiGAOM4s0q3wWFIkzoUFR5kse7lkhW4W46Ilk916pEKSbB0=~1; ZLDsiq3b3ce696144e42ab351af48092266ce3dda2b3c7b2ad6e09ba5d18504de03180tabowner=undefined; RT="z=1&dm=noon.com&si=ab54c411-4d4e-4e2a-ba0c-195da7c2f121&ss=m0un2svg&sl=7&tt=emy&obo=5&bcn=%2F%2F0217991b.akstat.io%2F&rl=1&nu=d41d8cd98f00b204e9800998ecf8427e&cl=1jo41"; bm_sv=7571026074041505C70A3590314B70EB~YAAQJ/hVaL4MZMKRAQAALXHJ1RkvNSXfCyYTk011vE36xJ4I4PsgfC8zgElPk2Flaisym7oUNA0mqEyGlwmnX2WDALFg5nXD5gegxCjVJlhQDMuSzJ434Yhl7adRy/chkKYoLjh1V/VNuyo8nPm6bSJtoBBpvUyC/fgLyqRf2cyGkalsVNmVsodPTFrrF/WdRxA19cGO4x3J0S4hMPMriFitVZUhRaiRnn4s8/z4Nzy26OqD2Fb6PhT/GPDHOoE=~1; x-whoami-headers=eyJ4LWxhdCI6IjMwMDYzMTQzNyIsIngtbG5nIjoiMzEyMjA1MjI0IiwieC1hYnkiOiJ7XCJwZHBfYm9zLmVuYWJsZWRcIjoxLFwibXBfaWNvbl92Mi5lbmFibGVkXCI6MSxcInBkcF9mbHlvdXQuZmx5b3V0X3ZhbHVlXCI6MCxcImNhdGVnb3J5X2Jlc3Rfc2VsbGVyLmVuYWJsZWRcIjoxLFwicGRwX3NjcmVlbnNob3Rfc2hhcmVfc2hlZXQuZW5hYmxlZFwiOjF9IiwieC1lY29tLXpvbmVjb2RlIjoiRUctQ0FJLVMxMiIsIngtYWItdGVzdCI6WzgzMCw4NTEsOTExLDk1MSw5NjFdfQ==',
    'priority': 'u=1, i',
    'referer': 'https://www.noon.com/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36',
    'x-nextjs-data': '1'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  data=response.json()
  noon_data=[]
  for hit in data['pageProps']['catalog']['hits']:
      item_data = {
                      "name": hit['brand']+ ' '+ hit['name'],
                      'picture': 'https://f.nooncdn.com/p/'+hit['image_key']+'.jpg?format=avif&width=400'
                  }
      noon_data.append(item_data)

  with open("noon_images.json",'w') as file:
      json.dump(noon_data,file,indent=4)

    
