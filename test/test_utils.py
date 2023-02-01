import datetime
import random
import string
from common import konstante

def rand_str(length):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))


def rand_valid_user():
    return {
            "ime": rand_str(10),
            "prezime": rand_str(10),
            "korisnicko_ime": rand_str(10),
            "lozinka": rand_str(10),
            "email": f"{rand_str(10)}@email.com",
            "pasos": str(random.randint(100000000, 999999999)),
            "drzavljanstvo": rand_str(10),
            "telefon": str(random.randint(100000, 999999)),
            "pol": rand_str(10),
            "uloga": konstante.ULOGA_KORISNIK,
        }


def gen_rand_valid_users(num):
    for i in range(num):
        yield rand_valid_user()

def rand_datetime(**kwargs):
    start = datetime.datetime(2000, 1, 1) if "start" not in kwargs else kwargs["start"]
    end = datetime.datetime(2023, 12, 31) if "end" not in kwargs else kwargs["end"]
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)

def rand_date_str(**kwargs):
    start = datetime.date(2000, 1, 1) if "start" not in kwargs \
            else datetime.datetime.strptime(kwargs["start"], "%d.%m.%Y.").date()
    end = datetime.date(2023, 12, 31) if "end" not in kwargs \
        else datetime.datetime.strptime(kwargs["end"], "%d.%m.%Y.").date()
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    date = start + datetime.timedelta(seconds=random_second)
    return date.strftime("%d.%m.%Y.")

def rand_time_str():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return f"{hour:0>2}:{minute:0>2}"

def rand_seat_positions():
    start = ord('A')
    # Dodaje se 1 da bi se izbegao slučaj gde je prazan red
    end = 1 + random.randint(ord('A'), ord('H'))
    return [chr(c) for c in range(start, end)]


def rand_date(**kwargs):
    start = datetime.date(2000, 1, 1) if "start" not in kwargs \
            else datetime.datetime.strptime(kwargs["start"], "%d.%m.%Y.").date()
    end = datetime.date(2023, 12, 31) if "end" not in kwargs \
        else datetime.datetime.strptime(kwargs["end"], "%d.%m.%Y.").date()
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    date = start + datetime.timedelta(seconds=random_second)
    return date


def rand_seat(max_row: int, max_col: int):
    row, col = rand_seat_coords(max_row, max_col)
    return f"{row}{col}"


def rand_seat_coords(max_row, max_col):
    return random.randint(ord('A'), ord('A')+max_col), random.randint(1, max_row)


def rand_valid_aerodrom():
    return {
        "skracenica": rand_str(3),
        "pun_naziv": rand_str(7),
        "grad": rand_str(7),
        "drzava": rand_str(7),
        }


def gen_rand_valid_aerodrom(num):
    for i in range(num):
        yield rand_valid_aerodrom()


def rand_valid_model_aviona():
    return {
        "naziv": rand_str(3),
        "broj_redova": random.randint(0,20),
        "pozicije_sedista": rand_seat_positions(),
        "id": random.randint(0,20),
    }


def gen_rand_valid_model_aviona(num):
    for i in range(num):
        yield rand_valid_model_aviona()


def rand_valid_konkretan_let():
    zauzetost = []
    for _ in range(3):
        zauzetost.append([False for _ in range(5)])
    return {
        "sifra": random.randint(0, 100),
        "broj_leta": rand_str(4),
        "datum_i_vreme_polaska": rand_datetime(),
        "datum_i_vreme_dolaska": rand_datetime(),
        "zauzetost": zauzetost}


def gen_rand_valid_konkretan_let(num):
    for i in range(num):
        yield rand_valid_konkretan_let()

def rand_datetime_end(**kwargs):
    start = datetime.date(2000, 1, 1) if "start" not in kwargs \
            else datetime.datetime.strptime(kwargs["start"], "%d.%m.%Y.").date()
    end = datetime.date(2023, 12, 31) if "end" not in kwargs \
        else datetime.datetime.strptime(kwargs["end"], "%d.%m.%Y.").date()
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)

    date = start + datetime.timedelta(seconds=random_second)
    dt = datetime.datetime.combine(date, datetime.datetime.min.time()) #islo je datetirme.fdatetime i izbacivalo je gresku
    return dt