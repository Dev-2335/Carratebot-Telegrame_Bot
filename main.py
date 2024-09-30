from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes 

TOKEN: Final = YOUR_TOKEN_HERE
BOT_USERNAME: Final = '@carratebot'

#COMMANDS
async def start_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me! How can i help you??')


async def help_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''
                                    Hello! I am a Carrate Master! \nCreated by Dev!! \nI can help you to calculate maths function just write Calculate and your equation.\n/start - start chatting\n/help - for help
                                    ''')


async def custom_command(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is custom command!')



#Responses

def handle_response(text: str) -> str:
    processed : str = text.lower()

    
    if any(txt in processed for txt in ['hello', 'hi', 'hey']):
        return 'Hey there!'
    
    if any(txt in processed for txt in ['how are you', 'how are you doing', 'how are you going']):
        return 'I am good!'
    
    if any(txt in processed for txt in ['good morning', 'good evening', 'good afternoon', 'good night']):
        return processed.title()
    
    if any(txt in processed for txt in ['can you help me', 'i need you help', 'i have a question']):
        return 'Yes sure,how can i help you!!'
    
    if 'who are you' in processed:
        return 'I am a Carrot.  The Carrate Master,Created by Dev!!'
    
    if 'thank you' in processed:
        return 'Most Welcome!!'
    
    if 'calculate' in processed:
        try:
            ans = eval(processed.replace('calculate', '').strip())
        except Exception as e:
            print(f"Error evaluating expression: {e}")
            ans = 'This can not be evaluated!'
        return f'Answer is {ans}'

    
    
    return 'I do not understand what you wrote...'

#For_group_chat
async def handle_message(update: Update , context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id})in {message_type} : "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)


        print('Bot:',response)
        await update.message.reply_text(response)

#For_Error==
async def error(update: Update,context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')



if __name__ == '__main__':
    print('Startinng Bot...')
    app = Application.builder().token(TOKEN).build()


    #Commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))


    #Messages
    app.add_handler(MessageHandler(filters.TEXT , handle_message))


    #Errors
    app.add_error_handler(error)

    #Checks every 3 sec
    print('Polling...')
    app.run_polling(poll_interval=3)