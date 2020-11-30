import telebot
from telebot import types
from bs4 import BeautifulSoup
from urllib.request import urlopen
import psycopg2
import pycountry
import random
from validate_email import validate_email
import tmdbsimple as tmdb
from requests import get

tmdb.API_KEY = '68c876f1625913a48af726dd8b1fb00d'

# Genre IDs
ACTION = 28
ADVENTURE = 12
ANIMATION = 16
COMEDY = 35
CRIME = 80
DOCUMENTARY = 99
DRAMA = 18
FAMILY = 10751
FANTASY = 14
HISTORY = 36
HORROR = 27
MUSIC = 10402
MYSTERY = 9648
ROMANCE = 10749
SCIENCE_FICTION = 878
TV_MOVIE = 10770
THRILLER = 53
WAR = 10752
WESTERN = 37
############


conn = psycopg2.connect(database="kinobotDB",
                        user="postgres",
                        password="6001",
                        host="127.0.0.1",
                        port="5432"
                        )
cursor = conn.cursor()

bot = telebot.TeleBot('1396092736:AAFXQ1JiGeZRpsVhxG7eOGmCQ1jYQaFF21k')
user_dict = {}


class CurrentMovie:
    def __init__(self):
        self.id = None
        self.genre_ids = []


class QuerySettings:
    def __init__(self):
        self.country = None
        self.year = None
        self.rating = None

        self.action = None
        self.adventure = None
        self.animation = None
        self.comedy = None
        self.crime = None
        self.documentary = None
        self.drama = None
        self.family = None
        self.fantasy = None
        self.history = None
        self.horror = None
        self.music = None
        self.mystery = None
        self.romance = None
        self.science_fiction = None
        self.tv_movie = None
        self.thriller = None
        self.war = None
        self.western = None


class Movie:
    def __init__(self, movie_id, watched, enjoy):
        self.movie_id = movie_id
        self.watched = watched
        self.enjoy = enjoy


class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.name = None
        self.mail = None
        self.qSettings = QuerySettings()
        self.movies = []


@bot.message_handler(commands=['start'])
def start_message(message):
    mess = 'Привет! Выберите действия:\n' \
           '/registration - регистрация \n' \
           '/login - вход в аккаунт'

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/registration', '/login')

    bot.send_message(message.from_user.id, text=mess, reply_markup=keyboard)


@bot.message_handler(commands=['registration'])
def call_registration(message):
    user = User(message.chat.id)
    user_dict[message.chat.id] = user
    bot.send_message(message.chat.id, 'Давайте знакомиться!')
    ask_name(message.from_user.first_name, message)  # -----  call getting NAME


@bot.message_handler(commands=['login'])
def ask_login(message):
    bot.send_message(message.chat.id, 'Введите почту')
    bot.register_next_step_handler(message, login)


def login(message):
    # TEMPORARY
    bot.send_message(message.chat.id, 'В разработке')
    user = User(message.chat.id)
    user_dict[message.chat.id] = user
    #
    main_menu(message)


# ------------------------------------------------   GET THE NAME    ------------------------------------------------#

def ask_name(get_name, message):
    user = user_dict[message.chat.id]
    user.name = get_name
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = "Это ваше имя?\n" + user.name
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


def get_name(message):
    user = user_dict[message.chat.id]
    user.name = message.text
    ask_name(user.name, message)


# ------------------------------------------------   GETTING EMAIL   ------------------------------------------------#

def get_mail(message):
    user = user_dict[message.chat.id]
    user.mail = message.text
    if not validate_email(user.mail):
        msg = bot.reply_to(message, 'Эл.почта не верна. Ввведите повторно:')
        bot.register_next_step_handler(msg, get_mail)
        return
    ask_age(message)  # -----  call getting AGE


# ------------------------------------------------   GET AGE    ------------------------------------------------#

