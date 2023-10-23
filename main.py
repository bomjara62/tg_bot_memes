import os
import re
import traceback
from transformers import AutoTokenizer, AutoModelWithLMHead
import telebot
from telebot import types
from PIL import Image, ImageDraw, ImageFont
import sqlite3
from text_class import text_analyse
from sqlite3 import Error
import random
import torch

device = "cuda:0" if torch.cuda.is_available() else "cpu"

bot_token = '6305312601:AAFQsXmD9BixL8rBmE4GfP5KaQJRkYnT_y8'
bot = telebot.TeleBot(bot_token)


with open("admins.txt", 'r', encoding='utf-8') as f:
    admins = f.read().splitlines()
    f.close()

tokenizer = AutoTokenizer.from_pretrained('tinkoff-ai/ruDialoGPT-medium')
model = AutoModelWithLMHead.from_pretrained('tinkoff-ai/ruDialoGPT-medium')

admin_send = False


def create_connection(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r'meme.db'
    sql_create_table_user = 'CREATE TABLE IF NOT EXISTS user(telegram_id text NOT NULL, first_name text NOT NULL, number_sticker_set integer NULL, count_sticker integer NULL, count_sticker_in_stickerpac integer NULL, settt integer NULL);'
    sql_create_table_channels = 'CREATE TABLE IF NOT EXISTS channels(name text NOT NULL, channel_id text NOT NULL, url_channel NOT NULL);'
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_table_user)
        create_table(conn, sql_create_table_channels)
    else:
        print("Error! cannot create the database connection.")


main()


def insert_user(dannye):
    database = r'meme.db'
    conn = create_connection(database)
    sql = 'INSERT INTO user (telegram_id, first_name, number_sticker_set, count_sticker, count_sticker_in_stickerpac, settt) VALUES (?, ?, ?, ?, ?, ?)'
    cur = conn.cursor()
    cur.execute(sql, dannye)
    conn.commit()


def select_number_sticker_set(dannye):
    database = r'meme.db'
    conn = create_connection(database)
    sql = 'SELECT number_sticker_set FROM user WHERE telegram_id = ?;'
    cur = conn.cursor()
    cur.execute(sql, dannye)
    number = cur.fetchall()
    return number


def update_number_sticker_set(dannye):
    database = r'meme.db'
    conn = create_connection(database)
    sql = 'UPDATE user SET number_sticker_set = ? WHERE telegram_id = ?'
    cur = conn.cursor()
    cur.execute(sql, dannye)
    conn.commit()


def select_count_sticker_in_stickerpac(dannye):
    database = r'meme.db'
    conn = create_connection(database)
    sql = 'SELECT count_sticker_in_stickerpac FROM user WHERE telegram_id = ?;'
    cur = conn.cursor()
    cur.execute(sql, dannye)
    number = cur.fetchall()
    return number


def update_count_sticker_in_stickerpac(dannye):
    database = r'meme.db'
    conn = create_connection(database)
    sql = 'UPDATE user SET count_sticker_in_stickerpac = ? WHERE telegram_id = ?'
    cur = conn.cursor()
    cur.execute(sql, dannye)
    conn.commit()


def select_count_sticker(dannye):
    database = r'meme.db'
    conn = create_connection(database)
    sql = 'SELECT count_sticker FROM user WHERE telegram_id = ?;'
    cur = conn.cursor()
    cur.execute(sql, dannye)
    number = cur.fetchall()
    return number


def select_set(dannye):
    database = r'meme.db'
    conn = create_connection(database)
    sql = 'SELECT settt FROM user WHERE telegram_id = ?;'
    cur = conn.cursor()
    cur.execute(sql, dannye)
    number = cur.fetchall()
    return number


def update_set(dannye):
    database = r'meme.db'
    conn = create_connection(database)
    sql = 'UPDATE user SET settt = ? WHERE telegram_id = ?'
    cur = conn.cursor()
    cur.execute(sql, dannye)
    conn.commit()


def update_count_sticker(dannye):
    database = r'meme.db'
    conn = create_connection(database)
    sql = 'UPDATE user SET count_sticker = ? WHERE telegram_id = ?'
    cur = conn.cursor()
    cur.execute(sql, dannye)
    conn.commit()


def select_all():
    database = r'meme.db'
    conn = create_connection(database)
    sql = 'SELECT * FROM user ORDER BY count_sticker DESC;'
    cur = conn.cursor()
    cur.execute(sql)
    number = cur.fetchall()
    return number


def insert_channel(dannye):
    database = r'meme.db'
    conn = create_connection(database)
    sql = 'INSERT INTO channels (name, channel_id, url_channel) VALUES (?, ?, ?)'
    cur = conn.cursor()
    cur.execute(sql, dannye)
    conn.commit()


