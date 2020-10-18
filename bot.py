from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram import types
import asyncio
import schedule
import time
import threading
from threading import Timer

from sqlighter import SQLighter

from ani_mag import Parser_class
import config

loop = asyncio.get_event_loop()
bot = Bot(TOKEN, parse_mode='HTML')

dp = Dispatcher(bot, loop=loop)

db = SQLighter('db.db')

parser = Parser_class('https://www.animag.ru/news')

# ссылка на стикеры
stik_baka = 'https://chpic.su/_data/stickers/a/AnimuReaction2/AnimuReaction2_057.webp'
stik_perf = 'https://chpic.su/_data/stickers/a/animegrid10/animegrid10_002.webp'
stik_hi = 'https://chpic.su/_data/stickers/m/menherachanstickers/menherachanstickers_012.webp'
stik_heh = 'https://chpic.su/_data/stickers/a/AnimeNonNonBiyoriEn/AnimeNonNonBiyoriEn_005.webp'


# отправляю себе инфу о том,что бот запущен
async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text='Бот запущен!')


#команда старт
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	await message.answer('Привет!\nЯ буду уведомлять тебя о всех новостях!Не забудь подписаться на рассылку(команда /subscribe),чтобы получать новости!\nДобро пожаловать в мир аниме :3')
	await message.answer_sticker(stik_hi)

#команда help, о боте
@dp.message_handler(commands=['help'])
async def help(message: types.Message):
	await message.answer('Немного о боте: Бота зовут news-chan, у нее есть имя :3 \nОна будет отправлять последние новости из мира аниме!Это пока все,что она может.')
	await message.answer_sticker(stik_heh)


# Команда активации подписки
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его
		db.add_subscriber(message.from_user.id)
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, True)
	await message.answer("Ты успешно подписался на рассылку!\nПодожди немного, скоро выйдут новые новости и ты узнаешь о них первым!")
	await message.answer_sticker(stik_perf)

# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
	if(not db.subscriber_exists(message.from_user.id)):
		# если юзера нет в базе, добавляем его с неактивной подпиской (запоминаем)
		db.add_subscriber(message.from_user.id, False)
		await message.answer("Ты итак не подписан.")
	else:
		# если он уже есть, то просто обновляем ему статус подписки
		db.update_subscription(message.from_user.id, False)
		await message.answer("Ты отписался от рассылки!")
		await message.answer_sticker(stik_baka)

# команда,для показа предыдущего поста
@dp.message_handler(commands=['previous'])
async def previous(message: types.Message):
	await message.answer('Кнопка временно не доступна! :3')


# проверяем наличие новых постов и делаем рассылки
async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)
		parser.run()
		
		nfo = parser.results[0]
		r = nfo['title'] + '\n\n' + nfo['desc'] + '\n' + 'Источник изображения: ' + nfo['image'] + '\n\n' + 'Ссылка на пост: ' + nfo['link']

		subscriptions = db.get_subscriptions()
			
		if parser.current_post[0] != parser.last_post:				
			for s in subscriptions:
				await bot.send_message(
				s[1],
				text = r
				)
				

# запускаем лонг поллинг
if __name__ == '__main__':
	dp.loop.create_task(scheduled(5))
	executor.start_polling(dp, on_startup=send_to_admin)
