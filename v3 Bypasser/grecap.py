import re
from httpx import Client
from user_agent import generate_user_agent as gua


def googRecap(proxy:str, aURL:str):
    with Client(http2=True, proxies=proxy) as session:

        #! Set Headers
        session.headers.update({'User-Agent': gua(), 'content-type': 'application/x-www-form-urlencoded'})

        #! Rebuild URL
        bURL = 'https://www.google.com/recaptcha/'
        bURL += (matches := re.findall(r'([api2|enterprise]+)\/anchor\?(.*)', aURL)[0])[0]

        #! Requests Token from Anchor URL
        resp = session.get(f'{bURL}/anchor',headers=headers, params=(param := matches[1]), timeout=10)

        #! Convert Params To Dict
        sParams = dict(pair.split('=') for pair in param.split('&'))

        #! Update Data
        payload = f"v={sParams['v']}&reason=q&c={re.search(r'value=.(.*?).>', resp.text)[1]}&k={sParams['k']}&co={sParams['co']}"

        #! Get Response Token
        resp = session.post(f'{bURL}/reload',headers=headers, params=f'k={sParams["k"]}', data=payload, timeout=10)
        return(re.search(r'"rresp","(.*?)"', resp.text)[1])
