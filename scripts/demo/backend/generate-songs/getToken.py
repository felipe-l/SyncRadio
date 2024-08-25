import requests

def refreshToken():
    cookies = {
        '__client': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImNsaWVudF8ya0lHY2NsM1lTWFFmZVlvZVcyN2tiUHM2QW4iLCJyb3RhdGluZ190b2tlbiI6InJuOXE4Y2lneGhyZGc3MXprNXpoNHozNGswNHQ0a2JlZnA3bG5wZmUifQ.Gtu9Eh8_JKdTbIRyZJJbJCodqqrqaDTwHXROoj-Sksze9wsYyvOmtEq-BeL2RWoDqrRaiR2QFk9KH6UaMc5JnQwBn2jk3wHtrC7M-zzuLRrxRU_8BAt6-XUIdFm8fZ33iYAekfQ6h73kYYnuTCtBet5Jbzmdu13vPu1j0hFPuGlSrF3DC8ABitwfWsDojSKjiix3vPOVOlHfXMq4RnDHWqjWlMSTz8FSxNOF5cep3OGknz0Y2igfXZpZGAHZVUprsXUJeCvw2Y71HOXVqLKoAyaEDjE5ygPs8wp-S8CeOQ1dAV0OGEKZ4jPLQoeZWxry1mE2PR8HEIC_Axct6YwbBA',
        '__client_uat': '1722963761',
        'ajs_anonymous_id': '53a75842-2125-49a1-88e7-2412d83d17f9',
        '__stripe_mid': 'c29ef96e-dc98-4b9e-ae6b-4dacb335c727d72524',
        '_cfuvid': 'H2V.rDgxe.JTRcJB5bTZHs67DtdQpWqNOnfVCb_F6qs-1724387233178-0.0.1.1-604800000',
        'mp_26ced217328f4737497bd6ba6641ca1c_mixpanel': '%7B%22distinct_id%22%3A%20%223d91f4d9-8b96-4f4c-8f60-4a069ddebb56%22%2C%22%24device_id%22%3A%20%221917b649f00505-0c204963380c66-26001e51-219b08-1917b649f00505%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24user_id%22%3A%20%223d91f4d9-8b96-4f4c-8f60-4a069ddebb56%22%7D',
        '__cf_bm': 'D_nFP1a_BQXb6dW2Qy8v0Je.YKjfrZ_i.66ps2SJwuQ-1724453425-1.0.1.1-DMvTH.tvGy1OfPKUloOwi6cgeJ5RPdp_RwHLvUgQD_Vb339jvHIpxJEc0vrEkV0jGO8SmQNEHTsUbyvH546DGQ',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.5',
        # 'content-length': '0',
        'content-type': 'application/x-www-form-urlencoded',
        # 'cookie': '__client=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImNsaWVudF8ya0lHY2NsM1lTWFFmZVlvZVcyN2tiUHM2QW4iLCJyb3RhdGluZ190b2tlbiI6InJuOXE4Y2lneGhyZGc3MXprNXpoNHozNGswNHQ0a2JlZnA3bG5wZmUifQ.Gtu9Eh8_JKdTbIRyZJJbJCodqqrqaDTwHXROoj-Sksze9wsYyvOmtEq-BeL2RWoDqrRaiR2QFk9KH6UaMc5JnQwBn2jk3wHtrC7M-zzuLRrxRU_8BAt6-XUIdFm8fZ33iYAekfQ6h73kYYnuTCtBet5Jbzmdu13vPu1j0hFPuGlSrF3DC8ABitwfWsDojSKjiix3vPOVOlHfXMq4RnDHWqjWlMSTz8FSxNOF5cep3OGknz0Y2igfXZpZGAHZVUprsXUJeCvw2Y71HOXVqLKoAyaEDjE5ygPs8wp-S8CeOQ1dAV0OGEKZ4jPLQoeZWxry1mE2PR8HEIC_Axct6YwbBA; __client_uat=1722963761; ajs_anonymous_id=53a75842-2125-49a1-88e7-2412d83d17f9; __stripe_mid=c29ef96e-dc98-4b9e-ae6b-4dacb335c727d72524; _cfuvid=H2V.rDgxe.JTRcJB5bTZHs67DtdQpWqNOnfVCb_F6qs-1724387233178-0.0.1.1-604800000; mp_26ced217328f4737497bd6ba6641ca1c_mixpanel=%7B%22distinct_id%22%3A%20%223d91f4d9-8b96-4f4c-8f60-4a069ddebb56%22%2C%22%24device_id%22%3A%20%221917b649f00505-0c204963380c66-26001e51-219b08-1917b649f00505%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24user_id%22%3A%20%223d91f4d9-8b96-4f4c-8f60-4a069ddebb56%22%7D; __cf_bm=D_nFP1a_BQXb6dW2Qy8v0Je.YKjfrZ_i.66ps2SJwuQ-1724453425-1.0.1.1-DMvTH.tvGy1OfPKUloOwi6cgeJ5RPdp_RwHLvUgQD_Vb339jvHIpxJEc0vrEkV0jGO8SmQNEHTsUbyvH546DGQ',
        'origin': 'https://suno.com',
        'priority': 'u=1, i',
        'referer': 'https://suno.com/',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    params = {
        '_clerk_js_version': '5.15.0',
    }

    response = requests.post(
        'https://clerk.suno.com/v1/client/sessions/sess_2kIGd7LNSYoT15Pg7I0y3rNMxqj/tokens',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(response.content)
    response_json = response.json()
    return response_json['jwt']