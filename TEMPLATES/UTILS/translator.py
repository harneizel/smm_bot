import aiohttp

class Translator:
    def __init__(self):
        self.base_url = "https://translate.googleapis.com/translate_a/single"

    async def translate(self, text, source_lang="ru", target_lang="en"):
        params = {
            "client": "gtx",
            "sl": source_lang,
            "tl": target_lang,
            "dt": "t",
            "q": text
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                data = await response.json()
                translated_text = data[0][0][0] if data and data[0] else None
                return translated_text
