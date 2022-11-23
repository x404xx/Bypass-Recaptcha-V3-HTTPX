from os import system
from httpx import Client
from grecap import googRecap
from user_agent import generate_user_agent as gua
system('cls')


def testV3(proxy:str, aURL:str):
    with Client(http2=True, proxies=proxy) as session:

        session.headers.update({
            'User-Agent': gua(),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'https://antcpt.com',
            'Referer': 'https://antcpt.com/',
            'X-Requested-With': 'XMLHttpRequest'
        })

        json_data = {
            'g-recaptcha-reponse': googRecap(proxy, aURL),
        }

        print(f"{(resp:=session.post('https://ar1n.xyz/recaptcha3ScoreTest', json=json_data, timeout=10).text)}\n")
        return resp

if __name__ == '__main__':
    testV3(None, 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LcR_okUAAAAAPYrPe-HK_0RULO1aZM15ENyM-Mf&co=aHR0cHM6Ly9hbnRjcHQuY29tOjQ0Mw..&hl=en&v=Km9gKuG06He-isPsP6saG8cn&size=invisible&cb=a035ydmpd1ys')
