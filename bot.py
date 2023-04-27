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
        return arg.split()[1]
    else:
        return "1"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("/chipaga")
    but2 = types.KeyboardButton("/situazione")
    but3 = types.KeyboardButton("/conferma 1")
    but4 = types.KeyboardButton("/conferma 2")
    but5 = types.KeyboardButton("/conferma 3")
    but6 = types.KeyboardButton("/conferma 4")
    but7 = types.KeyboardButton("/conferma 5")
    markup.add(but1, but2, but3, but4, but5, but6, but7)
    bot.reply_to(message, "Ciao! Benvenuto nel bot che dice chi paga il caffe ogni giorno e ricorda a Valerio che non ha pubblicato!", parse_mode='html', reply_markup=markup)

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
        if n_coffee.lstrip("-").isnumeric():
            add = int(n_coffee)
            if add < 1:
                add = 1
            nomi[in_stage] += add
            with open("db.txt", "w") as fp:
                json.dump(nomi, fp)
            if int(n_coffee) < 1:
                bot.reply_to(message, "Ci hai provato, ma "+in_stage+" ha comunque pagato 1 caffè, ti meriti una chiacchierata con la Damy")
            else:
                bot.reply_to(message, "Ok, "+in_stage+" ha pagato "+n_coffee+" caffè!")
        else:
            bot.reply_to(message, in_stage+" non ha pagato! (Ci hai provato, scommetto che le tue pubblicazioni sono le stesse di Verio, merda), nel dubbio -2 a Verio")
        modStage("")
        
@bot.message_handler(commands=['situazione', 'riassunto', "totale"])
def send_confirm(message):
    bot.reply_to(message, str(nomi))
    
@bot.message_handler(commands=['insulta'])
def send_confirm(message):
    shamer = list(shuffleDictionary(nomi).items())[0][0]
    bot.reply_to(message, shamer + " come al solito non ha pubblicato! Vergognati Vezio (so che anche te sicuramente non l'hai fatto)")


bot.infinity_polling()
