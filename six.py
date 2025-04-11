import pdfplumber
import telebot

BOT_TOKEN = "7643692092:AAFTFpcki0WBrFYiA3R4osugjFur8RImz28"
bot = telebot.TeleBot(BOT_TOKEN)

# وظيفة استخراج البيانات من PDF
def extract_table_from_pdf(pdf_path):
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                data.extend(table)
    return data

# وظيفة البحث عن الطالب وإرجاع نتيجته
def search_student(name, pdf_path):
    table_data = extract_table_from_pdf(pdf_path)
    
    for row in table_data:
        if name in row:
            return f"نتيجة {name}: {row}"
    
    return "الطالب غير موجود في السجل."

# عند استقبال الاسم من المستخدم
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "أهلاً! أرسل الاسم الرباعي للبحث عن نتيجته.")

@bot.message_handler(func=lambda msg: True)
def handle_query(message):
    name = message.text.strip()
    pdf_file_path = "namee.pdf"
    result = search_student(name, pdf_file_path)
    bot.reply_to(message, result)

# تشغيل البوت
bot.polling()