def ask_age(message):
    bot.send_message(message.chat.id, 'Сколько вам лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    user = user_dict[message.chat.id]
    user.age = message.text
    if not user.age.isdigit():
        msg = bot.reply_to(message, 'Возвраст должен быть числом. Сколько вам лет?')
        bot.register_next_step_handler(msg, get_age)
        return
    ask_genres(message)


# ------------------------------------------------   GET GENRES INFO ------------------------------------------------#

def ask_genres(message):
    bot.send_message(message.chat.id, 'Нашей интеллектуальной системе нужна калибровка. Оцените вашу '
                                      'заинтересованность определенными жанрами фильмов от 0 до 10. Как вы оцените '
                                      'жанр "Экшн"?')
    bot.register_next_step_handler(message, get_genres_action)


def get_genres_action(message):
    user = user_dict[message.chat.id]
    user.qSettings.action = message.text

    if not user.qSettings.action.isdigit() or int(user.qSettings.action) > 10 or int(user.qSettings.action) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_action)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Приключения"?')
    bot.register_next_step_handler(message, get_genres_adventure)


def get_genres_adventure(message):
    user = user_dict[message.chat.id]
    user.qSettings.adventure = message.text

    if not user.qSettings.action.isdigit() or int(user.qSettings.adventure) > 10 or int(user.qSettings.adventure) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_adventure)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Анимационные фильмы"?')
    bot.register_next_step_handler(message, get_genres_animation)


def get_genres_animation(message):
    user = user_dict[message.chat.id]
    user.qSettings.animation = message.text

    if not user.qSettings.action.isdigit() or int(user.qSettings.animation) > 10 or int(user.qSettings.animation) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_animation)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Комедия"?')
    bot.register_next_step_handler(message, get_genres_comedy)


def get_genres_comedy(message):
    user = user_dict[message.chat.id]
    user.qSettings.comedy = message.text

    if not user.qSettings.action.isdigit() or int(user.qSettings.comedy) > 10 or int(user.qSettings.comedy) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_comedy)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Криминал"?')
    bot.register_next_step_handler(message, get_genres_crime)


def get_genres_crime(message):
    user = user_dict[message.chat.id]
    user.qSettings.crime = message.text

    if not user.qSettings.crime.isdigit() or int(user.qSettings.crime) > 10 or int(user.qSettings.crime) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_crime)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Документальный"?')
    bot.register_next_step_handler(message, get_genres_documentary)


def get_genres_documentary(message):
    user = user_dict[message.chat.id]
    user.qSettings.documentary = message.text

    if not user.qSettings.documentary.isdigit() or int(user.qSettings.documentary) > 10 or int(
            user.qSettings.documentary) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_documentary)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Драма"?')
    bot.register_next_step_handler(message, get_genres_drama)


def get_genres_drama(message):
    user = user_dict[message.chat.id]
    user.qSettings.drama = message.text

    if not user.qSettings.drama.isdigit() or int(user.qSettings.drama) > 10 or int(
            user.qSettings.drama) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_drama)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Семейный"?')
    bot.register_next_step_handler(message, get_genres_family)


def get_genres_family(message):
    user = user_dict[message.chat.id]
    user.qSettings.family = message.text

    if not user.qSettings.family.isdigit() or int(user.qSettings.family) > 10 or int(
            user.qSettings.family) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_family)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Фэнтези"?')
    bot.register_next_step_handler(message, get_genres_fantasy)


def get_genres_fantasy(message):
    user = user_dict[message.chat.id]
    user.qSettings.fantasy = message.text

    if not user.qSettings.fantasy.isdigit() or int(user.qSettings.fantasy) > 10 or int(
            user.qSettings.fantasy) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_fantasy)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Исторический"?')
    bot.register_next_step_handler(message, get_genres_history)


def get_genres_history(message):
    user = user_dict[message.chat.id]
    user.qSettings.history = message.text

    if not user.qSettings.history.isdigit() or int(user.qSettings.history) > 10 or int(
            user.qSettings.history) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_history)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Хоррор"?')
    bot.register_next_step_handler(message, get_genres_horror)


def get_genres_horror(message):
    user = user_dict[message.chat.id]
    user.qSettings.horror = message.text

    if not user.qSettings.horror.isdigit() or int(user.qSettings.horror) > 10 or int(
            user.qSettings.horror) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_horror)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Музыкальный"?')
    bot.register_next_step_handler(message, get_genres_music)