def select_channels():
    database = r'meme.db'
    conn = create_connection(database)
    sql = 'SELECT * FROM channels;'
    cur = conn.cursor()
    cur.execute(sql)
    number = cur.fetchall()
    return number


def delete_channel(dannye):
    database = r'meme.db'
    conn = create_connection(database)
    sql = 'DELETE FROM channels WHERE name = ?'
    cur = conn.cursor()
    cur.execute(sql, dannye)
    conn.commit()


def select_user(dannye):
    database = r'meme.db'
    conn = create_connection(database)
    sql = 'SELECT * FROM user WHERE telegram_id = ?;'
    cur = conn.cursor()
    cur.execute(sql, dannye)
    number = cur.fetchall()
    return number


# channels = [
#    ["testttttttt1", '-1001929669909', 'https://t.me/testtttttttttttttttttttttttta']
# ]
'''
def check_sub_channel(channels, user_id):
    for channel in channels:
        check = bot.get_chat_member(channel[1], user_id)
    return check
'''
num = '0'

ran = ''


@bot.message_handler(content_types=["new_chat_members"])
def new_member(message):
    for member in message.new_chat_members:
        if member.username == 'tester_64_bot':
            try:
                database = r'meme.db'
                conn = create_connection(database)
                cur = conn.cursor()
                cur.execute(f"INSERT INTO chats(chat_id) VALUES('{message.chat.id}')")
                conn.commit()
            except:
                print(traceback.format_exc())



