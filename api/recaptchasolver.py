from re import search


class RecaptchaSolver:
    @staticmethod
    def _convert_params_to_dict(params):
        return dict(pair.split('=') for pair in params.split('&'))

    @staticmethod
    def _build_payload(s_params, c_value):
        return f"v={s_params['v']}&reason=q&c={c_value}&k={s_params['k']}&co={s_params['co']}"

    @staticmethod
    def _get_api_type(anchor_url):
        return (
            matches := search(
                r'(api2|enterprise)/anchor\?(.*)',
                anchor_url
            )
        ) and matches.groups() or (None, None)

    @staticmethod
    def _get_c_value(anchor_token):
        return (
            matches := search(
                r'value="(.*?)"',
                anchor_token)
        ) and matches.group(1) or None

    @staticmethod
    def _get_anchor_token(client, base_url, api_type, headers, params):
        return client.get(
            f'{base_url}/{api_type}/anchor',
            headers = headers,
            params = params
        ).text

    @staticmethod
    def _get_recaptcha_token(client, base_url, api_type, headers, s_params, payload):
        return (
            matches := search(
                r'"rresp","(.*?)"',
                client.post(
                    f'{base_url}/{api_type}/reload',
                    headers = headers,
                    params = f"k={s_params['k']}",
                    data = payload
                ).text
            )
        ) and matches.group(1) or None

    @classmethod
    def solve_recaptcha(cls, client, anchor_url):
        base_url = 'https://www.google.com/recaptcha'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        api_type, params = cls._get_api_type(anchor_url)
        if not api_type and not params:
            raise ValueError('Invalid anchor URL!')
        anchor_token = cls._get_anchor_token(client, base_url, api_type, headers, params)
        c_value = cls._get_c_value(anchor_token)
        if not c_value:
            raise ValueError('Failed to get a c_value!')
        s_params = cls._convert_params_to_dict(params)
        payload = cls._build_payload(s_params, c_value)
        recaptcha_token = cls._get_recaptcha_token(client, base_url, api_type, headers, s_params, payload)
        if not recaptcha_token:
            raise ValueError('Failed to get a recaptcha_token!')
        return recaptcha_token
