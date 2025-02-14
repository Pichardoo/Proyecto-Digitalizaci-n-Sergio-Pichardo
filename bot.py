from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Token del bot de Telegram
TOKEN = '7632006497:AAHf669gCx8w0aLpI8AYNpFbhbd-W8tMxo0'

# Lista de recordatorios
reminders = []
selected_date = None  # Para guardar la fecha seleccionada
year_selected = None  # Año seleccionado
month_selected = None  # Mes seleccionado
hour_selected = None  # Hora seleccionada
minute_selected = None  # Minuto seleccionado
reminder_title = None  # Título del recordatorio
reminder_message = None  # Mensaje del recordatorio
user_state = {}  # Guardamos el estado de cada usuario

# Función para el comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Crear los botones del menú
    keyboard = [
        [InlineKeyboardButton("Añadir Recordatorio", callback_data="add_reminder")],
        [InlineKeyboardButton("Lista de Recordatorios", callback_data="list_reminders")],
        [InlineKeyboardButton("Eliminar Recordatorio", callback_data="delete_reminder")],
        [InlineKeyboardButton("Help", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "¡Hola! ¿Qué te gustaría hacer?",
        reply_markup=reply_markup
    )

# Función para manejar la acción de añadir un recordatorio
async def add_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    user_state[update.callback_query.from_user.id] = "TITLE"  # Guardamos el estado del usuario
    await update.callback_query.message.reply_text("Por favor, escribe el título de tu recordatorio.")

# Función para manejar la lista de recordatorios
async def list_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    if reminders:
        reminders_text = "\n\n".join([f"{reminder[0].strftime('%Y-%m-%d %H:%M')} - {reminder[1]}: {reminder[2]}" for reminder in reminders])
        await update.callback_query.message.reply_text(f"Lista de recordatorios:\n{reminders_text}")
    else:
        await update.callback_query.message.reply_text("No tienes recordatorios aún.")

# Función para eliminar todos los recordatorios
async def delete_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    if reminders:
        reminders.clear()  # Borra todos los recordatorios
        await update.callback_query.message.reply_text("Todos los recordatorios han sido eliminados.")
    else:
        await update.callback_query.message.reply_text("No tienes recordatorios para eliminar.")

# Función para mostrar el Help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    help_text = (
        "Este bot te permite gestionar tus recordatorios de manera sencilla.\n\n"
        "Comandos disponibles:\n"
        "/recordar - Añadir un nuevo recordatorio\n"
        "/list - Ver todos los recordatorios\n"
        "/delete - Eliminar todos los recordatorios\n"
        "Puedes hacer clic en los botones para interactuar con el bot."
    )
    await update.callback_query.message.reply_text(help_text)

# Función para iniciar el proceso de creación de un recordatorio
async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_state[update.message.from_user.id] = "TITLE"  # Guardamos el estado del usuario
    await update.message.reply_text("Por favor, escribe el título de tu recordatorio.")

# Función para manejar el título del recordatorio
async def handle_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    
    if user_state.get(user_id) == "TITLE":
        global reminder_title
        reminder_title = update.message.text  # Guardamos el título
        user_state[user_id] = "MESSAGE"  # Cambiamos el estado a "MESSAGE"
        await update.message.reply_text("Ahora, escribe el mensaje del recordatorio.")
    elif user_state.get(user_id) == "MESSAGE":
        global reminder_message
        reminder_message = update.message.text  # Guardamos el mensaje
        user_state[user_id] = "DATE"  # Cambiamos el estado a "DATE"
        
        # Iniciamos la selección de la fecha
        await update.message.reply_text("Perfecto. Ahora, selecciona el año para el recordatorio.")
        
        # Mostrar años disponibles (actual + 5 años)
        current_year = datetime.now().year
        years = [current_year + i for i in range(6)]
        
        buttons = [[InlineKeyboardButton(str(year), callback_data=f"year_{year}") for year in years]]
        
        return await update.message.reply_text(
            "Por favor, selecciona un año:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# Función para manejar la selección del año
async def handle_year_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    global year_selected
    year_selected = int(query.data.split("_")[1])  # Extraemos el año
    
    # Mostrar los meses disponibles (1-12)
    buttons = [InlineKeyboardButton(str(i), callback_data=f"month_{i}") for i in range(1, 13)]
    month_rows = [buttons[i:i + 4] for i in range(0, len(buttons), 4)]  # Dividimos en filas de 4 botones
    
    await query.edit_message_text(
        f"Año seleccionado: {year_selected}. Ahora selecciona el mes:",
        reply_markup=InlineKeyboardMarkup(month_rows)
    )

# Función para manejar la selección del mes
async def handle_month_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    global month_selected
    month_selected = int(query.data.split("_")[1])  # Extraemos el mes
    
    # Mostrar los días del mes seleccionado
    days_in_month = [InlineKeyboardButton(str(day), callback_data=f"day_{day}") for day in range(1, 32)]
    await query.edit_message_text(
        f"Mes seleccionado: {month_selected}. Ahora selecciona el día:",
        reply_markup=InlineKeyboardMarkup([days_in_month[i:i + 7] for i in range(0, len(days_in_month), 7)]))
    
# Función para manejar la selección del día
async def handle_day_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    global selected_date
    day = int(query.data.split("_")[1])  # Extraemos el día seleccionado
    selected_date = datetime(year_selected, month_selected, day)
    
    await query.edit_message_text(f"Fecha seleccionada: {selected_date.strftime('%Y-%m-%d')}. Ahora, selecciona la hora:")

    # Mostrar horas disponibles (de 0 a 23)
    hours = [InlineKeyboardButton(f"{i:02}", callback_data=f"hour_{i}") for i in range(24)]
    hour_rows = [hours[i:i + 4] for i in range(0, len(hours), 4)]  # Dividimos en filas de 4 botones
    
    await query.message.reply_text(
        "Selecciona la hora:",
        reply_markup=InlineKeyboardMarkup(hour_rows)
    )

# Función para manejar la selección de la hora
async def handle_hour_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    global hour_selected
    hour_selected = int(query.data.split("_")[1])  # Extraemos la hora seleccionada
    
    # Mostrar minutos disponibles (de 00 a 55, incrementados de 5 en 5)
    minutes = [InlineKeyboardButton(f"{i:02}", callback_data=f"minute_{i}") for i in range(0, 60, 5)]
    minute_rows = [minutes[i:i + 4] for i in range(0, len(minutes), 4)]  # Dividimos en filas de 4 botones
    
    await query.edit_message_text(f"Hora seleccionada: {hour_selected:02}. Ahora, selecciona los minutos:")
    
    await query.message.reply_text(
        "Selecciona los minutos:",
        reply_markup=InlineKeyboardMarkup(minute_rows)
    )

# Función para manejar la selección de los minutos
async def handle_minute_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    global minute_selected
    minute_selected = int(query.data.split("_")[1])  # Extraemos los minutos seleccionados
    
    # Guardamos el recordatorio
    reminder_time = datetime(year_selected, month_selected, selected_date.day, hour_selected, minute_selected)
    reminders.append((reminder_time, reminder_title, reminder_message))
    
    await query.edit_message_text(f"Recordatorio agregado para {reminder_time.strftime('%Y-%m-%d %H:%M')}.\n\nTítulo: {reminder_title}\nMensaje: {reminder_message}")


# Función para notificaciones automáticas
async def send_reminders() -> None:
    while True:
        now = datetime.now()
        for reminder in reminders:
            reminder_time, title, message = reminder
            if reminder_time <= now:
                await application.bot.send_message(chat_id=YOUR_CHAT_ID, text=f"¡Es hora! {title}: {message}")
                reminders.remove(reminder)
        await asyncio.sleep(60)  # Revisa cada minuto

    
# Configurar el bot
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Comandos
    application.add_handler(CommandHandler("start", start))

    # Menú interactivo
    application.add_handler(CallbackQueryHandler(add_reminder, pattern="add_reminder"))
    application.add_handler(CallbackQueryHandler(list_reminders, pattern="list_reminders"))
    application.add_handler(CallbackQueryHandler(delete_reminder, pattern="delete_reminder"))
    application.add_handler(CallbackQueryHandler(help, pattern="help"))

    # Manejo de selecciones de fecha, hora, etc.
    application.add_handler(CallbackQueryHandler(handle_year_selection, pattern="^year_"))
    application.add_handler(CallbackQueryHandler(handle_month_selection, pattern="^month_"))
    application.add_handler(CallbackQueryHandler(handle_day_selection, pattern="^day_"))
    application.add_handler(CallbackQueryHandler(handle_hour_selection, pattern="^hour_"))
    application.add_handler(CallbackQueryHandler(handle_minute_selection, pattern="^minute_"))

    # Manejo del título y mensaje de recordatorio
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_title))

    application.run_polling()

if __name__ == "__main__":
    main()
