from aiogram.utils import executor
from bot_create import dp
import asyncio
from handlers import client, jury, moder, admin, other

async def on_startup(_):
    print('Бот вышел в онлайн')
    asyncio.create_task(other.scheduler())


client.register_handlers_client(dp)
jury.register_handlers_jury(dp)
moder.register_handlers_moder(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
