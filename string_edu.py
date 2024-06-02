import random
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler


STARTING, INWORK, ENDING = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"""🤗 Привет, {update.effective_user.first_name}!
📝 Введи текст, над которым нужно работать :)
⛔️ Для остановки проверки по тексту, напиши /stop""", reply_markup=ReplyKeyboardRemove())
    return STARTING

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: 
    
    
    print(context.user_data["status"])
    text = text.split(".")
    output = ""
    for x in text:
        y = random.randint(1, 5)
        if y == 5:
            for z in x:
                output += "_"
            output += " "
        else:
            output += x + " "
    await update.message.reply_text(output + str(len(text)))

def cleaner(kidWord):
    kidWord = kidWord.replace("?", "")
    kidWord = kidWord.replace("!", "")
    kidWord = kidWord.replace(".", "")
    kidWord = kidWord.replace(",", "")
    kidWord = kidWord.replace("(", "")
    kidWord = kidWord.replace(")", "")
    return kidWord.casefold()

def right_random(words):
    output = random.sample(words, k=1)
    while len(output[0]) <= 2:
        output = random.sample(words, k=1)
    output = str(output[0])
    return output

async def starting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("starting")
    context.user_data["status"] = "1"
    context.user_data["number"] = "0"
    context.user_data["text"] = update.message.text
    text = update.message.text
    sentences = text.split(".")
    
    editSentence = sentences[0]
    words = editSentence.split(" ")
    
    allWords = text.split(" ")
    kidWord = right_random(words)
    right_random(allWords)
    ranWords = random.sample(allWords, k=3)

    reply_keyboard = [
    [cleaner(kidWord), cleaner(right_random(allWords))],
    [cleaner(right_random(allWords)), cleaner(right_random(allWords))],
    ]
    random.shuffle(reply_keyboard)
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    context.user_data["kidWord"] = cleaner(kidWord)
    
    await update.message.reply_text(editSentence.replace(kidWord, "__________"), reply_markup=markup)
    return INWORK

async def inwork(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("inwork")
##    context.user_data["status"] = "1"
    if context.user_data["kidWord"] == update.message.text:
        await update.message.reply_text("✅ Правильно!")
    else:
        await update.message.reply_text("❌ Неверно! Правильно: " + context.user_data["kidWord"])
    context.user_data["number"] = int(context.user_data["number"]) + 1
    text = context.user_data["text"]
    sentences = text.split(".")
    print(str(len(sentences)) + " " + str(context.user_data["number"]))
    if len(sentences)-1 == int(context.user_data["number"]):
        await update.message.reply_text("""✅ Молодчина! Текст закончился 👍
Пиши /start, чтобы скинуть мне ещё текстик :)""", reply_markup=ReplyKeyboardRemove())
        context.user_data.clear()
        print("ended")
        return ConversationHandler.END
    

    editSentence = sentences[context.user_data["number"]]
    words = editSentence.split(" ")
    allWords = text.split(" ")
    kidWord = right_random(words)
    right_random(allWords)
    ranWords = random.sample(allWords, k=3)

    reply_keyboard = [
    [cleaner(kidWord), cleaner(right_random(allWords))],
    [cleaner(right_random(allWords)), cleaner(right_random(allWords))],
    ]
    random.shuffle(reply_keyboard)
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    context.user_data["kidWord"] = cleaner(kidWord)
    
    await update.message.reply_text(editSentence.replace(kidWord, "__________"), reply_markup=markup)
    
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("""Все данные на данный текст обнуляются.
Пиши /start, чтобы скинуть мне ещё текстик :)""", reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    print("stoped")
    return ConversationHandler.END   


def main() -> None:
    app = Application.builder().token("").build()

    conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                STARTING: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, starting),
                ],
                INWORK: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, inwork)
                ],
            },
            fallbacks=[CommandHandler("stop", stop)],
        )
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