def get_genres_music(message):
    user = user_dict[message.chat.id]
    user.qSettings.music = message.text

    if not user.qSettings.music.isdigit() or int(user.qSettings.music) > 10 or int(
            user.qSettings.music) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_music)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Мистика"?')
    bot.register_next_step_handler(message, get_genres_mystery)


def get_genres_mystery(message):
    user = user_dict[message.chat.id]
    user.qSettings.mystery = message.text

    if not user.qSettings.mystery.isdigit() or int(user.qSettings.mystery) > 10 or int(
            user.qSettings.mystery) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_mystery)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Романтический"?')
    bot.register_next_step_handler(message, get_genres_romance)


def get_genres_romance(message):
    user = user_dict[message.chat.id]
    user.qSettings.romance = message.text

    if not user.qSettings.romance.isdigit() or int(user.qSettings.romance) > 10 or int(
            user.qSettings.romance) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_romance)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Научная фантастика"?')
    bot.register_next_step_handler(message, get_genres_science_fiction)


def get_genres_science_fiction(message):
    user = user_dict[message.chat.id]
    user.qSettings.science_fiction = message.text

    if not user.qSettings.science_fiction.isdigit() or int(user.qSettings.science_fiction) > 10 or int(
            user.qSettings.science_fiction) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_science_fiction)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Телефильм" (фильм, созданный специально для демонстрации '
                                      'по сети телевизионного вещания?')
    bot.register_next_step_handler(message, get_genres_tv_movie)


def get_genres_tv_movie(message):
    user = user_dict[message.chat.id]
    user.qSettings.tv_movie = message.text

    if not user.qSettings.tv_movie.isdigit() or int(user.qSettings.tv_movie) > 10 or int(
            user.qSettings.tv_movie) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_tv_movie)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Триллер"?')
    bot.register_next_step_handler(message, get_genres_thriller)


def get_genres_thriller(message):
    user = user_dict[message.chat.id]
    user.qSettings.thriller = message.text

    if not user.qSettings.thriller.isdigit() or int(user.qSettings.thriller) > 10 or int(
            user.qSettings.thriller) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_thriller)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Военный"?')
    bot.register_next_step_handler(message, get_genres_war)


def get_genres_war(message):
    user = user_dict[message.chat.id]
    user.qSettings.war = message.text

    if not user.qSettings.war.isdigit() or int(user.qSettings.war) > 10 or int(
            user.qSettings.war) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_war)
        return
    bot.send_message(message.chat.id, 'Как вы оцените жанр "Вестерн"?')
    bot.register_next_step_handler(message, get_genres_western)


def get_genres_western(message):
    user = user_dict[message.chat.id]
    user.qSettings.western = message.text

    if not user.qSettings.western.isdigit() or int(user.qSettings.western) > 10 or int(
            user.qSettings.western) < 0:
        bot.reply_to(message, 'Оцените от 0 до 10. Ваша оценка?')
        bot.register_next_step_handler(message, get_genres_western)
        return

    bot.send_message(message.chat.id, 'Отлично. Калибровка пройдена!')
    main_menu(message)


# ------------------------------------------------   MAIN MENU    -----------------------------------#
def main_menu(message):
    mess = 'Главное меню. Выберите действия:\n' \
           '/suggest - получить рекомендацию фильма\n' \
           '/settings - настройки поиска\n' \
           '/stat - получить вашу статистику'

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/suggest', '/settings', '/stat')

    bot.send_message(message.from_user.id, text=mess, reply_markup=keyboard)


