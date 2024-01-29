import random
import sqlite3

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup

from classes import *
from const import *

TOKEN = '6040789894:AAH4Fl0-QprVNA8IPSGzn9w8zH1zTNwzrNs'
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


def kbh():
    kbh = ReplyKeyboardMarkup(resize_keyboard=True)
    kbh1 = KeyboardButton('/help')
    kbh.add(kbh1)
    return kbh


def kbg():
    kbg = ReplyKeyboardMarkup(resize_keyboard=True)
    kbg1 = KeyboardButton('СТОП')
    kbg.add(kbg1)
    return kbg


def kba():
    kba = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(1072, 1104, 6):
        ba1 = [KeyboardButton(text=chr(i + j)) for j in range(6) if i + j < 1104]
        kba.add(*ba1)
    ba2 = KeyboardButton('СТОП')
    kba.add(ba2)
    return kba


def kbn():
    kbn = InlineKeyboardMarkup(row_width=len(genre))
    for i in range(0, len(genre), 3):
        bn2 = [InlineKeyboardButton(text=genre[i + j], callback_data=genre[i + j]) for j in range(3) if
               i + j < len(genre)]
        kbn.add(*bn2)
    return kbn


def anime_names(url):
    lst = anime_lst(url)
    ikb = InlineKeyboardMarkup(row_width=1)
    ib = [InlineKeyboardButton(text=nu, callback_data=nu[:10]) for nu in lst]
    ikb.add(*ib)
    return ikb


def watch_anime(name, my_url):
    ikb = InlineKeyboardMarkup(row_width=1)
    ib = InlineKeyboardButton(text=f'Смотреть {name}', url=my_url)
    ikb.add(ib)
    return ikb


def next_new_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton('Следующая новость')
    b2 = KeyboardButton('Предыдущая новость')
    b3 = KeyboardButton('СТОП')
    kb.add(b2, b1)
    kb.add(b3)
    return kb


tries = 6
lst_play = []
newslst = news_lst()


def guess_number():
    random_num = random.randint(1, 100)
    return random_num


def guess_word():
    word = random.choice(words)
    return word


def is_valid(char):
    try:
        num = int(char)
        return num
    except:
        if char.upper() == 'СТОП':
            return char
        return False


class StateText(StatesGroup):
    digit = State()
    admin = State()
    word = State()
    news = State()


