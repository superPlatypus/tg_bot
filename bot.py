from doctest import OutputChecker
from urllib import response
import telebot
from gtts import gTTS
from pycoingecko import CoinGeckoAPI
import requests
import json
import os
from pytube import YouTube
import youtube_dl
from yt_dlp import YoutubeDL
import urllib.request
from googletrans import Translator

bot = telebot.TeleBot('5435181622:AAE2BNEWaw8uBwjxKjKmUViM_1Pr5J7re9Q');
cg = CoinGeckoAPI()


@bot.message_handler(commands=['say'])
def say(message):
    cid = message.chat.id
    text = message.text[4:]
    speech = gTTS(text = text, lang = 'ru', slow = 'false')
    speech.save('tg_bot\speech.mp3')
    bot.send_audio(cid, open('tg_bot\speech.mp3', 'rb'))


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
        "X-RapidAPI-Key": "6713ccc8b1mshcd4451e44154eabp155c8fjsn6c23347a3abc",
        "X-RapidAPI-Host": "tiktok-downloader-download-tiktok-videos-without-watermark.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if (os.path.exists('tt_video.mp4')):
        os.remove('tt_video.mp4')
    urllib.request.urlretrieve(response.json()['video'][0], 'tt_video.mp4')
    cid = message.chat.id
    bot.send_video(cid, open('tt_video.mp4', 'rb'))



@bot.message_handler(func=lambda message: True)
def smart_answer(message):
    if message.text.lower() == "нет":
        bot.reply_to(message, "Пидора ответ")
    if message.text.lower() == "да":
        bot.reply_to(message, "Пизда")


bot.infinity_polling()