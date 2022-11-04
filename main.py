import telebot
import numpy
import pandas
cars = pandas.read_csv("cars.csv", encoding = "UTF-8")
try:
    person = pandas.read_csv("person.csv", encoding = "UTF-8")
except Exception:

    person = pandas.DataFrame(
    {
        "phone number": [""],
        "telegram id": [0],
        "name": [""],
        "surname": [""],
        "last name": [""],
    }
)
    person.to_csv("person.csv", encoding = "UTF-8")
bot = telebot.TeleBot("5721652129:AAFJcqV2LoDGNOno2TbpiYf_VLeou2zHCro");
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global person
    mtext = message.text.split()
    try:
        if mtext[0]=="зб":
            if mtext[1]=="дебаг":
                if mtext[2] == "принтмашины":
                    bot.send_message(message.chat.id, cars.to_string())
            if mtext[1] == "рег":
                person = person.append(pandas.Series([mtext[5], message.from_user.id, mtext[2], mtext[3], mtext[4]]), ignore_index=True)
                person.to_csv("person.csv", encoding = "UTF-8")
                bot.send_message(message.chat.id, "Успешно")
    except Exception as e:
        bot.send_message(message.chat.id, str(e))
bot.polling(none_stop=True, interval=0)