# ------------------------------------------------   SUGGESTION    -----------------------------------#
@bot.message_handler(commands=['suggest'])
def call_suggest(message):
    user = user_dict[message.chat.id]
    if user.qSettings.action is None:
        bot.send_message(message.chat.id, 'Вам нужно пройти калибровку!')
        main_menu(message)

    global ACTION, ADVENTURE, ANIMATION, COMEDY, CRIME, DOCUMENTARY, DRAMA, FAMILY, FANTASY, HISTORY, HORROR, MUSIC, \
        MYSTERY, ROMANCE, SCIENCE_FICTION, TV_MOVIE, THRILLER, WAR, WESTERN
    genres = [ACTION, ADVENTURE, ANIMATION, COMEDY, CRIME, DOCUMENTARY, DRAMA, FAMILY, FANTASY, HISTORY, HORROR, MUSIC,
              MYSTERY, ROMANCE, SCIENCE_FICTION, TV_MOVIE, THRILLER, WAR, WESTERN]

    genres_weights = [int(user.qSettings.action), int(user.qSettings.adventure), int(user.qSettings.animation),
                      int(user.qSettings.comedy), int(user.qSettings.crime), int(user.qSettings.documentary),
                      int(user.qSettings.drama), int(user.qSettings.family), int(user.qSettings.fantasy),
                      int(user.qSettings.history), int(user.qSettings.horror), int(user.qSettings.music),
                      int(user.qSettings.mystery), int(user.qSettings.romance), int(user.qSettings.science_fiction),
                      int(user.qSettings.tv_movie), int(user.qSettings.thriller), int(user.qSettings.war),
                      int(user.qSettings.western)]
    current_genre = random.choices(genres, genres_weights)
    if user.qSettings.country is not None:
        current_country = str(user.qSettings.country)
    if user.qSettings.year is not None:
        current_year = int(user.qSettings.year)
    if user.qSettings.rating is not None:
        current_rating = float(user.qSettings.rating)

    discover = tmdb.Discover()

    if user.qSettings.country is None and user.qSettings.year is None and user.qSettings.rating is None:
        discover.movie(with_genres=current_genre)

    if user.qSettings.country is not None and user.qSettings.year is None and user.qSettings.rating is None:
        discover.movie(with_genres=current_genre, region=current_country)

    if user.qSettings.country is None and user.qSettings.year is not None and user.qSettings.rating is None:
        discover.movie(with_genres=current_genre, region=current_year)

    if user.qSettings.country is None and user.qSettings.year is None and user.qSettings.rating is not None:
        discover.movie(with_genres=current_genre, region=current_rating)

    if user.qSettings.country is not None and user.qSettings.year is not None and user.qSettings.rating is None:
        discover.movie(with_genres=current_genre, region=current_country, year=current_year)

    if user.qSettings.country is not None and user.qSettings.year is None and user.qSettings.rating is not None:
        discover.movie(with_genres=current_genre, region=current_country, year=current_rating)

    if user.qSettings.country is None and user.qSettings.year is not None and user.qSettings.rating is not None:
        discover.movie(with_genres=current_genre, region=current_year, year=current_rating)

    if user.qSettings.country is not None and user.qSettings.year is not None and user.qSettings.rating is not None:
        discover.movie(with_genres=current_genre, region=current_country, year=current_year,
                       vote_average_gte=current_rating)

    print_suggestion(message, discover)


