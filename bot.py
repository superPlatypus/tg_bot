import config 
from doctest import OutputChecker
from urllib import response
import telebot
from gtts import gTTS
from pycoingecko import CoinGeckoAPI
import requests
import json
import os
from yt_dlp import YoutubeDL
import urllib.request
from googletrans import Translator
import random


bot = telebot.TeleBot(config.bot_token);
cg = CoinGeckoAPI()


@bot.message_handler(commands=['say'])
def say(message):
    bot.delete_message(message.chat.id, message.message_id)
    cid = message.chat.id
    text = message.text[4:]
    speech = gTTS(text = text, lang = 'ru', slow = 'false')
    speech.save('speech.mp3')
    bot.send_audio(cid, open('speech.mp3', 'rb'))

@bot.message_handler(commands=['all'])
def all(message):
    bot.reply_to(message, "@Torch_head @PlatypusWithHat  @ferrnot @kirushahuesos")
    


@bot.message_handler(commands=['joke'])
def joke(message):
    response = requests.get('https://api.chucknorris.io/jokes/random')
    bot.reply_to(message, "Original: " + response.json()['value'] + "\n" + "Translated: " + Translator().translate(response.json()['value'], dest='ru').text)



@bot.message_handler(commands=['crypto'])
def crypto(message):
    data = cg.get_price(ids=['bitcoin', 'ethereum'], vs_currencies='usd')
    out = ""
    for crypto in data:
        for currency in data[crypto]:
            #print(crypto, data[crypto][currency])
            out = out + crypto + " " + str(data[crypto][currency]) + "$" + "\n"
    bot.reply_to(message, out) 

@bot.message_handler(commands=['yt'])
def download_from_yt(message):
    url = message.text.split(' ')[1]
    #print(link)
    # YouTube(link).streams.first().download('tg_bot')
    ydl_opts = {'outtmpl' : 'yt_video.mp4'}
    URLS = [url]
    if (os.path.exists('yt_video.mp4')):
        os.remove('yt_video.mp4')
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(URLS)
    cid = message.chat.id
    
    bot.send_video(cid, open('yt_video.mp4', 'rb'))

@bot.message_handler(commands=['tt'])
def download_from_tiktok(message):
    link = message.text.split(' ')[1]
    #bot.delete_message(message.chat.id, message.message_id)
    url = "https://tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com/index"
    querystring = {"url":link}
    headers = {
        "X-RapidAPI-Key": config.X_RapidAPI_Key,
        "X-RapidAPI-Host": "tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if (os.path.exists('tt_video.mp4')):
        os.remove('tt_video.mp4')
    urllib.request.urlretrieve(response.json()['video'][0], 'tt_video.mp4')
    cid = message.chat.id
    bot.send_video(cid, open('tt_video.mp4', 'rb'))

@bot.message_handler(commands=['cat'])
def send_cat(message):
    cid = message.chat.id
    a = 1
    if (random.randint(1,2) == 1):
        url = 'https://cataas.com/cat/gif'
        urllib.request.urlretrieve(url, 'cat_gif.gif')
        bot.send_video(cid, open('cat_gif.gif', 'rb'))
    else:
        url = 'https://cataas.com/cat'
        urllib.request.urlretrieve(url, 'cat_photo.jpeg')
        bot.send_photo(cid, open('cat_photo.jpeg', 'rb'))      




@bot.message_handler(func=lambda message: True)
def smart_answer(message):
    if message.text.lower() == "нет":
        bot.reply_to(message, "Пидора ответ")
    if message.text.lower() == "да":
        bot.reply_to(message, "Пизда")


bot.infinity_polling()
