import requests
from bs4 import BeautifulSoup
import telebot

api_token = 'SOME_API'
bot = telebot.TeleBot(api_token, parse_mode=None)

def get_first_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }

    url = "https://fighttime.ru/"
    req = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(req.text, 'lxml')

    b = []
    articles = soup.find('div', id="site").find_all('a', rel="bookmark")
    for item in range(30):
        item_url = articles[item].get('href')
        b.append(f'https://fighttime.ru{item_url}')
    hrefs = set(b)

    # -----------------------------------------
    data = []
    for content in hrefs:
        content_url = content
        reg = requests.get(url=content_url, headers=headers)
        sovp = BeautifulSoup(reg.text, 'lxml')

        Zagolovok = sovp.find('h1', class_="story-title entry-title").text
        Image = sovp.find('div', id="feat-img-reg").find('img').get('src')
        full_content = sovp.find('div', class_="itemFullText").find_all('blockquote')
        clear_content = []
        for a in full_content:
            clear_content.append(a.text.strip())

        korzina = {
            "title": Zagolovok,
            "image": f"https://fighttime.ru{Image}",
            "content": clear_content
        }
        data.append(korzina)
    return data


@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(message, "Hello")
    print("Hello")


@bot.message_handler(commands=["news"])
def send_content(message):
    
    data_base = get_first_news()
    v = 1
    for t in data_base:
        folder = t["image"]
        nachalo = f'{t["title"]}\n'
        obshee = f'\n{t["content"]}'
        form = nachalo + obshee
        bot.send_photo(message.chat.id, photo=folder)
        bot.send_message(message.chat.id, form)
        print(f"Итерация номер {v} завершена")
        v = v + 1

bot.infinity_polling()