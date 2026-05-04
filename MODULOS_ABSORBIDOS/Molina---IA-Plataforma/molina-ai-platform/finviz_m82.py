import requests
import re
def get_v(t):
 url=f'https://finviz.com/quote.ashx?t={t}'
 h={'User-Agent':'Mozilla/5.0'}
 r=requests.get(url,headers=h).text
 pe=re.findall(r'P/E</td><td.*?>(.*?)</td>',r)
 m=re.findall(r'Market Cap</td><td.*?>(.*?)</td>',r)
 print(f'{t} | Cap: {m[0] if m else "N/A"} | P/E: {pe[0] if pe else "N/A"}')
[get_v(t) for t in ['XOM','NVDA','ORCL']]