def insert_table(mes, guess):
    conn = sqlite3.connect('users_id.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT id FROM users WHERE id = {mes.from_user.id}")
    data = cursor.fetchall()
    if len(data) > 0:
        cursor.execute('UPDATE users SET play = ? WHERE id = ?', (guess, mes.from_user.id))
        conn.commit()
    else:
        cursor.execute('INSERT INTO users VALUES(?, ?, ?)', (mes.from_user.username, mes.from_user.id, guess))
        conn.commit()


def create_table(mes, guess):
    conn = sqlite3.connect('users_id.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(username TEXT, id INTEGER, play TEXT)""")
    conn.commit()
    insert_table(mes, guess)



def lst_redact(us_id):
    for i in lst_play:
        if i.us_id == str(us_id):
            lst_play.remove(i)
            return


def get_guess_num_by_id(id):
    return int(get_guess_word_by_id(id))


def get_guess_word_by_id(id):
    conn = sqlite3.connect('users_id.db')
    cursor = conn.cursor()
    cursor.execute("SELECT play FROM users WHERE id = ?", (id,))
    data = cursor.fetchall()
    return str(data[0][0])


def get_user_by_id(id):
    for i in lst_play:
        if i.us_id == str(id):
            return i


@dp.message_handler(commands=['help'])
async def help_command(mes: types.Message):
    with open('Commands', 'r', encoding='utf-8') as f:
        await mes.answer(f.read())


@dp.message_handler(commands=['start'])
async def get_start(mes: types.Message):
    await mes.answer(
        f'<b>Привет, {mes.from_user.first_name}, я бот, с которым можно поиграть в разные игры, а еще я могу порекомендовать тебе аниме и даже могк показать новости из моего родного города! :)</b>',
        parse_mode='html')


@dp.message_handler(commands=['admin'])
async def admin_command(mes: types.Message):
    await mes.answer('Введите код доступа')
    await StateText.admin.set()


@dp.message_handler(content_types=['text'], state=StateText.admin)
async def get_password(mes: types.Message, state: FSMContext):
    conn = sqlite3.connect('users_id.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    if mes.text == 'qwerty321':
        text = ''
        for user in data:
            text += user[0] + ' | ' + str(user[1]) + ' | ' + str(user[2]) + '\n'
        await mes.answer(text)
    else:
        await mes.answer('Доступ запрещён')
    await state.finish()


@dp.message_handler(commands=['digits'])
async def get_random_digit(mes: types.Message):
    guess = guess_number()
    create_table(mes, guess)
    print(guess)

    await StateText.digit.set()
    await mes.reply('<b>Погнали!</b>', parse_mode='html')
    await mes.answer(
        'Я загадал число в диапозоне от 1 до 100, твои предположения? Чтобы прекратить играть, напишите "СТОП"',
        reply_markup=kbg())


@dp.message_handler(content_types=['text'], state=StateText.digit)
async def get_user_digit(mes: types.Message, state: FSMContext):
    guess = get_guess_num_by_id(mes.from_user.id)
    num = is_valid(mes.text)
    if str(num).upper() == 'СТОП':
        await mes.answer('Я остановил игру!😉', reply_markup=ReplyKeyboardRemove())
        await state.finish()
    elif not num:
        await mes.answer('А может быть все-таки введем целое число от 1 до 100?')
        return
    elif num != guess:
        if num < guess:
            await mes.answer('Ваше число меньше загаданного, попробуйте еще разок')
        elif num > guess:
            await mes.answer('Ваше число больше загаданного, попробуйте еще разок')
    else:
        await mes.reply('Вы угадали, поздравляем!', reply_markup=kbh())
        await state.finish()


@dp.message_handler(commands=['words'])
async def commands_words(mes: types.Message):
    word = guess_word()
    create_table(mes, word)
    print(word)
    gameplay = PlayWords(word, tries, mes.from_user.id)
    lst_redact(mes.from_user.id)
    lst_play.append(gameplay)

    await StateText.word.set()
    await mes.reply('<b>Погнали!</b>', parse_mode='html')
    await mes.answer(
        'Я загадал слово, как думаешь, какая буква? Чтобы прекратить играть, напишите "СТОП"')
    await bot.send_photo(chat_id=mes.from_user.id, photo=display_hangman(gameplay.tries, gameplay.word))
    await mes.answer(' '.join(gameplay.field), reply_markup=kba())


@dp.message_handler(content_types=['text'], state=StateText.word)
async def get_user_alpha(mes: types.Message, state: FSMContext):
    gameplay = get_user_by_id(mes.from_user.id)
    guess = get_guess_word_by_id(mes.from_user.id)
    letter = mes.text
    if str(letter).upper() == 'СТОП':
        await mes.answer('Я остановил игру!😉', reply_markup=kbh())
        await state.finish()
    elif str(letter).lower() == guess:
        await mes.answer(f'Вы выйграли, загаданное слово {guess.upper()}🧟', reply_markup=kbh())
        await state.finish()
    elif letter in gameplay.errors:
        await mes.answer('Вы уже вводили эту букву')
    elif letter in guess:
        await bot.send_photo(chat_id=mes.from_user.id, photo=display_hangman(gameplay.tries, guess))
        await mes.answer(gameplay.update_field(letter))
    else:
        await bot.send_photo(chat_id=mes.from_user.id, photo=display_hangman(gameplay.count_tries(), guess))
        await mes.answer(gameplay.update_field(letter))

    if gameplay.tries == 0:
        await mes.answer(f'Вы проиграли! Загаданное слово {guess.upper()}😈', reply_markup=kbh())
        await state.finish()
    if ''.join(gameplay.field) == guess:
        await mes.answer(f'Вы выйграли, загаданное слово {guess.upper()}🧟', reply_markup=kbh())
        await state.finish()


@dp.message_handler(commands=['anime'])
async def commands_anime(mes: types.Message):
    await mes.answer('Я могу посоветовать тебе разные аниме!', reply_markup=kbn())


@dp.callback_query_handler(lambda callback_query: callback_query.data in genre)
async def vote_callback(callback: types.CallbackQuery):
    if callback.data in genre:
        await callback.message.answer_photo(
            photo='https://gas-kvas.com/uploads/posts/2023-01/1673404494_gas-kvas-com-p-anime-risunki-iz-raznikh-anime-8.jpg',
            caption=f'Аниме в жанре {callback.data}:',
            reply_markup=anime_names(genres[callback.data]))


@dp.callback_query_handler(lambda callback_query: callback_query.data in urls)
async def callback_anime_names(callback: types.CallbackQuery):
    anime_info = get_anime_info(urls[callback.data])
    await callback.message.answer_photo(photo=anime_info[1],
                                        caption=f'<b>{anime_info[0]}</b>', parse_mode='html')
    await callback.message.answer(f'{anime_info[2].strip()}\n\n<b>Рейтинг: {anime_info[3]}</b>', parse_mode='html',
                                  reply_markup=watch_anime(anime_info[0], anime_info[-1]))


@dp.message_handler(commands=['news'])
async def commands_news(mes: types.Message):
    number = 0
    await mes.answer('Я запускаю НОВОСТИ, чтобы остановить нажмите "СТОП"')
    await mes.answer(news_lst()[number], reply_markup=next_new_kb())
    create_table(mes, number)
    await StateText.news.set()


@dp.message_handler(content_types=['text'], state=StateText.news)
async def get_next_by_news(mes: types.Message, state: FSMContext):
    number = get_guess_num_by_id(mes.from_user.id)
    if mes.text == 'СТОП':
        await mes.answer('Я остановил новости!', reply_markup=kbh())
        await state.finish()
    elif mes.text.capitalize() == 'Следующая новость':
        number += 1
        number = (number, number - len(newslst))[number >= len(newslst)]
        await mes.answer(newslst[number])
        print(number)
        insert_table(mes, number)
    elif mes.text.capitalize() == 'Предыдущая новость':
        number -= 1
        number = (number, len(newslst) - 1)[number < 0]
        print(number)
        await mes.answer(newslst[number])
        insert_table(mes, number)
    else:
        await mes.answer('Введи какую новость ты хочешь увидеть :)')


@dp.message_handler()
async def get_random_mes(mes: types.Message):
    await mes.answer('Прости, я тебя не понимяу :(', reply_markup=kbh())


if __name__ == '__main__':
    executor.start_polling(dp)