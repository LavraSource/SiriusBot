import telebot
import numpy
import pandas
import os
import sys
os.chdir(os.path.dirname(sys.argv[0]))
cars = pandas.read_csv("cars.csv", encoding = "UTF-8")
try:
    person = pandas.read_csv("person.csv", encoding = "UTF-8")
except Exception:

    person = pandas.DataFrame(
    {
        "phone number": [],
        "telegram id": [],
        "name": [],
        "surname": [],
        "last name": [],
    }
)
    person.to_csv("person.csv", encoding = "UTF-8")
bot = telebot.TeleBot("5721652129:AAFJcqV2LoDGNOno2TbpiYf_VLeou2zHCro");
pdata = pandas.Series(index = ["phone number", "telegram id", "name", "surname", "last name"], dtype=object)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global person
    mtext = message.text.split()
    try:
        if mtext[0]=="зб":
            if mtext[1]=="дебаг":
                if mtext[2] == "принтмашины":
                    bot.send_message(message.chat.id, cars.to_string())
                if mtext[2] == "принтлюди":
                    bot.send_message(message.chat.id, cars.to_string())
            if mtext[1] == "рег":
                if len(mtext) > 2:
                    person = person.append(pandas.Series([mtext[5], message.from_user.id, mtext[2], mtext[3], mtext[4]]), ignore_index=True)
                    person.to_csv("person.csv", encoding = "UTF-8")
                    bot.send_message(message.chat.id, "Успешно")
                else:
                    msg = bot.send_message(message.chat.id, "Как вас зовут (ФИО)?")
                    bot.register_next_step_handler(msg, regStepName)
    except Exception as e:
        bot.send_message(message.chat.id, str(e))
def regStepName(message):
    global pdata
    mtext = message.text.split()
    try:
        pdata["name"] = mtext[0]
        pdata["surname"] = mtext[1]
        pdata["last name"] = mtext[2]
        msg = bot.send_message(message.chat.id, "Какой ваш номер?")
        bot.register_next_step_handler(msg, regStepNumber)
    except Exception as e:
        bot.send_message(message.chat.id, str(e))
def regStepNumber(message):
    global pdata, person
    mtext = message.text
    try:
        pdata["phone number"] = mtext
        pdata["telegram id"] = message.from_user.id
        person = person.append(pdata, ignore_index=True)
        person.to_csv("person.csv", encoding = "UTF-8")
        bot.send_message(message.chat.id, "Успешно")
    except Exception as e:
        bot.send_message(message.chat.id, str(e))
bot.polling(none_stop=True, interval=0)