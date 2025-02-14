import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Token del bot de Telegram
TOKEN = 'TU_TOKEN_AQUI'

# Lista de recordatorios
reminders = []
user_state = {}
scheduler = AsyncIOScheduler()

# Función para enviar notificaciones automáticas
async def send_reminder(context: ContextTypes.DEFAULT_TYPE) -> None:
    job = context.job
    await context.bot.send_message(job.context["chat_id"], text=f"📢 Recordatorio: {job.context['title']}\n{job.context['message']}")

# Función para agregar recordatorios con notificaciones automáticas
def schedule_reminder(chat_id, title, message, reminder_time):
    scheduler.add_job(send_reminder, 'date', run_date=reminder_time, args=[chat_id], id=str(reminder_time), replace_existing=True, 
                      context={"chat_id": chat_id, "title": title, "message": message})

# Función para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Añadir Recordatorio", callback_data="add_reminder")],
        [InlineKeyboardButton("Lista de Recordatorios", callback_data="list_reminders")],
        [InlineKeyboardButton("Eliminar Recordatorio", callback_data="delete_reminder")],
        [InlineKeyboardButton("Configurar", callback_data="config")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("¡Hola! ¿Qué te gustaría hacer?", reply_markup=reply_markup)

# Función para manejar la acción de añadir un recordatorio
async def add_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    user_state[update.callback_query.from_user.id] = "TITLE"
    await update.callback_query.message.reply_text("Escribe el título del recordatorio.")

# Función para manejar el título del recordatorio
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    text = update.message.text

    if user_state.get(user_id) == "TITLE":
        context.user_data["title"] = text
        user_state[user_id] = "MESSAGE"
        await update.message.reply_text("Ahora escribe el mensaje del recordatorio.")
    elif user_state.get(user_id) == "MESSAGE":
        context.user_data["message"] = text
        user_state[user_id] = "DATE"
        await update.message.reply_text("Escribe la fecha y hora del recordatorio (YYYY-MM-DD HH:MM)")
    elif user_state.get(user_id) == "DATE":
        try:
            reminder_time = datetime.strptime(text, "%Y-%m-%d %H:%M")
            reminders.append((reminder_time, context.user_data["title"], context.user_data["message"]))
            schedule_reminder(update.message.chat_id, context.user_data["title"], context.user_data["message"], reminder_time)
            await update.message.reply_text(f"✅ Recordatorio guardado para {reminder_time}.")
        except ValueError:
            await update.message.reply_text("Formato incorrecto. Usa YYYY-MM-DD HH:MM")

# Función para listar los recordatorios
async def list_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    if reminders:
        reminders_text = "\n".join([f"{r[0]} - {r[1]}: {r[2]}" for r in reminders])
        await update.callback_query.message.reply_text(f"Lista de recordatorios:\n{reminders_text}")
    else:
        await update.callback_query.message.reply_text("No tienes recordatorios aún.")

# Función para eliminar todos los recordatorios
async def delete_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    reminders.clear()
    scheduler.remove_all_jobs()
    await update.callback_query.message.reply_text("Todos los recordatorios han sido eliminados.")

# Configurar el bot
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    scheduler.start()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(add_reminder, pattern="add_reminder"))
    application.add_handler(CallbackQueryHandler(list_reminders, pattern="list_reminders"))
    application.add_handler(CallbackQueryHandler(delete_reminder, pattern="delete_reminder"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling()

if __name__ == "__main__":
    main()
