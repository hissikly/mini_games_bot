import requests
import random
from bs4 import BeautifulSoup

words = ["толерантность", "эксгумация", "либерализм", "экспонат", "пышность", "скабрёзность", "шаловливость",
         "экспозиция", "индульгенция", "контрацептив", "шкворень", "эпиграф", "эпитафия", "барбекю", "жульен",
         "энцефалопатия", "парашютист", "импозантность", "индифферент", "демультипликатор", "педикулёз", "выхухоль",
         "россомаха", "сущность", "поэтапность", "напыщенность", "возвышенность"]

genres = {'Исторический': 'https://animego.org/anime/genre/historical',
          'Комедия': 'https://animego.org/anime/genre/comedy',
          'Сверхъестественное': 'https://animego.org/anime/genre/supernatural',
          'Сёнэн': 'https://animego.org/anime/genre/shounen', 'Экшен': 'https://animego.org/anime/genre/action',
          'Детектив': 'https://animego.org/anime/genre/mystery', 'Романтика': 'https://animego.org/anime/genre/romance',
          'Школа': 'https://animego.org/anime/genre/school', 'Драма': 'https://animego.org/anime/genre/drama',
          'Фантастика': 'https://animego.org/anime/genre/sci-fi', 'Гарем': 'https://animego.org/anime/genre/harem',
          'Военное': 'https://animego.org/anime/genre/military', 'Фэнтези': 'https://animego.org/anime/genre/fantasy',
          'Этти': 'https://animego.org/anime/genre/ecchi',
          'Повседневность': 'https://animego.org/anime/genre/slice-of-life',
          'Рейтинг': 'https://animego.org/anime?sort=r.rating&direction=desc'}
genre = ['Исторический', 'Комедия', 'Сверхъестественное', 'Сёнэн', 'Экшен', 'Детектив', 'Романтика', 'Школа', 'Драма',
         'Фантастика', 'Гарем', 'Военное', 'Фэнтези', 'Этти', 'Повседневность', 'Рейтинг']

urls = {}


def display_hangman(tries, word):
    stages = [
        'https://sun9-21.userapi.com/impf/c629430/v629430905/70e3/0OiskJRPjmE.jpg?size=512x512&quality=96&sign=6117340b804f7f624172f133e4d3f908&type=album',
        'https://sun9-18.userapi.com/impf/c629430/v629430905/70ea/7uPU1_zENpw.jpg?size=512x512&quality=96&sign=d91f2ec98be6ce2a8418f5710ae9bfee&type=album',
        'https://sun9-50.userapi.com/impf/c629430/v629430905/70f1/YY7kSVFxa7A.jpg?size=512x512&quality=96&sign=a4694cd5482915fc19a89d4f917285ff&type=album',
        'https://sun9-68.userapi.com/impf/c629430/v629430905/70f8/WTy-zRJTh1U.jpg?size=512x512&quality=96&sign=cc75f4a1109480a6342c80b803d17406&type=album',
        'https://sun9-41.userapi.com/impf/c629430/v629430905/70ff/BSt1-giVLPI.jpg?size=512x512&quality=96&sign=54c95c2c4b4266a0dc11d6a830982b1a&type=album',
        'https://sun9-63.userapi.com/impf/c629430/v629430905/7106/iBIG6iTXOKk.jpg?size=512x512&quality=96&sign=f2c2b639213549b4024834760f9e053f&type=album',
        'https://sun9-8.userapi.com/impf/c629430/v629430905/7114/UtPdWKjWjqk.jpg?size=512x512&quality=96&sign=1caa4076386ce06f4c44fdc4daf12622&type=album'
    ]
    return stages[tries]


def anime_lst(url):
    print(url)
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')
    lst = []
    for div in soup.find_all('div', class_='animes-list-item media'):
        lst.append(div.find('div', class_='h5 font-weight-normal mb-1').a.text)
        urls[div.find('div', class_='h5 font-weight-normal mb-1').a.text[:10]] = \
            div.find('div', class_='h5 font-weight-normal mb-1').a['href']
    return lst


def try_anime(html):
    try:
        isinstance(html, str)
        return html.text
    except:
        return 'Об это аниме мало информации:('


def get_anime_info(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'html.parser')
    name = try_anime(soup.find('div', class_='anime-title').div.h1)
    info = try_anime(soup.find('div', class_='description pb-3'))
    rating = try_anime(soup.find('span', class_='rating-value'))
    photo = soup.find('div', class_='anime-poster position-relative cursor-pointer')
    photo = photo.find_all('div')[1].img['src']
    return name, photo, info, rating, url


def news_lst():
    source = requests.get('https://chgtrk.ru/').text
    soup = BeautifulSoup(source, 'html.parser')
    lst = []
    for div in soup.find_all('div', class_="news-item__title"):
        lst.append(div.a.text + '\n' + 'https://chgtrk.ru/' + div.a['href'])
    random.shuffle(lst)
    return lst
