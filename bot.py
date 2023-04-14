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
newNomi = []

def shuffleDictionary(d):
    l = list(d.items())
    random.shuffle(l)
    return dict(l)

def modStage(str):
    global in_stage
    in_stage = str

def extract_arg(arg):
    if len(arg.split()) > 1:
        return arg.split()[1:][0]
    else:
        return "1"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("/chipaga")
    but2 = types.KeyboardButton("/conferma 1")
    but3 = types.KeyboardButton("/conferma 2")
    but4 = types.KeyboardButton("/conferma 3")
    but5 = types.KeyboardButton("/conferma 4")
    but6 = types.KeyboardButton("/situazione")
    markup.add(but1, but2, but3, but4, but5, but6)
    bot.reply_to(message, "Ciao! Benvenuto nel bot che dice chi paga il caffe ogni giorno!", parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['chipaga', 'caffe', "dimmichipaga", "alternativa"])
def send_coffie(message):
    global newNomi
    if not newNomi or in_stage == "":
        newNomi = list(sorted(shuffleDictionary(nomi).items(), key=lambda item: item[1]))
    modStage(newNomi[0][0])
    newNomi = newNomi[1:]
    bot.reply_to(message, in_stage)
    
@bot.message_handler(commands=['conferma', 'hapagato', "ok"])
def send_confirm(message):
    if in_stage == "":
        bot.reply_to(message, "Coglione, devi prima far generare qualcuno "+in_stage)
    else:
        n_coffee = extract_arg(message.text)
        if n_coffee.isnumeric():
            nomi[in_stage] += int(n_coffee)
        else:
            nomi[in_stage] += 1
        with open("db.txt", "w") as fp:
            json.dump(nomi, fp)
        if n_coffee.isnumeric():
            bot.reply_to(message, "Ok, "+in_stage+" ha pagato "+n_coffee+" caffè!")
        else:
            bot.reply_to(message, "Ok, "+in_stage+" ha pagato! (Ci hai provato merda, +1)")
        modStage("")
        
@bot.message_handler(commands=['situazione', 'riassunto', "totale"])
def send_confirm(message):
    bot.reply_to(message, str(nomi))
    
@bot.message_handler(commands=['insulta'])
def send_confirm(message):
    bot.reply_to(message, "Luca non ha pubblicato!")


bot.infinity_polling()
