from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# ====== CONFIG (EDIT THESE) ======
BOT_TOKEN = "8283657749:AAHL9nxFvQ2Ksm1GS8hU_IwScgpbVCQC-RI"
ADMIN_ID = 6338370995
PACK_LINK = "https://www.mediafire.com/file/ndni2qoeomvmfyg/XTOXIC_%25E2%2582%25B999_PACK.zip/file"
# =================================

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Submit Payment Proof", callback_data="pay")]]
    await update.message.reply_text(
        "Welcome to XTOXIC Packs 🔥\n\n"
        "Step 1️⃣ Pay ₹99 via QR\n"
        "Step 2️⃣ Send UTR\n"
        "Step 3️⃣ Get pack after verification\n\n"
        "⚠️ Fake proofs = rejected",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_data[query.from_user.id] = {}
    await query.message.reply_text("Please enter your UPI Transaction ID (UTR):")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    if uid not in user_data:
        return
    user_data[uid]["utr"] = update.message.text
    await update.message.reply_text("Now upload payment screenshot (optional but recommended):")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id
    if uid not in user_data:
        return

    utr = user_data[uid]["utr"]
    username = update.message.from_user.username

    caption = (
        f"🧾 New Payment Proof\n\n"
        f"User: @{username}\n"
        f"UTR: {utr}"
    )

    keyboard = [[
        InlineKeyboardButton("✅ Approve", callback_data=f"approve_{uid}"),
        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{uid}")
    ]]

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await update.message.reply_text("✅ Proof received. Please wait for verification.")

async def admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, uid = query.data.split("_")
    uid = int(uid)

    if action == "approve":
        await context.bot.send_message(
            chat_id=uid,
            text=f"✅ Payment Approved!\n\nHere is your pack:\n{PACK_LINK}\n\nThanks for supporting XTOXIC 🔥"
        )
        await query.message.edit_caption("✅ Approved")

    else:
        await context.bot