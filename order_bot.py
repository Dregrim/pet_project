
from telegram import ReplyKeyboardMarkup, KeyboardButton,Update,BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler,filters,CallbackQueryHandler
import adminpanel.mysqlqueries as q
# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    button = KeyboardButton("Поділитися номером ☎️", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[button]], one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Привіт! Поділися номером:", reply_markup=reply_markup)


async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    phone = contact.phone_number
    if phone.startswith("+"):
        tel_number = phone[3:]
    elif phone.startswith("3"):
        tel_number = phone[2:]
    else:
        print(phone)
        await update.message.reply_text("Сталась помилка")
    name = contact.first_name
     
    # Зберігаємо або отримуємо клієнта
    client_id = q.client_id(tel_number)
    context.user_data["client_id"] = client_id

    keyboard = [
        ["📃 Список замовлень"],
        ["Інформація про клієнта"],
        ["Допомога"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"Дякую, {name}! Я зберіг твій номер: {phone}",
        reply_markup=reply_markup
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📃 Список замовлень"],
        ["Інформація про клієнта"],
        ["Допомога"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"Оберіть дію:",
        reply_markup=reply_markup
    )

async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client_id = context.user_data.get("client_id")

    if not client_id:
        await update.message.reply_text("Спершу поділися своїм номером за допомогою /start")
        return

    orders = q.orders_list(client_id)

    if not orders:
        await update.message.reply_text("У тебе ще немає замовлень")
    else:
        text = "\n".join([f"ID: {o[0]}, Date: {o[1]}, Status: {o[2]}" for o in orders])
        await update.message.reply_text(f"Твої замовлення:\n{text}")
    
    
    keyboard = [[f"Замовлення {o[0]}"] for o in orders]  
    keyboard += [["👈 Назад"]]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Оберіть замовлення:", reply_markup=reply_markup)

async def item_list(order_id, update: Update, context: ContextTypes.DEFAULT_TYPE):
    client_id = context.user_data.get("client_id")
    o_client_id = q.client_by_order(order_id)
    if client_id == o_client_id[0]:
        items = q.order_items(order_id)
        t_items = []

        if not items:
            await update.message.reply_text("Сталась помилка")
        else:
            total_sum = sum(i[1] for i in items)
        
            t_items.append(["Разом:",f"{total_sum} грн"])
            text = f"<b>Замовлення   №{order_id}</b>\n\n"
            for i in items:
                name, price, quantity = i
                if quantity >1:
                    qu = 0
                    while qu < quantity:
                        text+=f"{name} - {price} грн\n\n"
                        qu +=1
                else:        
                    text+=f"{name} - {price} грн\n\n"
                qu = 0
            text += f"Загальна сума - {total_sum} грн"
            await update.message.reply_text(text,parse_mode="HTML")

        keyboard = [["📃 Список замовлень"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text("Назад до списку замовлень:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Вибачте, це не Ваше замовлення.")
    
    
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client_id = context.user_data.get("client_id")
    client = q.client_profile(client_id)
    first_name, last_name, tel_number, email = client
    text = f"Інформація про Вас:\n\n Ім'я:\t{first_name}\n\n Прізвище:\t{last_name}\n\n Номер телефону:\t{tel_number}\n\n E-mail:\t{email}"
    await update.message.reply_text(text,parse_mode="HTML")
    keyboard = [["👈 Назад"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("Повернутись в головне меню:", reply_markup=reply_markup)



async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📃 Список замовлень":
        await orders(update, context)
    elif text.startswith("Замовлення"):
        order_id = text.split()[1]  # отримуємо ID замовлення з кнопки
        await item_list(order_id, update, context)
    elif text == "👈 Назад":
        await buttons(update, context)
    elif text == "Інформація про клієнта":
         await profile(update, context)


def main():
    app = ApplicationBuilder().token("8096008190:AAHepIlz_iYiGPbrDpztZbchXqY_1pa6Zg4").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("orders", orders))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))
    app.add_handler(CommandHandler("item_list", item_list))
    app.add_handler(CallbackQueryHandler(item_list))

    app.run_polling()

if __name__ == "__main__":
    main()