@bot.message_handler(content_types=['text'])
def handle_text(message):
    global ran, num, admin_send
    # value = ((message.from_user.id),)
    # num = select_set(value)
    # num = num[0][0]
    fl = False
    all_users = select_all()
    for i in range(len(all_users)):
        if str(all_users[i][0]) == str(message.from_user.id):
            fl = True
    channels = select_channels()
    fl_chan = True
    for i in range(len(channels)):
        check = bot.get_chat_member(channels[i][1].split()[0], message.from_user.id)
        if check.status == 'left':
            fl_chan = False
            break
    if message.text == '/start' or not (fl) or not (fl_chan):
        if not (fl):
            values = (str(message.from_user.id), str(message.from_user.first_name), 0, 0, 0, 0)
            insert_user(values)
        keyboard1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('#️⃣Начать использовать', callback_data='start')
        keyboard1.add(btn1)
        bot.send_message(message.chat.id,
                         text=f'👋🏻 Воу, {message.from_user.first_name}\nпривет :)\n\nЯ бот создающий мемные\nцитаты, и делаю я их из\nразных мемов.',
                         reply_markup=keyboard1)
    elif message.text == '/add_cannels':
        bot.send_message(message.chat.id,
                         text=f'Для того, чтобы добавить канал в список каналов на которые нужно подписаться введите через запятую его название, телеграм айди канала и ссылку на него\n\nПример:\nchannel_name, -123123123123, https://t.me/test')
        bot.register_next_step_handler(message, add_channel)
    elif message.text == '/delete_channel':
        all_channels = select_channels()
        txt = f''
        for i in range(len(all_channels)):
            txt = txt + f'{all_channels[i][0]}, {all_channels[i][1]}, {all_channels[i][2]}\n'
        bot.send_message(message.chat.id, text=f'Для того чтобы удалить канал введите его название')
        bot.send_message(message.chat.id, text=f'{txt}')
        bot.register_next_step_handler(message, del_chan)
    elif message.text == '/profile':
        keyb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('🛠Стикеры', callback_data='sticker')
        keyb.add(btn1)
        dannye = (message.from_user.id,)
        user = select_user(dannye)[0]
        count_mems = select_count_sticker(dannye)
        count_mems = count_mems[0][0]
        bot.send_message(message.chat.id,
                         text=f'{user[1]} твой профиль🙊\n\n– создано: {count_mems} цитат\n\n⬇️ Ещё можно редактировать\nсвои стикерпаки',
                         reply_markup=keyb)
    elif message.text == '/top':
        users = select_all()
        txt = ''
        for i in range(len(users)):
            txt = txt + f'{i + 1}. {users[i][1]}' + ' ' + f'{users[i][3]}\n'
        bot.send_message(message.chat.id, text=f'Топ мемоцитов:\n\n{txt}')
    elif '/create' in message.text:

        number = message.text.split()[1]
        txt = ' '
        if str(number).isdigit():
            all_files = os.listdir(os.getcwd() + '/all')

            if 0 < int(number) < len(all_files):
                img2 = Image.open(f'{number}.png')
            else:
                bot.send_message(message.chat.id, 'Введите число в промежутке между 1 и 72')
                return
            if len(message.text.split()) > 2:
                txt = message.text.split(' ', 2)[2]

            elif message.reply_to_message:
                txt = message.reply_to_message.text

            img1 = Image.new('RGB', (512, 512), (255, 255, 255))
            img3 = Image.open('cloudd.png')
            res = img2.resize((350, 400))
            res.save(f'{number}.png')
            img2 = Image.open(f'{number}.png')
            img1.putalpha(0)
            res = img3.resize((200, 100))
            res.save('cloudd.png')
            img3 = Image.open('cloudd.png')
            draw = ImageDraw.Draw(img3)
            font = ImageFont.truetype("ofont.ru_Zametka Parletter.ttf", 20)
            if len(txt) > 14:
                txt = txt[:11] + '...'
            draw.text((10, 30), f'{txt}', fill='black', font=font)
            img1.paste(img2, (0, 100), mask=img2.convert('RGBA'))
            img1.paste(img3, (300, 80), mask=img3.convert('RGBA'))
            # img1.show()
            img1.save('draw-ellipse-rectangle-line.png')

            mes = bot.send_document(-4067580571, document=open('draw-ellipse-rectangle-line.png', 'rb'))
            fid = f'{mes.document.file_id}'

            value = ((message.from_user.id),)
            number_stickerpac = select_number_sticker_set(value)
            count_in_pack = select_count_sticker_in_stickerpac(value)
            count_mems = select_count_sticker(value)
            number_stickerpac = number_stickerpac[0][0]
            count_in_pack = count_in_pack[0][0]
            count_mems = count_mems[0][0]
            settt = select_set(value)[0][0]
            if number_stickerpac == 0 and count_in_pack == 0:
                # hood1000richbot
                # tester_64_bot
                bot.create_new_sticker_set(message.from_user.id,
                                           f'sticker_{str(message.from_user.id)}_{str(settt + 1)}_by_Sticker_AiBot',
                                           f'{message.from_user.first_name}№{number_stickerpac + 1}', [f'🤨'], f"{fid}")
                dannye = (number_stickerpac + 1, message.from_user.id)
                update_number_sticker_set(dannye)
                dannye = (count_in_pack + 1, message.from_user.id)
                update_count_sticker_in_stickerpac(dannye)
                dannye = (count_mems + 1, message.from_user.id)
                update_count_sticker(dannye)
                dannye = (settt + 1, message.from_user.id)
                update_set(dannye)
                sett = bot.get_sticker_set(
                    name=f'sticker_{str(message.from_user.id)}_{str(settt + 1)}_by_Sticker_AiBot')
                keyb = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('👍', callback_data='like:0:0:l')
                btn2 = types.InlineKeyboardButton('👎', callback_data='like:0:0:d')
                keyb.add(btn1, btn2)
                bot.send_sticker(message.chat.id, sticker=sett.stickers[-1].file_id, reply_markup=keyb)
                # bot.send_message(message.chat.id, text=f'Сделано, http://t.me/addstickers/sticker_{str(message.from_user.id)}_{"12412412"}_by_hood1000richbot')
            elif count_in_pack == 120:
                bot.create_new_sticker_set(message.from_user.id,
                                           f'sticker_{str(message.from_user.id)}_{str(settt + 1)}_by_Sticker_AiBot',
                                           f'stickers_{message.from_user.first_name}№{number_stickerpac + 1}', [f'🤨'],
                                           f'{fid}')
                dannye = (number_stickerpac + 1, message.from_user.id)
                update_number_sticker_set(dannye)
                dannye = (1, message.from_user.id)
                update_count_sticker_in_stickerpac(dannye)
                dannye = (count_mems + 1, message.from_user.id)
                update_count_sticker(dannye)
                dannye = (settt + 1, message.from_user.id)
                update_set(dannye)
                sett = bot.get_sticker_set(name=f'sticker_{str(message.from_user.id)}_{str(settt)}_by_Sticker_AiBot')
                keyb = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('👍', callback_data='like:0:0:l')
                btn2 = types.InlineKeyboardButton('👎', callback_data='like:0:0:d')
                keyb.add(btn1, btn2)
                bot.send_sticker(message.chat.id, sticker=sett.stickers[-1].file_id, reply_markup=keyb)
                # bot.send_message(message.chat.id, text=f'Сделано, http://t.me/addstickers/stick_{str(message.from_user.id)}_{str(number_stickerpac)}_by_hood1000richbot')
            else:
                try:
                    # bot.create_new_sticker_set(message.from_user.id, f'sticker_{str(message.from_user.id)}_{str(num+1)}_by_hood1000richbot', f'{message.from_user.first_name}№{number_stickerpac+1}', f'🤨', f'{fid}')

                    bot.add_sticker_to_set(message.from_user.id,
                                           f'sticker_{str(message.from_user.id)}_{str(settt)}_by_Sticker_AiBot', [f'🤨'],
                                           f'{fid}')
                    dannye = (count_in_pack + 1, message.from_user.id)
                    update_count_sticker_in_stickerpac(dannye)
                    dannye = (count_mems + 1, message.from_user.id)
                    update_count_sticker(dannye)
                    sett = bot.get_sticker_set(
                        name=f'sticker_{str(message.from_user.id)}_{str(settt)}_by_Sticker_AiBot')
                    keyb = types.InlineKeyboardMarkup()
                    btn1 = types.InlineKeyboardButton('👍', callback_data='like:0:0:l')
                    btn2 = types.InlineKeyboardButton('👎', callback_data='like:0:0:d')
                    keyb.add(btn1, btn2)
                    bot.send_sticker(message.chat.id, sticker=sett.stickers[-1].file_id, reply_markup=keyb)
                    # bot.send_message(message.chat.id, text=f'Сделано, http://t.me/addstickers/sticker_{str(message.from_user.id)}_{"12412412"}_by_hood1000richbot')
                except:
                    bot.create_new_sticker_set(message.from_user.id,
                                               f'sticker_{str(message.from_user.id)}_{str(settt + 1)}_by_Sticker_AiBot',
                                               f'{message.from_user.first_name}№{number_stickerpac + 1}', [f'🤨'],
                                               f'{fid}')
                    dannye = (number_stickerpac + 1, message.from_user.id)
                    update_number_sticker_set(dannye)
                    dannye = (count_in_pack + 1, message.from_user.id)
                    update_count_sticker_in_stickerpac(dannye)
                    dannye = (count_mems + 1, message.from_user.id)
                    update_count_sticker(dannye)
                    dannye = (settt + 1, message.from_user.id)
                    update_set(dannye)
                    sett = bot.get_sticker_set(
                        name=f'sticker_{str(message.from_user.id)}_{str(settt + 1)}_by_Sticker_AiBot')
                    keyb = types.InlineKeyboardMarkup()
                    btn1 = types.InlineKeyboardButton('👍', callback_data='like:0:0:l')
                    btn2 = types.InlineKeyboardButton('👎', callback_data='like:0:0:d')
                    keyb.add(btn1, btn2)
                    bot.send_sticker(message.chat.id, sticker=sett.stickers[-1].file_id, reply_markup=keyb)
                    # bot.send_message(message.chat.id, text=f'Сделано, http://t.me/addstickers/sticker_{str(message.from_user.id)}_{"12412412"}_by_hood1000richbot')

    elif '/gen' in message.text:
        images = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                  '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35',
                  '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52',
                  '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69',
                  '70', '71']
        txt = ''
        try:
            number = message.text.split()[1]
        except:
            number = 'Хуй'


        try:

            if message.reply_to_message:
                text = message.reply_to_message.text
                inputs = tokenizer(f'@@ПЕРВЫЙ@@{text} @@ВТОРОЙ@@',
                                   return_tensors='pt')
                generated_token_ids = model.generate(
                    **inputs,
                    top_k=10,
                    top_p=0.95,
                    num_beams=3,
                    num_return_sequences=1,
                    do_sample=True,
                    no_repeat_ngram_size=2,
                    temperature=1.0,
                    repetition_penalty=1.2,
                    length_penalty=1.0,
                    eos_token_id=50257,
                    max_time=6,
                    max_length=18
                )

                context_with_response = [tokenizer.decode(sample_token_ids) for sample_token_ids in
                                         generated_token_ids]
                print(context_with_response[0])
                result = context_with_response[0].split('@@ВТОРОЙ@@')[1].replace('@@ПЕРВЫЙ@@', '')

                txt = result
            else:
                txt = message.text.replace('/gen ', '')

            sent_type = text_analyse(txt)[0]['label']
            all_files = os.listdir(os.getcwd() + f'/{sent_type.lower()}')
            numb = random.randint(1, len(all_files))
            img2 = Image.open(f'{sent_type.lower()}/{numb}.png')

            # Создание картинки
            img1 = Image.new('RGB', (512, 512), (255, 255, 255))
            img3 = Image.open('cloudd.png')
            res = img2.resize((350, 400))
            res.save(f'{numb}.png')
            img2 = Image.open(f'{numb}.png')
            img1.putalpha(0)
            res = img3.resize((200, 100))
            res.save('cloudd.png')
            img3 = Image.open('cloudd.png')
            draw = ImageDraw.Draw(img3)
            font = ImageFont.truetype("ofont.ru_Zametka Parletter.ttf", 20)
            if len(txt) > 18:
                txt = txt[:16] + '...'
            draw.text((10, 30), f'{txt}', fill='black', font=font)
            img1.paste(img2, (0, 100), mask=img2.convert('RGBA'))
            img1.paste(img3, (300, 80), mask=img3.convert('RGBA'))
            # img1.show()
            img1.save('draw-ellipse-rectangle-line.png')

            mes = bot.send_document(-4067580571, document=open('draw-ellipse-rectangle-line.png', 'rb'))
            fid = f'{mes.document.file_id}'

            value = ((message.from_user.id),)
            number_stickerpac = select_number_sticker_set(value)
            count_in_pack = select_count_sticker_in_stickerpac(value)
            count_mems = select_count_sticker(value)
            number_stickerpac = number_stickerpac[0][0]
            count_in_pack = count_in_pack[0][0]
            count_mems = count_mems[0][0]
            settt = select_set(value)[0][0]
            if number_stickerpac == 0 and count_in_pack == 0:
                print(1)
                # hood1000richbot
                # tester_64_bot
                bot.create_new_sticker_set(message.from_user.id,
                                           f'sticker_{str(message.from_user.id)}_{str(settt + 1)}_by_Sticker_AiBot',
                                           f'{message.from_user.first_name}№{number_stickerpac + 1}', [f'🤨'], f"{fid}")
                dannye = (number_stickerpac + 1, message.from_user.id)
                update_number_sticker_set(dannye)
                dannye = (count_in_pack + 1, message.from_user.id)
                update_count_sticker_in_stickerpac(dannye)
                dannye = (count_mems + 1, message.from_user.id)
                update_count_sticker(dannye)
                dannye = (settt + 1, message.from_user.id)
                update_set(dannye)
                sett = bot.get_sticker_set(
                    name=f'sticker_{str(message.from_user.id)}_{str(settt + 1)}_by_Sticker_AiBot')
                keyb = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('👍', callback_data='like:0:0:l')
                btn2 = types.InlineKeyboardButton('👎', callback_data='like:0:0:d')
                keyb.add(btn1, btn2)
                bot.send_sticker(message.chat.id, sticker=sett.stickers[-1].file_id, reply_markup=keyb)
                # bot.send_message(message.chat.id, text=f'Сделано, http://t.me/addstickers/sticker_{str(message.from_user.id)}_{"12412412"}_by_hood1000richbot')
            elif count_in_pack == 120:
                print(2)
                bot.create_new_sticker_set(message.from_user.id,
                                           f'sticker_{str(message.from_user.id)}_{str(settt + 1)}_by_Sticker_AiBot',
                                           f'stickers_{message.from_user.first_name}№{number_stickerpac + 1}', [f'🤨'],
                                           f'{fid}')
                dannye = (number_stickerpac + 1, message.from_user.id)
                update_number_sticker_set(dannye)
                dannye = (1, message.from_user.id)
                update_count_sticker_in_stickerpac(dannye)
                dannye = (count_mems + 1, message.from_user.id)
                update_count_sticker(dannye)
                dannye = (settt + 1, message.from_user.id)
                update_set(dannye)
                sett = bot.get_sticker_set(name=f'sticker_{str(message.from_user.id)}_{str(settt)}_by_Sticker_AiBot')
                keyb = types.InlineKeyboardMarkup()
                btn1 = types.InlineKeyboardButton('👍', callback_data='like:0:0:l')
                btn2 = types.InlineKeyboardButton('👎', callback_data='like:0:0:d')
                keyb.add(btn1, btn2)
                bot.send_sticker(message.chat.id, sticker=sett.stickers[-1].file_id, reply_markup=keyb)
                # bot.send_message(message.chat.id, text=f'Сделано, http://t.me/addstickers/stick_{str(message.from_user.id)}_{str(number_stickerpac)}_by_hood1000richbot')
            else:
                print(3, 'ебануться')
                try:
                    # bot.create_new_sticker_set(message.from_user.id, f'sticker_{str(message.from_user.id)}_{str(num+1)}_by_hood1000richbot', f'{message.from_user.first_name}№{number_stickerpac+1}', f'🤨', f'{fid}')

                    bot.add_sticker_to_set(message.from_user.id,
                                           f'sticker_{str(message.from_user.id)}_{str(settt)}_by_Sticker_AiBot', [f'🤨'],
                                           f'{fid}')
                    print('ахуеть')
                    dannye = (count_in_pack + 1, message.from_user.id)
                    update_count_sticker_in_stickerpac(dannye)
                    dannye = (count_mems + 1, message.from_user.id)
                    update_count_sticker(dannye)
                    sett = bot.get_sticker_set(
                        name=f'sticker_{str(message.from_user.id)}_{str(settt)}_by_Sticker_AiBot')
                    keyb = types.InlineKeyboardMarkup()
                    btn1 = types.InlineKeyboardButton('👍', callback_data='like:0:0:l')
                    btn2 = types.InlineKeyboardButton('👎', callback_data='like:0:0:d')
                    keyb.add(btn1, btn2)
                    bot.send_sticker(message.chat.id, sticker=sett.stickers[-1].file_id, reply_markup=keyb)
                    # bot.send_message(message.chat.id, text=f'Сделано, http://t.me/addstickers/sticker_{str(message.from_user.id)}_{"12412412"}_by_hood1000richbot')
                except:
                    print(traceback.format_exc())
                    bot.create_new_sticker_set(message.from_user.id,
                                               f'sticker_{str(message.from_user.id)}_{str(settt + 1)}_by_Sticker_AiBot',
                                               f'{message.from_user.first_name}№{number_stickerpac + 1}', [f'🤨'],
                                               f'{fid}')
                    dannye = (number_stickerpac + 1, message.from_user.id)
                    update_number_sticker_set(dannye)
                    dannye = (count_in_pack + 1, message.from_user.id)
                    update_count_sticker_in_stickerpac(dannye)
                    dannye = (count_mems + 1, message.from_user.id)
                    update_count_sticker(dannye)
                    dannye = (settt + 1, message.from_user.id)
                    update_set(dannye)
                    sett = bot.get_sticker_set(
                        name=f'sticker_{str(message.from_user.id)}_{str(settt + 1)}_by_Sticker_AiBot')
                    keyb = types.InlineKeyboardMarkup()
                    btn1 = types.InlineKeyboardButton('👍', callback_data='like:0:0:l')
                    btn2 = types.InlineKeyboardButton('👎', callback_data='like:0:0:d')
                    keyb.add(btn1, btn2)
                    bot.send_sticker(message.chat.id, sticker=sett.stickers[-1].file_id, reply_markup=keyb)
                    # bot.send_message(message.chat.id, text=f'Сделано, http://t.me/addstickers/sticker_{str(message.from_user.id)}_{"12412412"}_by_hood1000richbot')
        except:
            print(traceback.format_exc())

            bot.send_message(message.chat.id, text="Введите текст")

    elif str(message.from_user.id) in admins and message.text == '/admin':
        keyb = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton('Просмотр статистики чатов', callback_data='chat_statistic')
        btn2 = types.InlineKeyboardButton('Разослать во все чаты сообщение', callback_data='send_messages')
        keyb.add(btn1, btn2)
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=keyb)

    elif str(message.from_user.id) in admins and admin_send:
        admin_send = False
        database = r'meme.db'
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM chats")
        chats = cur.fetchall()
        for chat in chats:
            try:
                bot.send_message(int(chat[1]), message.text)
            except:
                pass
        cur.execute(f"SELECT * FROM user")
        users = cur.fetchall()
        for chat in users:
            try:
                bot.send_message(int(chat[0]), message.text)
            except:
                pass
        conn.close()

    else:
        if '/' in message.text:
            tx = message.text.split()[1:]
            txt = ''
            for i in range(len(tx)):
                txt += tx[i] + ' '
            number = message.text.split()[0].split('/')[1]
            ran = number
            try:
                ran = int(ran)
                if 0 < int(ran) < 72:
                    # Создание картинки
                    img1 = Image.new('RGB', (512, 512), (255, 255, 255))
                    img2 = Image.open(f'{ran}.png')
                    img3 = Image.open('cloudd.png')
                    res = img2.resize((350, 400))
                    res.save(f'{ran}.png')
                    img2 = Image.open(f'{ran}.png')
                    img1.putalpha(0)
                    res = img3.resize((200, 100))
                    res.save('cloudd.png')
                    img3 = Image.open('cloudd.png')
                    draw = ImageDraw.Draw(img3)
                    font = ImageFont.truetype("ofont.ru_Zametka Parletter.ttf", 20)
                    if len(txt) > 11:
                        txt = txt[:11] + '...'
                    draw.text((10, 30), f'{txt}', fill='black', font=font)
                    img1.paste(img2, (0, 100), mask=img2.convert('RGBA'))
                    img1.paste(img3, (300, 80), mask=img3.convert('RGBA'))
                    # img1.show()
                    img1.save('draw-ellipse-rectangle-line.png')

                    mes = bot.send_document(-1001988093066, document=open('draw-ellipse-rectangle-line.png', 'rb'))
                    fid = f'{mes.document.file_id}'

                    value = ((message.from_user.id),)
                    number_stickerpac = select_number_sticker_set(value)
                    count_in_pack = select_count_sticker_in_stickerpac(value)
                    count_mems = select_count_sticker(value)
                    number_stickerpac = number_stickerpac[0][0]
                    count_in_pack = count_in_pack[0][0]
                    count_mems = count_mems[0][0]
                    settt = select_set(value)[0][0]
                    if number_stickerpac == 0 and count_in_pack == 0:
                        bot.create_new_sticker_set(message.from_user.id,
                                                   f'sticker_{str(message.from_user.id)}_{str(settt + 1)}_by_tester_64_bot',
                                                   f'{message.from_user.first_name}№{number_stickerpac + 1}', f'🤨',
                                                   f'{fid}')
                        dannye = (number_stickerpac + 1, message.from_user.id)
                        update_number_sticker_set(dannye)
                        dannye = (count_in_pack + 1, message.from_user.id)
                        update_count_sticker_in_stickerpac(dannye)
                        dannye = (count_mems + 1, message.from_user.id)
                        update_count_sticker(dannye)
                        dannye = (settt + 1, message.from_user.id)
                        update_set(dannye)
                        sett = bot.get_sticker_set(
                            name=f'sticker_{str(message.from_user.id)}_{str(settt + 1)}_by_tester_64_bot')
                        keyb = types.InlineKeyboardMarkup()
                        btn1 = types.InlineKeyboardButton('👍', callback_data='like:0:0:l')
                        btn2 = types.InlineKeyboardButton('👎', callback_data='like:0:0:d')
                        keyb.add(btn1, btn2)
                        bot.send_sticker(message.chat.id, sticker=sett.stickers[-1].file_id, reply_markup=keyb)
                        # bot.send_message(message.chat.id, text=f'Сделано, http://t.me/addstickers/sticker_{str(message.from_user.id)}_{"12412412"}_by_hood1000richbot')
                    elif count_in_pack == 120:
                        bot.create_new_sticker_set(message.from_user.id,
                                                   f'sticker_{str(message.from_user.id)}_{str(settt + 1)}_by_hood1000richbot',
                                                   f'stickers_{message.from_user.first_name}№{number_stickerpac + 1}',
                                                   f'🤨',
                                                   f'{fid}')
                        dannye = (number_stickerpac + 1, message.from_user.id)
                        update_number_sticker_set(dannye)
                        dannye = (1, message.from_user.id)
                        update_count_sticker_in_stickerpac(dannye)
                        dannye = (count_mems + 1, message.from_user.id)
                        update_count_sticker(dannye)
                        dannye = (settt + 1, message.from_user.id)
                        update_set(dannye)
                        sett = bot.get_sticker_set(
                            name=f'sticker_{str(message.from_user.id)}_{str(settt)}_by_tester_64_bot')
                        keyb = types.InlineKeyboardMarkup()
                        btn1 = types.InlineKeyboardButton('👍', callback_data='like:0:0:l')
                        btn2 = types.InlineKeyboardButton('👎', callback_data='like:0:0:d')
                        keyb.add(btn1, btn2)
                        bot.send_sticker(message.chat.id, sticker=sett.stickers[-1].file_id, reply_markup=keyb)
                        # bot.send_message(message.chat.id, text=f'Сделано, http://t.me/addstickers/stick_{str(message.from_user.id)}_{str(number_stickerpac)}_by_hood1000richbot')
                    else:
                        # bot.create_new_sticker_set(message.from_user.id, f'sticker_{str(message.from_user.id)}_{str(num+1)}_by_hood1000richbot', f'{message.from_user.first_name}№{number_stickerpac+1}', f'🤨', f'{fid}')
                        bot.add_sticker_to_set(message.from_user.id,
                                               f'sticker_{str(message.from_user.id)}_{str(settt)}_by_tester_64_bot',
                                               f'🤨',
                                               f'{fid}')
                        dannye = (count_in_pack + 1, message.from_user.id)
                        update_count_sticker_in_stickerpac(dannye)
                        dannye = (count_mems + 1, message.from_user.id)
                        update_count_sticker(dannye)
                        sett = bot.get_sticker_set(
                            name=f'sticker_{str(message.from_user.id)}_{str(settt)}_by_tester_64_bot')
                        keyb = types.InlineKeyboardMarkup()
                        btn1 = types.InlineKeyboardButton('👍', callback_data='like:0:0:l')
                        btn2 = types.InlineKeyboardButton('👎', callback_data='like:0:0:d')
                        keyb.add(btn1, btn2)
                        bot.send_sticker(message.chat.id, sticker=sett.stickers[-1].file_id, reply_markup=keyb)
            except:
                bot.send_message(message.chat.id, text=f'Введите текст')