# ------------------------------------------------   PRINT SUGGESTION    -----------------------------------#
def print_suggestion(message, discover):
    user = user_dict[message.chat.id]
    current_movie = random.choice(discover.results)
    current_movie_id = current_movie['id']
    CurrentMovie.id = current_movie_id
    CurrentMovie.genre_ids = current_movie['genre_ids']
    for movie in user.movies:
        if movie.movie_id == current_movie_id:
            current_movie = random.choice(discover.results)
            current_movie_id = current_movie['id']

    # Image
    current_movie_for_picture = tmdb.Movies(current_movie_id)
    img = current_movie_for_picture.images()
    if img is not None:
        img_backdrops = img['posters']
        if len(img_backdrops) >= 2:
            img_path = img_backdrops[1]
            img_path2 = img_path['file_path']

            img_url_part = 'https://image.tmdb.org/t/p/w500'
            img_url = img_url_part + str(img_path2)
            bot.send_photo(message.chat.id, get(img_url).content)

    bot.send_message(message.chat.id, current_movie['title'])
    bot.send_message(message.chat.id, current_movie['release_date'])
    bot.send_message(message.chat.id, current_movie['overview'])
    mess = 'Вас заинтересовал этот фильм? Выберите действие:\n' \
           '/trash - не заинтересовало\n' \
           '/later - заинтересовало, посмотрю позже\n' \
           '/watched_trash - смотрел, не понравилось\n' \
           '/watched_nice - смотрел, понравилось!'

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/trash', '/later', '/watched_trash', '/watched_nice')

    bot.send_message(message.from_user.id, text=mess, reply_markup=keyboard)

    # ------------------------------------------------   TRASH MOVIE    -----------------------------------#
    @bot.message_handler(commands=['trash'])
    def call_trash(message):
        movie_id = CurrentMovie.id
        type_of_correction = 'decrease'
        watched = False
        enjoy = False
        bot.send_message(message.from_user.id, text='Мы запомним!')
        for genre_id in CurrentMovie.genre_ids:
            weights_correction(message, type_of_correction, genre_id)

        new_movie = Movie(movie_id, watched, enjoy)
        user.movies.append(new_movie)
        main_menu(message)

    # ------------------------------------------------   WATCH LATER MOVIE    -----------------------------------#
    @bot.message_handler(commands=['later'])
    def call_trash(message):
        movie_id = CurrentMovie.id
        type_of_correction = 'increase'
        watched = False
        enjoy = True
        bot.send_message(message.from_user.id, text='Хороший выбор, сохраним в список "Посмотреть позже"!')
        for genre_id in CurrentMovie.genre_ids:
            weights_correction(message, type_of_correction, genre_id)

        new_movie = Movie(movie_id, watched, enjoy)
        user.movies.append(new_movie)
        main_menu(message)

    # ---------------------------------------------   watched And its trash MOVIE    --------------------------------#
    @bot.message_handler(commands=['watched_trash'])
    def call_trash(message):
        movie_id = CurrentMovie.id
        type_of_correction = 'decrease'
        watched = True
        enjoy = False
        bot.send_message(message.from_user.id, text='Принято, больше не будем рекомендовать этот фильм!')
        for genre_id in CurrentMovie.genre_ids:
            weights_correction(message, type_of_correction, genre_id)

        new_movie = Movie(movie_id, watched, enjoy)
        user.movies.append(new_movie)
        main_menu(message)

    # ---------------------------------------------   watched And its nice MOVIE    --------------------------------#
    @bot.message_handler(commands=['watched_nice'])
    def call_trash(message):
        movie_id = CurrentMovie.id
        type_of_correction = 'increase'
        watched = True
        enjoy = True
        bot.send_message(message.from_user.id, text='Рады, что вам понравилось, будем рекомендовать вам больше '
                                                    'фильмов в этом жанре!')
        for genre_id in CurrentMovie.genre_ids:
            print(genre_id)
            weights_correction(message, type_of_correction, genre_id)

        new_movie = Movie(movie_id, watched, enjoy)
        user.movies.append(new_movie)
        main_menu(message)


# ------------------------------------------------   WEIGHTS CORRECTION    -----------------------------------#

