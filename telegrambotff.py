from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_USERNAME = "mirzoevffbot"  # бе @ навис
WHATSAPP_NUMBER = "+992004116897"
TELEGRAM_USERNAME = "@mr_mirzoev_ff"
ADMIN_USERNAME = "@mr_mirzoev_ff"  # барои тугмаи "Баровардани алмаз"

user_referrals = {}
user_balances = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    keyboard = [
        [InlineKeyboardButton("📸 Инстаграм", url="https://www.instagram.com/ffmirzoev.tj?igsh=MXI3d2FhcndyY3QzbQ==")],
        [InlineKeyboardButton("📢 Телеграм", url="https://t.me/ffmirzoevtj")],
        [InlineKeyboardButton("🎵 Тикток", url="https://www.tiktok.com/@mr.mirzoev.ff?_t=ZN-8v4cAnrvSVy&_r=1")],
        [InlineKeyboardButton("✅ Ман обуна шудам", callback_data="check_subscription")]
    ]
    text = (
        "Хуш омадед, бародар!\n\n"
        "Илтимос, аввал ба каналҳои зерин обуна шавед:\n"
        "🔸 Инстаграм\n"
        "🔸 Телеграм\n"
        "🔸 Тикток\n\n"
        "Пас аз обуна шудан, тугмаи '✅ Ман обуна шудам'-ро зер кунед."
    )
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    username = query.from_user.username or f"user{user_id}"

    if query.data == "check_subscription":
        keyboard = [
            [InlineKeyboardButton("🪙 Алмази пулакӣ", callback_data="paid_diamond")],
            [InlineKeyboardButton("💎 Алмази бе пул", callback_data="free_diamond")],
            [InlineKeyboardButton("🔙 Назад", callback_data="go_back_to_start")]
        ]

        await query.edit_message_text("Офарин, бародар! Акнун интихоб кун:",
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "paid_diamond":
        await query.edit_message_text(f"Алоқа гир:\n📱 WhatsApp: {WHATSAPP_NUMBER}\n💬 Telegram: {TELEGRAM_USERNAME}")

    elif query.data == "free_diamond":
        ref_link = f"https://t.me/{BOT_USERNAME}?start=ref_{user_id}"
        user_referrals.setdefault(user_id, set())
        user_balances.setdefault(user_id, 0)

        keyboard = [
            [InlineKeyboardButton("📊 Баланс", callback_data="check_balance")],
            [InlineKeyboardButton("💵 Баровардани алмаз", callback_data="withdraw")]
        ]
        await query.edit_message_text(
            f"Ин реферал линки шумо аст:\n{ref_link}\n\nШумо метавонед онро ба дӯстонатон равон кунед, ва барои ҳар як обуначӣ 8 алмаз гиред.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "check_balance":
        count = len(user_referrals.get(user_id, []))
        balance = user_balances.get(user_id, 0)
        await query.edit_message_text(f"📊 Баланс: {balance} алмаз\n👥 Даъватҳо: {count} нафар")

    elif query.data == "withdraw":
        await query.edit_message_text(f"Барои гирифтани алмазҳо, бо {ADMIN_USERNAME} тамос гиред.")


async def referral_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    if args and args[0].startswith("ref_"):
        ref_id = int(args[0].split("_")[1])
        if ref_id != user_id:
            user_referrals.setdefault(ref_id, set()).add(user_id)
            user_balances[ref_id] = len(user_referrals[ref_id]) * 8
    await start(update, context)


app = ApplicationBuilder().token("7374942567:AAHJDEk5d4-FXCEoZut_pd7apFvpNQ7qx1s").build()
app.add_handler(CommandHandler("start", referral_entry))
app.add_handler(CallbackQueryHandler(button_handler))

print("Бот фаъол шуд!")
app.run_polling()
