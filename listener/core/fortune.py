import aiohttp
import asyncio

_BASE_URLS=[
    'http://yerkee.com/api/fortune/',
    'https://helloacm.com/api/fortune/',
    'https://horoscope-free-api.herokuapp.com'
]

class StoryTeller:
    """Asynchronous story teller api client."""

    def __init__(self):
        self.teller = None

class FortuneTeller:
    """Asynchronous fortune teller api client."""

    def __init__(self):
        self.teller = None

    @staticmethod
    def get_api_formatted_url(api='helloacm', category=''):
        if api == 'yerkee':
            url = _BASE_URLS[0] + category
        elif api == 'helloacm':
            url = _BASE_URLS[1]
        else:
            url = _BASE_URLS[2]
        return url

    async def get_fortune(self, api='yerkee', category='all'):
        """Get fortune.
        params:      | valid_values
        api         -> helloacm, yerkee
        category    -> all, computers, cookie, definitions, miscellaneous,
                       people, platitudes, politics, science, and wisdom.

        helloacm api, Retrieve random fortune.
        yerkee api , retrieve random fortune, also categorical fortune.
        """

        async with aiohttp.ClientSession() as session:
            url = self.get_api_formatted_url(api, category)
            response = await session.get(url)
            print(response)
        return await response.json()

    async def get_horoscope(self, time, sign):
        """Get horoscope by time and sunsign.
        horoscope-free-api, for daily horoscope.

        Daily Horoscope GET:/?time=today&sign=<sunsign>
        Eg: GET https://horoscope-free-api.herokuapp.com/?time=today&sign=cancer

        Weekly Horoscope GET:/?time=week&sign=<sunsign>
        Eg: GET https://horoscope-free-api.herokuapp.com/?time=week&sign=cancer

        Monthly Horoscope GET:/?time=month&sign=<sunsign>
        Eg: GET https://horoscope-free-api.herokuapp.com/?time=month&sign=cancer

        Yearly Horoscope GET:/?time=year&sign=<sunsign>
        Eg: GET https://horoscope-free-api.herokuapp.com/?time=year&sign=cancer
        """

        _BASE_URL = _BASE_URLS[2]
        async with aiohttp.ClientSession() as session:
            url = "{}/?time={}&sign={}".format(_BASE_URL, time, sign)
            response = await session.get(url)
        return await response.json()

# TESTS
# async def main(loop):
#     resp = await ft.get_horoscope(time='today', sign='virgo')
#     print(resp)
#     resp = await ft.get_fortune()
#     print(resp)
#
# ft = FortuneTeller()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main(loop))
