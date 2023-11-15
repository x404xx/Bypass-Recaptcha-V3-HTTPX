from os import name, system

from httpx import Client
from user_agent import generate_user_agent as gua

from api.recaptchasolver import RecaptchaSolver


def test_v3(anchor_url, proxies=None):
    """
    Create the client instance only once and use the same instance for grabbing the reCAPTCHA token and testing v3.
    """
    base_headers = {'User-Agent': gua()}
    with Client(http2=True, headers=base_headers, proxies=proxies, timeout=10) as client:
        recaptcha_token = RecaptchaSolver.solve_recaptcha(client, anchor_url)
        ant_header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'https://antcpt.com',
            'Referer': 'https://antcpt.com/',
            'X-Requested-With': 'XMLHttpRequest'
        }
        json_data = {'g-recaptcha-reponse': recaptcha_token}
        print(client.post('https://ar1n.xyz/recaptcha3ScoreTest', headers=ant_header, json=json_data).text)


if __name__ == '__main__':
    system('cls' if name == 'nt' else 'clear')
    anchor_url = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LcR_okUAAAAAPYrPe-HK_0RULO1aZM15ENyM-Mf&co=aHR0cHM6Ly9hbnRjcHQuY29tOjQ0Mw..&hl=en&v=Km9gKuG06He-isPsP6saG8cn&size=invisible&cb=a035ydmpd1ys'
    test_v3(anchor_url)
