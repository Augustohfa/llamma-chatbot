import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
import ollama
# Patch the event loop to allow nesting
nest_asyncio.apply()


# Define the Telegram bot token
telegram_token = "7865577166:AAGRst-NpPj15O13Owd6wHSfavmAMi3Hc-4"

# A dictionary to maintain conversation history for each user
conversation_context = {}
# Function to generate the response with LLaMA using Ol


def generate_response_with_llama(user_id, user_input, user_contact):
    model_name = "zarah_discord_ia"
    # Retrieve the conversation history for this user, or start a new one
    context = conversation_context.get(user_id, [])

    # Append the user message to the context
    context.append({"role": "user", "content": user_input})

    # Generate the response using the LLaMA model
    response = ollama.chat(model=model_name, messages=context)

    # Append the model's response to the context
    bot_response = response['message']['content']
    context.append({"role": "assistant", "content": bot_response})

    # Update the conversation context
    conversation_context[user_id] = context
    print(
        f'''
Respondendo para {user_contact.first_name} {user_contact.last_name} chat com ID: {user_id}
__________________________________________________
{bot_response}
__________________________________________________
        '''
    )

    return bot_response


async def respond_to_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id  # Get the user's ID
    user_input = update.message.text
    user_contact = update.message.chat
    message_time = update.message.date
    print(
        f'''{message_time}: {user_contact.first_name} {
            user_contact.last_name}: {user_input}'''
    )

    # Generate the response using the LLaMA model
    response = generate_response_with_llama(user_id, user_input, user_contact)

    # Send the response back to the user on Telegram
    await update.message.reply_text(response)

# Main function to set up the bot and handlers


async def main():
    # Create the application with the Telegram bot token
    application = Application.builder().token(telegram_token).build()

    # Add the handler to receive text messages
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, respond_to_message))

    # Start the bot with polling
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
