import requests
from telebot import TeleBot, types, apihelper

proxy = {
    'https': 'https://free.shecan.ir/dns-query'  # For HTTPS
}

apihelper.proxy = proxy

bot = TeleBot('8155387502:AAG_4AyeKJvKEC-GQNahNFbaImP4XEr5Itk')
response = requests.get('https://www.karlancer.com/api/publics/category-page?q=python&order=newest')

projects = response.json()['data']['projects']['data']

user_contacts = set()

@bot.message_handler(commands=['start'])
def welcome(message):
    markup_info = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    info_btn = types.KeyboardButton('📞 Send Contact Info', request_contact=True)
    markup_info.add(info_btn)
    bot.send_message(message.chat.id, f'welcome to my bot {message.from_user.first_name}')
    bot.send_message(message.chat.id, f'please send contact info and then use bot for free :)', reply_markup=markup_info)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact.phone_number in user_contacts:
        bot.send_message(message.chat.id, 'You have already shared your contact info.')
    else:
        user_contacts.add(message.contact.phone_number)
        bot.send_message(message.chat.id, 'Thank you for sharing your contact info!')
        send_project_offer(message.chat.id)
def send_project_offer(chat_id):
    markup_data = types.InlineKeyboardMarkup()
    data_btn = types.InlineKeyboardButton('Get Latest Python Projects on Karlancer', callback_data='get_projects')
    markup_data.add(data_btn)
    bot.send_message(chat_id, 'Press the button below to get the latest Python projects on Karlancer:', reply_markup=markup_data)

@bot.callback_query_handler(func=lambda call: call.data == 'get_projects')
def send_project_data(call):
    bot.answer_callback_query(call.id, "Fetching the latest projects...")
    # Send project data here (for now, just a link)
    bot.send_message(call.message.chat.id,
                         'Here are the latest Python projects on Karlancer:')
    for project in projects:
        if 'روز' not in project['past_time']:
            bot.send_message(call.message.chat.id, f'''title:  {project["title"]}
            description:  {project["description"]}
            min_budget:  {project["min_budget"]} > max_budget:  {project["max_budget"]}
            url : {project['shortened_url']}
            passed time : {project["past_time"]}
            ''')

bot.polling()