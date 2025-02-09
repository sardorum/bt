import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Tokenni o'zingizning bot tokeningizga almashtiring
TOKEN = "7925929707:AAE_NeRoegYWfIIqW-g0NQfaNnljIG0tijE"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Logger qo'shamiz
logging.basicConfig(level=logging.INFO)

# 500 ta savol va javoblar
questions = [
    {"savol": "O‘zbekiston poytaxti qaysi shahar?", "javob": "Toshkent", "variantlar": ["Samarqand", "Buxoro", "Toshkent", "Andijon"]},
    {"savol": "Yerning sun’iy yo‘ldoshi nima?", "javob": "Oy", "variantlar": ["Mars", "Oy", "Yupiter", "Venera"]},
    {"savol": "Eng katta okean qaysi?", "javob": "Tinch okeani", "variantlar": ["Atlantika", "Hind", "Tinch okeani", "Shimoliy Muz"]},
    {"savol": "Tesla kompaniyasining asoschisi kim?", "javob": "Ilon Mask", "variantlar": ["Jeff Bezos", "Ilon Mask", "Bill Gates", "Steve Jobs"]},
    {"savol": "Dunyodagi eng baland tog‘ qaysi?", "javob": "Everest", "variantlar": ["Elbrus", "Everest", "Kilimanjaro", "Mak-Kinli"]},
    {"savol": "O‘zbekistonning mashhur shirinligi 'Navruz' uchun tayyorlanadigan milliy taom nima?", "javob": "Sumalak", "variantlar": ["Palov", "Norin", "Sumalak", "Manti"]},
    {"savol": "O‘zbekistonning milliy me’moriy yodgorligi 'Hazrat Imom Majmuasi' qaysi shaharda joylashgan?", "javob": "Toshkent", "variantlar": ["Samarqand", "Toshkent", "Namangan", "Andijon"]},
    {"savol": "Oqsoqolning boshidagi nechta tosh bor, agar u uchtasini tashlab yuborsa?", "javob": "Ikki tosh", "variantlar": ["Bir tosh", "Ikki tosh", "Uch tosh", "To'rtta tosh"]} ,
    {"savol": "Qaerda 'Yangi yil' avval boshlandi?", "javob": "Sharqda", "variantlar": ["Sharqda", "G‘arbda", "Shimolda", "Janubda"]} ,
    {"savol": "Qaysi hayvonning nomi birinchi boshlangan?", "javob": "Bug‘u", "variantlar": ["Bug‘u", "Suvqurbaqa", "To‘ng‘iz", "Chumchuq"]} ,
    {"savol": "Eng uzoq vaqtda tutilib turadigan gap nima?", "javob": "Sukunat", "variantlar": ["Kulgi", "Gap", "Sukunat", "Uyqu"]} ,
    {"savol": "Qaysi hayvon o‘z o‘rnida qoladi?", "javob": "Mol", "variantlar": ["Eshak", "Tulki", "Mol", "Mushuk"]} ,
    {"savol": "Qaysi o‘zbekcha so‘z doimo aqlni charxlaydi?", "javob": "Kitob", "variantlar": ["Kitob", "Radio", "Televizor", "Telefon"]} ,
    {"savol": "Qaysi shaharni dunyo bo‘ylab tanishadi, lekin u yerda hech kim yashamaydi?", "javob": "Xotira", "variantlar": ["Samarqand", "Buxoro", "Xotira", "Toshkent"]} ,
    {"savol": "Qaysi so‘zda uchta 'o' bor?", "javob": "Olov", "variantlar": ["Qovoq", "Olov", "Tomosha", "Osh"]} ,
    {"savol": "Qaysi hayvon doimo yolg‘iz yuradi?", "javob": "Tulk", "variantlar": ["Tulk", "Sher", "Ot", "Qoplon"]} ,
    {"savol": "Eng katta joyda nima joylashgan?", "javob": "Bo‘sh joy", "variantlar": ["Uy", "Do‘kon", "Bo‘sh joy", "Bozor"]} ,
    {"savol": "Qaerda butun dunyo harakatsiz qoladi?", "javob": "Xotira", "variantlar": ["Hayot", "Xotira", "Chuqur", "Ko‘z"]} ,
    {"savol": "Qaysi so‘zda uchta 's' bor?", "javob": "Assalom", "variantlar": ["Tennis", "Assalom", "Soss", "Sovuq"]} ,
    {"savol": "Qaysi hayvon bir vaqtning o‘zida uchadi va yuradi?", "javob": "Eshak", "variantlar": ["Ot", "It", "Eshak", "Echki"]} ,
    {"savol": "Qaerda suv to‘ldirish mumkin, lekin hech qachon kam emas?", "javob": "Daryo", "variantlar": ["Ko‘l", "Hovuz", "Daryo", "Chashma"]} ,
    {"savol": "Qaerda shamollar hech qachon to‘xtamaydi?", "javob": "Chorrahada", "variantlar": ["Chorrahada", "Bog‘da", "Uyda", "Hovlida"]} ,
    {"savol": "Qaerda quyosh chiqadi va botadi?", "javob": "Osmonda", "variantlar": ["Yerda", "Osmonda", "Dengizda", "Chorrahada"]} ,
    {"savol": "Qaysi joyda dengiz hech qachon suvsiz qolmaydi?", "javob": "Xayol", "variantlar": ["Daryo", "Ko‘l", "Xayol", "Chashma"]} ,
    {"savol": "Qaysi so‘z uchta 'q' bilan yoziladi?", "javob": "Qovoq", "variantlar": ["Quloq", "Qiyin", "Qovoq", "Qaldirg‘och"]} ,
    {"savol": "Qaerda olov hech qachon o‘chmaydi?", "javob": "Ko‘ngil", "variantlar": ["Uyda", "Ko‘ngil", "Bog‘da", "Dengizda"]} ,
    {"savol": "Qaysi so‘zda uchta 'b' bor?", "javob": "Boboqol", "variantlar": ["Boboqol", "Bobo", "Bubbik", "Balbob"]} ,
    {"savol": "Dunyodagi eng uzun daryo qaysi?", "javob": "Nil", "variantlar": ["Amazonka", "Nil", "Misisipi", "Yangtze"]} ,
    {"savol": "Yer yuzining nechta qismi suv bilan qoplangan?", "javob": "70%", "variantlar": ["50%", "60%", "70%", "80%"]} ,
    {"savol": "Qaysi davlat aholisi eng ko‘p?", "javob": "Xitoy", "variantlar": ["Hindiston", "Xitoy", "AQSh", "Indoneziya"]} ,
    {"savol": "Dunyodagi eng baland tog‘ qaysi?", "javob": "Everest", "variantlar": ["K2", "Everest", "Denali", "Makalu"]} ,
    {"savol": "Qaysi dengiz O‘zbekiston hududida joylashgan?", "javob": "Orol dengizi", "variantlar": ["Qora dengiz", "Orol dengizi", "Aral dengizi", "Kaspiy dengizi"]} ,
    {"savol": "Dunyodagi eng katta sahro qaysi?", "javob": "Sahroi Kabir", "variantlar": ["Gobi", "Kalahari", "Sahroi Kabir", "Arabiston sahrosi"]} ,
    {"savol": "Qaysi mamlakatning poytaxti Uashington?", "javob": "AQSh", "variantlar": ["Kanada", "Meksika", "AQSh", "Braziliya"]} ,
    {"savol": "Qaysi davlat 2020 yilda yozgi Olimpiada o‘yinlariga mezbonlik qilgan?", "javob": "Yaponiya", "variantlar": ["Yaponiya", "Braziliya", "Xitoy", "Angliya"]} ,
    {"savol": "Dunyodagi eng katta qit’a qaysi?", "javob": "Osiyo", "variantlar": ["Osiyo", "Afrika", "Yevropa", "Amerika"]} ,
    {"savol": "O‘zbekistonning rasmiy tili qaysi?", "javob": "O‘zbek tili", "variantlar": ["Rus tili", "Tojik tili", "O‘zbek tili", "Qirg‘iz tili"]} ,
    {"savol": "O‘zbekiston Respublikasi mustaqilligini qachon e’lon qilgan?", "javob": "1991 yil", "variantlar": ["1989 yil", "1991 yil", "1994 yil", "1998 yil"]} ,
    {"savol": "Dunyodagi eng katta ko‘l qaysi?", "javob": "Kaspiy dengizi", "variantlar": ["Kaspiy dengizi", "Baykal ko‘li", "Yuqori ko‘l", "Viktoriya ko‘li"]} ,
    {"savol": "Dunyodagi eng ko‘p aholisi bo‘lgan shahar qaysi?", "javob": "Tokyo", "variantlar": ["Shanghai", "Mumbai", "New York", "Tokyo"]} ,
    {"savol": "Yer kurrasida nechta qit’a bor?", "javob": "7", "variantlar": ["5", "6", "7", "8"]}
]
random.shuffle(questions)