def weights_correction(message, type_of_correction, genre_id):
    user = user_dict[message.chat.id]
    if type_of_correction == 'decrease':
        correct_value = -1

    if type_of_correction == 'increase':
        correct_value = 1

    if genre_id == ACTION:
        if not int(user.qSettings.action) > 9 and not int(user.qSettings.action) < 1:
            user.qSettings.action = int(user.qSettings.action) + correct_value

    if genre_id == ADVENTURE:
        if not int(user.qSettings.adventure) > 9 and not int(user.qSettings.adventure) < 1:
            user.qSettings.adventure = int(user.qSettings.adventure) + correct_value

    if genre_id == ANIMATION:
        if not int(user.qSettings.animation) > 9 and not int(user.qSettings.animation) < 1:
            user.qSettings.animation = int(user.qSettings.animation) + correct_value

    if genre_id == COMEDY:
        if not int(user.qSettings.comedy) > 9 and not int(user.qSettings.comedy) < 1:
            user.qSettings.comedy = int(user.qSettings.comedy) + correct_value

    if genre_id == CRIME:
        if not int(user.qSettings.crime) > 9 and not int(user.qSettings.adventure) < 1:
            user.qSettings.adventure = int(user.qSettings.adventure) + correct_value

    if genre_id == DOCUMENTARY:
        if not int(user.qSettings.documentary) > 9 and not int(user.qSettings.documentary) < 1:
            user.qSettings.documentary = int(user.qSettings.documentary) + correct_value

    if genre_id == DRAMA:
        if not int(user.qSettings.drama) > 9 and not int(user.qSettings.drama) < 1:
            user.qSettings.drama = int(user.qSettings.drama) + correct_value

    if genre_id == FAMILY:
        if not int(user.qSettings.family) > 9 and not int(user.qSettings.family) < 1:
            user.qSettings.family = int(user.qSettings.family) + correct_value

    if genre_id == FANTASY:
        if not int(user.qSettings.fantasy) > 9 and not int(user.qSettings.fantasy) < 1:
            user.qSettings.fantasy = int(user.qSettings.fantasy) + correct_value

    if genre_id == HISTORY:
        if not int(user.qSettings.history) > 9 and not int(user.qSettings.history) < 1:
            user.qSettings.history = int(user.qSettings.history) + correct_value

    if genre_id == HORROR:
        if not int(user.qSettings.horror) > 9 and not int(user.qSettings.horror) < 1:
            user.qSettings.horror = int(user.qSettings.horror) + correct_value

    if genre_id == MUSIC:
        if not int(user.qSettings.music) > 9 and not int(user.qSettings.music) < 1:
            user.qSettings.music = int(user.qSettings.music) + correct_value

    if genre_id == MYSTERY:
        if not int(user.qSettings.mystery) > 9 and not int(user.qSettings.mystery) < 1:
            user.qSettings.mystery = int(user.qSettings.mystery) + correct_value

    if genre_id == ROMANCE:
        if not int(user.qSettings.romance) > 9 and not int(user.qSettings.romance) < 1:
            user.qSettings.romance = int(user.qSettings.romance) + correct_value

    if genre_id == SCIENCE_FICTION:
        if not int(user.qSettings.science_fiction) > 9 and not int(user.qSettings.science_fiction) < 1:
            user.qSettings.science_fiction = int(user.qSettings.science_fiction) + correct_value

    if genre_id == TV_MOVIE:
        if not int(user.qSettings.tv_movie) > 9 and not int(user.qSettings.tv_movie) < 1:
            user.qSettings.tv_movie = int(user.qSettings.tv_movie) + correct_value

    if genre_id == THRILLER:
        if not int(user.qSettings.thriller) > 9 and not int(user.qSettings.thriller) < 1:
            user.qSettings.thriller = int(user.qSettings.thriller) + correct_value

    if genre_id == WAR:
        if not int(user.qSettings.war) > 9 and not int(user.qSettings.war) < 1:
            user.qSettings.war = int(user.qSettings.war) + correct_value

    if genre_id == WESTERN:
        if not int(user.qSettings.western) > 9 and not int(user.qSettings.western) < 1:
            user.qSettings.western = int(user.qSettings.western) + correct_value

    return


# ------------------------------------------------   STATISTICS    -----------------------------------#
@bot.message_handler(commands=['stat'])
def call_stat(message):
    mess = 'Что вы хотите узнать?. Выберите действие:\n' \
           '/watch_later_list - список фильмов "Посмотреть позже"\n' \
           '/watched_list - список просмотренных фильмов\n' \
           '/trash_list - список непонравившихся фильмов\n' \
           '/nice_list - список непонравившихся фильмов\n' \
           '/query_settings_list - показать текущие параметры поиска\n' \
           '/menu - вернуться в меню'

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    bot.send_message(message.from_user.id, text=mess, reply_markup=keyboard)


# ------------------------------------------------   WATCH LATER LIST    -----------------------------------#

@bot.message_handler(commands=['watch_later_list'])
def watch_later_list(message):
    user = user_dict[message.chat.id]
    movie_list = 'Список "Посмотреть позже":\n'

    for movie in user.movies:
        if movie.watched is False and movie.enjoy is True:
            query_results = tmdb.Movies(movie.movie_id)
            query_results.info()
            current_movie = query_results.title
            print(current_movie)
            movie_list = movie_list + current_movie + '\n'
    bot.send_message(message.chat.id, movie_list)
    call_stat(message)