def add_channel(message):
    list_channel = message.text
    list_channel = list_channel.split(',')
    dannye = (list_channel[0], list_channel[1], list_channel[2])
    insert_channel(dannye)
    all_channels = select_channels()
    txt = f''
    for i in range(len(all_channels)):
        txt = txt + f'{all_channels[i][0]}, {all_channels[i][1]}, {all_channels[i][2]}\n'
    bot.send_message(message.chat.id, text=f'Канал добавлен!\n\n{txt}')


def del_chan(message):
    name = message.text
    dannye = ((name),)
    delete_channel(dannye)
    bot.send_message(message.chat.id, text=f'Канал удален')


@bot.callback_query_handler(func=lambda call: True)
def querry_handler(call):
    global admin_send

    data = call.data.split(':')
    if data[0] == 'start':
        fl_ch = True
        channels = select_channels()
        for i in range(len(channels)):
            check = bot.get_chat_member(channels[i][1].split()[0], call.message.from_user.id)
            if check.status == 'left':
                fl_ch = False
        if not (fl_ch):
            keyboard2 = types.InlineKeyboardMarkup()
            for i in range(len(channels)):
                btn1 = types.InlineKeyboardButton(f'Подписаться {i + 1}', url=f'{channels[i][2].split()[0]}')
                keyboard2.add(btn1)
            btn2 = types.InlineKeyboardButton('Проверить подписку', callback_data='start')
            keyboard2.add(btn2)
            bot.send_message(call.message.chat.id,
                             text=f'💕{call.message.from_user.first_name}, для бесплатного\nдоступаподпишитесь на каналы\nниже:\n\nза это вы получите подарок :)',
                             reply_markup=keyboard2)
        else:
            bot.send_message(call.message.chat.id,
                             text=f'💬 Мемоцит - бот для чатов :)\n\n– отправьте сообщение чтобы \nсоздать мемоцит, ответьте \nна чьё-то сообщение\nкомандой /m и бот сделает \nмемоцит. \n\n#⃣ Другие команды, инфа (https://telegra.ph/Instrukciya---Memocit-01-15)')
    elif data[0] == 'sticker':
        value = ((call.message.chat.id),)
        keyb = types.InlineKeyboardMarkup()
        settt = select_set(value)[0][0]
        for i in range(settt):
            btn1 = types.InlineKeyboardButton(f'Цитаты {call.message.from_user.first_name}№{i + 1}',
                                              callback_data=f'settt:{i + 1}')
            keyb.add(btn1)
        bot.send_message(call.message.chat.id, text=f'💎 список ваших стикерпаков:', reply_markup=keyb)
    elif data[0] == 'settt':
        keyb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Удалить стикер', callback_data=f'delete:{data[1]}')
        keyb.add(btn1)
        bot.send_message(call.message.chat.id,
                         text=f'🛠 Редактирование набора http://t.me/addstickers/stick_{str(call.from_user.id)}_{str(data[1])}_by_hood1000richbot',
                         reply_markup=keyb)
    elif data[0] == 'delete':
        bot.send_message(call.message.chat.id,
                         f'Пришлите стикер, который хотите 🗑 удалить из набора http://t.me/addstickers/stick_{str(call.from_user.id)}_{str(data[1])}_by_hood1000richbot')
        bot.register_next_step_handler(call.message, del_st, data[1])
    elif data[0] == 'like':
        keyb = types.InlineKeyboardMarkup()
        if data[3] == 'l':
            btn1 = types.InlineKeyboardButton(f'👍{int(data[1]) + 1}',
                                              callback_data=f'like:{int(data[1]) + 1}:{data[2]}:l')
            btn2 = types.InlineKeyboardButton(f'👎{int(data[2])}', callback_data=f'like:{int(data[1]) + 1}:{data[2]}:d')
            keyb.add(btn1, btn2)
        else:
            btn1 = types.InlineKeyboardButton(f'👍{int(data[1])}',
                                              callback_data=f'like:{int(data[1])}:{int(data[2]) + 1}:l')
            btn2 = types.InlineKeyboardButton(f'👎{int(data[2]) + 1}',
                                              callback_data=f'like:{int(data[1])}:{int(data[2]) + 1}:d')
            keyb.add(btn1, btn2)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=keyb)

    elif data[0] == 'chat_statistic':
        database = r'meme.db'
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM chats")
        chats = cur.fetchall()
        count = 0

        for chat in chats:
            try:
                count += int(bot.get_chat_members_count(chat[1]))
            except:
                print(traceback.format_exc())

        cur.execute(f"SELECT * FROM user")
        users = cur.fetchall()
        bot.send_message(call.message.chat.id, f"""Количество чатов: {len(chats)}\n
Количество пользователей в чатах: {count}\n
Количество пользоваталей ботом: {len(users)}""")

    elif data[0] == 'send_messages':
        bot.send_message(call.message.chat.id, "Введите сообщение для рассылки")
        admin_send = True


def del_st(call, settt):
    number_st = call.text
    sett = bot.get_sticker_set(name=f'sticker_{str(call.from_user.id)}_{str(settt)}_by_tester_64_bot')
    delst = sett.stickers[int(number_st) + 1].file_id
    bot.delete_sticker_from_set(delst)
    bot.send_message(call.chat.id, text=f'Стикер удален')


bot.infinity_polling(timeout=10, long_polling_timeout=5)
