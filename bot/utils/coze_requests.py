import requests
import json
import asyncio
import aiohttp

from bot.utils.config import COZE_URL as url, COZE_TOKEN as token, COZE_BOT_ID as coze_id

#coze взаимодействия
# все делается асинхронно чтобы не втыкали
async def coze_request(tg_id, query, history):
    async with aiohttp.ClientSession() as session:
        headers = {'Authorization': f"Bearer {token}",
                   'Content-Type': 'application/json',
                   'Accept': '*/*',
                   'Host':'api.coze.com',
                   'Connection':'keep-alive'}
        data = {'conversation_id':'123',
                'bot_id': str(coze_id),
                'user': str(tg_id),
                'query': query,
                'stream': False,
                'chat_history': history}
        async with await session.post(url=url, headers=headers, data=json.dumps(data)) as response:
            if response.status == 200:
                data = (json.loads(await response.text()))["messages"]

                print(f"ответ нейронки {data}")
                print(type(data))
                return data

            #response = (json.loads(await response.text())["messages"]
            #print(f"messages {response}")
            #print(type(response))
            #return response