# ------------------------------------------------   WATCHED LIST    -----------------------------------#

@bot.message_handler(commands=['watched_list'])
def watched_list(message):
    user = user_dict[message.chat.id]
    movie_list = 'Список просмотренных фильмов:\n'

    for movie in user.movies:
        if movie.watched is True:
            query_results = tmdb.Movies(movie.movie_id)
            query_results.info()
            current_movie = query_results.title
            print(current_movie)
            movie_list = movie_list + current_movie + '\n'
    bot.send_message(message.chat.id, movie_list)
    call_stat(message)


# ------------------------------------------------   TRASH LIST    -----------------------------------#

@bot.message_handler(commands=['trash_list'])
def trash_list(message):
    user = user_dict[message.chat.id]
    movie_list = 'Список непонравившихся фильмов:\n'

    for movie in user.movies:
        if movie.enjoy is False:
            query_results = tmdb.Movies(movie.movie_id)
            query_results.info()
            current_movie = query_results.title
            print(current_movie)
            movie_list = movie_list + current_movie + '\n'
    bot.send_message(message.chat.id, movie_list)
    call_stat(message)


# ------------------------------------------------   Nice LIST    -----------------------------------#

@bot.message_handler(commands=['nice_list'])
def nice_list(message):
    user = user_dict[message.chat.id]
    movie_list = 'Список понравившихся фильмов:\n'

    for movie in user.movies:
        if movie.enjoy is True:
            query_results = tmdb.Movies(movie.movie_id)
            query_results.info()
            current_movie = query_results.title
            print(current_movie)
            movie_list = movie_list + current_movie + '\n'
    bot.send_message(message.chat.id, movie_list)
    call_stat(message)


# ------------------------------------------------   QUERY SETTINGS LIST    -----------------------------------#

@bot.message_handler(commands=['query_settings_list'])
def query_settings_list(message):
    user = user_dict[message.chat.id]
    answer = 'Текущие параметры поиска:\n'
    year = 'Год: ' + str(user.qSettings.year) + '\n'
    country = 'Страна: ' + str(user.qSettings.country) + '\n'
    rating = 'Минимальный рейтинг: ' + str(user.qSettings.rating) + '\n' + '\n'

    genres_stat = 'Рейтинг жанров: ' + '\n' \
                  + 'Экшн: ' + str(user.qSettings.action) + '\n' \
                  + 'Приключения: ' + str(user.qSettings.adventure) + '\n' \
                  + 'Анимация: ' + str(user.qSettings.animation) + '\n' \
                  + 'Комедия: ' + str(user.qSettings.comedy) + '\n' \
                  + 'Криминал: ' + str(user.qSettings.crime) + '\n' \
                  + 'Документальный: ' + str(user.qSettings.documentary) + '\n' \
                  + 'Драма: ' + str(user.qSettings.drama) + '\n' \
                  + 'Семейный: ' + str(user.qSettings.family) + '\n' \
                  + 'Фэнтази: ' + str(user.qSettings.fantasy) + '\n' \
                  + 'Исторический: ' + str(user.qSettings.history) + '\n' \
                  + 'Хоррор: ' + str(user.qSettings.horror) + '\n' \
                  + 'Музыкальный: ' + str(user.qSettings.music) + '\n' \
                  + 'Мистика: ' + str(user.qSettings.mystery) + '\n' \
                  + 'Романтический: ' + str(user.qSettings.romance) + '\n' \
                  + 'Научная фантастика: ' + str(user.qSettings.science_fiction) + '\n' \
                  + 'ТВ-шоу: ' + str(user.qSettings.tv_movie) + '\n' \
                  + 'Триллер: ' + str(user.qSettings.thriller) + '\n' \
                  + 'Военный: ' + str(user.qSettings.war) + '\n' \
                  + 'Вестерн: ' + str(user.qSettings.western)

    answer = answer + year + country + rating + genres_stat

    bot.send_message(message.chat.id, answer)
    call_stat(message)


