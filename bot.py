import random
import json
import telebot
from telebot import types
f = open("api_key.txt", "r") #Secret API_KEY
TOKEN = f.read()
bot = telebot.TeleBot(TOKEN)

with open("db.txt", "r") as fp:
    nomi = json.load(fp)

in_stage = ""

def shuffleDictionary(d):
    l = list(d.items())
    random.shuffle(l)
    return dict(l)

def modStage(str):
    global in_stage
    in_stage = str

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("/chipaga")
    but2 = types.KeyboardButton("/conferma")
    but3 = types.KeyboardButton("/situazione")
    markup.add(but1, but2, but3)
    bot.reply_to(message, "Ciao! Benvenuto nel bot che dice chi paga il caffe ogni giorno!", parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['chipaga', 'caffe', "dimmichipaga", "alternativa"])
def send_coffie(message):
    newNomi = {}
    newNomi = shuffleDictionary(nomi)
    modStage(min(newNomi, key=newNomi.get))
    bot.reply_to(message, in_stage)
    
@bot.message_handler(commands=['conferma', 'hapagato', "ok"])
def send_confirm(message):
    if in_stage == "":
        bot.reply_to(message, "Coglione, devi prima far generare qualcuno "+in_stage)
    else:
        nomi[in_stage] += 1
        with open("db.txt", "w") as fp:
            json.dump(nomi, fp)
        bot.reply_to(message, "Ok, "+in_stage+" ha pagato!")
        modStage("")
        
@bot.message_handler(commands=['situazione', 'riassunto', "totale"])
def send_confirm(message):
    bot.reply_to(message, str(nomi))


bot.infinity_polling()
