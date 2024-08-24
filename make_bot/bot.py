import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'make_bot.settings')  # Ensure this is correct

import django
django.setup()

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext
from asgiref.sync import sync_to_async
from courses.models import Course, UserData  # Now you can safely import the Course model
import requests
from bs4 import BeautifulSoup




# Define the categories available
categories = [
    ('python', 'Python'),
    ('java', 'Java'),
    ('javascript', 'JavaScript'),
    ('webdev', 'Web Development'),
    ('machinelearning', 'Machine Learning'),
    ('other', 'Other')
]

# Start command to greet the user and show available commands
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id

    # Fetch or create the user in a synchronous context
    user_data = await sync_to_async(UserData.objects.filter(id=user_id).first)()

    if user_data:
        await update.message.reply_text(
            f"Hello, welcome back {user_data.first_name}!"
        )
    else:
        new_user = UserData(
            id=user_id,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name,
            username=update.effective_user.username
        )
        await sync_to_async(new_user.save)()
        await update.message.reply_text(f"Welcome {update.effective_user.first_name} to your home.")

# Help command to list available commands
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        """
        Available commands:
        /start  -> Start the bot
        /help  -> Get help
        /translate -> Enable translation mode (Kurdish to English)
        /free  -> Get free Udemy course
        /show_users -> Show registered users
        /contact  -> Contact me
        """
    )

# Define bot functions
async def free(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton(category[1], callback_data=f"category:{category[0]}")]
        for category in categories
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Please choose a category:", reply_markup=reply_markup
    )

async def category_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    category = query.data.split(':')[1]

    # Query the courses for the selected category
    courses = await sync_to_async(list)(Course.objects.filter(category=category))

    if not courses:
        await query.edit_message_text(
            text="Sorry, there are no courses available in this category. Please try again later."
        )
        return

    keyboard = [
        [InlineKeyboardButton(course.title, callback_data=f"course:{course.id}")]
        for course in courses
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="Please choose a course:", reply_markup=reply_markup
    )

async def course_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    course_id = query.data.split(':')[1]
    course = await sync_to_async(Course.objects.get)(id=course_id)

    # Define the button
    button = [
        [InlineKeyboardButton("🔗 Click here to get the course", url=course.url)]
    ]
    reply_markup = InlineKeyboardMarkup(button)

    # Edit the message with course title and info
    await query.edit_message_text(
        text=(
              f"> ⏰: time \\(2:50 hours \\)\n"
              f"> ⭐: 4\\./5\n"  # '.' is escaped
              f"> 👨‍🎓: 184,664 students\n"
              f"> 📊: Development \\> Data Science\n"
              f"> 🗣: English \\(US\\)\n"
              f"> 💬: Dive into the world of Docker and learn about Dockerfiles and Container Management"
              f"\n\n[{course.title}](\\{course.url})"
        ),
        reply_markup=reply_markup,
        parse_mode="MarkdownV2"
    )

async def contact(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        parse_mode="MarkdownV2",
        text =(
            "📣 *If you have any questions\\, feel free to ask\\. Contact me at:*\n\n"
            "> ⏰ [Telegram](https://t\\.me/Ramyar_mhamad): `@Ramyar\\_mhamad`\n\n"
            "> ⭐ Snapchat: `adam69iiu`\n\n"
            "> 📞 Phone: `07505821211`\n\n"
            "_ssssss_ 😉😉😉😉😉😉 _ssssss_"
        ),
    )

# Initialize the bot application
application = Application.builder().token(os.getenv("TOKEN")).build()

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("free", free))
application.add_handler(CommandHandler("contact", contact))
application.add_handler(CallbackQueryHandler(category_selection, pattern="^category:"))
application.add_handler(CallbackQueryHandler(course_selection, pattern="^course:"))


# Start the bot
if __name__ == "__main__":
    application.run_polling()
