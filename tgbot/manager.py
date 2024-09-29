import nest_asyncio
import os

from telethon import TelegramClient

nest_asyncio.apply()

API_ID = os.environ['API_ID']

API_HASH = os.environ['API_HASH']


async def send_manager_message(user, text):
    async with TelegramClient('anon', API_ID, API_HASH) as client:
        await client.get_dialogs()
        try:
            from_ = await client.get_entity(user.username)
        except ValueError:
            pass
        try:
            from_ = await client.get_entity(user.id)
        except ValueError:
            pass
        if from_ is None:
            raise ValueError("I could not find the user")
        await client.loop.run_until_complete(await client.send_message(
            user.id,
            text
        ))