# Foydalanuvchilar ma'lumotlari
players = {}

@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    chat_id = message.chat.id
    players[chat_id] = {"score": 0, "current_question": 0}
    total_players = len(players)
    await message.answer(
        "🎮 <b>Aqilni Sinov o‘yini boshlandi!</b> \n\n👥 Jami foydalanuvchilar: {}".format(total_players),
        parse_mode="HTML"
    )
    await ask_question(message)

async def ask_question(message):
    chat_id = message.chat.id
    player = players.get(chat_id)

    if player and player["current_question"] < len(questions):
        question_data = questions[player["current_question"]]
        savol = question_data["savol"]
        variantlar = question_data["variantlar"]
        
        keyboard = InlineKeyboardMarkup()
        for variant in variantlar:
            keyboard.add(InlineKeyboardButton(variant, callback_data=variant))
        
        progress = "🟩"    *    player["current_question"] +    "⬜"    *  (len(questions) - player["current_question"] - 5)
        
        await message.answer(
            f"❓ <b>{savol}</b>\n\n{progress}", parse_mode="HTML", reply_markup=keyboard
        )
    else:
        await message.answer("🎉 <b>Siz barcha savollarga to‘g‘ri javob berdingiz!</b> 👏", parse_mode="HTML")
        await message.answer("🏆 <b>TABRIKLAYMIZ!</b> Siz barcha savollarga to‘g‘ri javob berdingiz va o‘yinni muvaffaqiyatli yakunladingiz! 🎉", parse_mode="HTML")
        await end_game(message)

@dp.callback_query_handler(lambda call: True)
async def check_answer(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    player = players.get(chat_id)

    if player:
        current_question = player["current_question"]
        correct_answer = questions[current_question]["javob"]
        
        if call.data == correct_answer:
            player["score"] += 1
            player["current_question"] += 1
            await call.message.edit_text(f"✅ <b>To‘g‘ri javob!</b> 🎉", parse_mode="HTML")
            await ask_question(call.message)
        else:
            await call.message.edit_text(
                f"❌ <b>Noto‘g‘ri!</b> ✅ To‘g‘ri javob: <b>{correct_answer}</b>\n🎯 Siz {player['score']} ball to‘pladingiz.",
                parse_mode="HTML"
            )
            await end_game(call.message)

async def end_game(message):
    chat_id = message.chat.id
    players.pop(chat_id, None)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🔄 Qayta o‘ynash", callback_data="restart"))
    await message.answer("🔄 Qayta o‘ynash uchun pastdagi  start tugmasin bosin!", reply_markup=keyboard)

@dp.callback_query_handler(lambda call: call.data == "restart")
async def restart_game(call: types.CallbackQuery):
    await start_game(call.message)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)