# ------------------------------------------------   CALIBRATION    -----------------------------------#
@bot.message_handler(commands=['calibration'])
def call_calibration(message):
    ask_genres(message)


# ------------------------------------------------   SETTINGS    -----------------------------------#
@bot.message_handler(commands=['settings'])
def call_settings(message):
    mess = 'Настройки подбора фильмов. Выберите действия:\n' \
           '/country - установить страну производства\n' \
           '/year - установить дату производства\n' \
           '/rating - установить минимальный рейтинг\n' \
           '/reset - сбросить настройки страны, даты и рейтинга\n' \
           '/calibration - повторная калибровка по интересу к жанрам\n' \
           '/menu - вернуться в меню'

    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('/country', '/year', '/rating', '/reset', '/calibration', '/menu')
    bot.send_message(message.from_user.id, text=mess, reply_markup=keyboard)


# ------------------------------------------------   COUNTRY    -----------------------------------#
@bot.message_handler(commands=['country'])
def ask_country(message):
    bot.send_message(message.chat.id, 'Введите страну производства фильмов на англ. (прим. Russian Federation, '
                                      'Brazil, Ukraine)')
    bot.register_next_step_handler(message, call_country)


def call_country(message):
    user = user_dict[message.chat.id]
    user.qSettings.country = pycountry.countries.get(name=message.text).alpha_2
    bot.send_message(message.chat.id, 'Принято!')
    call_settings(message)


# ------------------------------------------------   YEAR    -----------------------------------#
@bot.message_handler(commands=['year'])
def ask_year(message):
    bot.send_message(message.chat.id, 'Введите год производства фильма')
    bot.register_next_step_handler(message, call_year)


def call_year(message):
    user = user_dict[message.chat.id]
    user.qSettings.year = message.text
    if not user.qSettings.year.isdigit() or int(user.qSettings.year) < 1940:
        msg = bot.reply_to(message, 'Год должен быть числом, больше 1940. Введите год производства фильма')
        bot.register_next_step_handler(msg, call_year)
        return
    bot.send_message(message.chat.id, 'Принято!')
    call_settings(message)


# ------------------------------------------------   RATING    -----------------------------------#
@bot.message_handler(commands=['rating'])
def ask_rate(message):
    bot.send_message(message.chat.id, 'Введите минимально допустимый рейтинг фильма (от 0 до 10)')
    bot.register_next_step_handler(message, call_rate)


def call_rate(message):
    user = user_dict[message.chat.id]
    user.qSettings.rating = message.text
    if not user.qSettings.rating.isdigit() or int(user.qSettings.rating) > 10 or int(user.qSettings.rating) < 0:
        msg = bot.reply_to(message, 'Допускается только число от 0 до 10. Введите минимально допустимый рейтинг фильма')
        bot.register_next_step_handler(msg, call_rate)
        return
    bot.send_message(message.chat.id, 'Принято!')
    call_settings(message)


# ------------------------------------------------   RESET    -----------------------------------#
@bot.message_handler(commands=['reset'])
def call_reset(message):
    bot.send_message(message.chat.id, 'Настройки страны, даты и рейтинга сброшены')
    user = user_dict[message.chat.id]
    user.qSettings.country = None
    user.qSettings.year = None
    user.qSettings.rating = None
    call_settings(message)


# ------------------------------------------------   RETURN TO MENU    -----------------------------------#
@bot.message_handler(commands=['menu'])
def call_return_to_menu(message):
    main_menu(message)


# ------------------------------------------------   KEYBOARD UNDER MESSAGE    -----------------------------------#

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user = user_dict[call.message.chat.id]
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Отлично! Теперь ввведите свою почту')
        bot.register_next_step_handler(call.message, get_mail)  # ----- call to get mail

    if call.data == "no":
        bot.send_message(call.message.chat.id, "Как вас зовут?")
        bot.register_next_step_handler(call.message, get_name)


def print_hi(name):
    print(name)


if __name__ == '__main__':
    print_hi('BotStart')

bot.polling()
