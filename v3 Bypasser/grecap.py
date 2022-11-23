from re import findall
from httpx import Client
from user_agent import generate_user_agent as gua


def googRecap(proxy:str, aURL:str):
    with Client(http2=True, proxies=proxy) as session:

        #! Set Headers
        session.headers.update({'User-Agent': gua(), 'content-type': 'application/x-www-form-urlencoded'})

        #! Rebuild URL
        bURL = 'https://www.google.com/recaptcha/'
        bURL += (matches := findall(r'([api2|enterprise]+)\/anchor\?(.*)', aURL)[0])[0]+'/'

        #! Requests Token from Anchor URL
        resp = session.get(f'{bURL}anchor', params=(param := matches[1]), timeout=10)

        #! Convert Params To Dict
        sParams = dict(pair.split('=') for pair in param.split('&'))

        #! Update Data
        payload = f"v={sParams['v']}&reason=q&c={findall(r'value=.(.*?).>', resp.text)[0]}&k={sParams['k']}&co={sParams['co']}"

        #! Get Response Token
        resp = session.post(f'{bURL}reload', params=f'k={sParams["k"]}', data=payload, timeout=10)
        return(findall(r'"rresp","(.*?)"', resp.text)[0])
