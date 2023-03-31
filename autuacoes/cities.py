import csv
from functools import lru_cache

from pathlib import Path

from rows.fields import slug


CITY_DATA_FILENAME = Path(__file__).parent / "data" / "municipios.csv"
REGEXP_RS = re.compile("^RIO GRANDE DO SUL (.*)$")
STATE_NAMES = {
    "acre": "AC",
    "alagoas": "AL",
    "amapa": "AP",
    "amazonas": "AM",
    "bahia": "BA",
    "ceara": "CE",
    "distrito_federal": "DF",
    "espirito_santo": "ES",
    "goias": "GO",
    "maranhao": "MA",
    "mato_grosso": "MT",
    "mato_grosso_do_sul": "MS",
    "minas_gerais": "MG",
    "para": "PA",
    "pernambuco": "PE",
    "parana": "PR",
    "paraiba": "PB",
    "piaui": "PI",
    "rio_de_janeiro": "RJ",
    "rio_grande_do_norte": "RN",
    "rio_grande_do_sul": "RS",
    "rondonia": "RO",
    "roraima": "RR",
    "santa_catarina": "SC",
    "sao_paulo": "SP",
    "sergipe": "SE",
    "tocantins": "TO",
}
BLOCK_WORDS = ("da", "das", "de", "do", "dos", "e")
WORD_MAP = {
    "thome": "tome",
    "thome": "tome",
}
CITY_SPELL_MAP = {
    ("CE", "itapage"): "itapaje",
    ("MA", "governador_edson_lobao"): "governador_edison_lobao",
    ("MG", "brasopolis"): "brazopolis",
    ("MG", "dona_eusebia"): "dona_euzebia",
    ("MT", "poxoreo"): "poxoreu",
    ("PA", "santa_isabel_do_para"): "santa_izabel_do_para",
    ("PB", "serido"): "junco_do_serido",
    ("PE", "iguaraci"): "iguaracy",
    ("RJ", "parati"): "paraty",
    ("RJ", "trajano_de_morais"): "trajano_de_moraes",
    ("RN", "assu"): "acu",  # Açu
    ("SC", "passos_de_torres"): "passo_de_torres",
    ("SC", "picarras"): "balneario_picarras",
    ("SC", "presidente_castelo_branco"): "presidente_castello_branco",
    ("SE", "gracho_cardoso"): "graccho_cardoso",
    ("SP", "florinia"): "florinea",
    ("SP", "moji_mirim"): "mogi_mirim",
    ("SP", "sao_luis_do_paraitinga"): "sao_luiz_do_paraitinga",
    ("TO", "fortaleza_do_tabocao"): "tabocao",
    ("TO", "sao_valerio_da_natividade"): "sao_valerio",
}


@lru_cache(maxsize=1)
def read_state_codes():
    with CITY_DATA_FILENAME.open() as fobj:
        return {row["city_ibge_code"][:2]: row["state"] for row in csv.DictReader(fobj)}


@lru_cache(maxsize=5570 * 2)
def city_key(state, city):
    state, city = state.upper().strip(), slug(city).replace("sant_ana", "santana")
    city = CITY_SPELL_MAP.get((state, city), city)
    city = " ".join(
        WORD_MAP.get(word, word)
        for word in city.split("_")
        if word not in BLOCK_WORDS
    )
    return slug(state + " " + city)


@lru_cache(maxsize=5570 * 2)
def split_state_city(text):
    words = text.split()
    if len(words[0]) == 2:  # State acronym
        return words[0], " ".join(words[1:])

    else:  # This row has full state name
        for index, _ in enumerate(words, start=1):
            key = slug(" ".join(words[:index]))
            if key in STATE_NAMES:
                return STATE_NAMES[key], " ".join(words[index:])
        raise ValueError(f"Cannot recognize state/city: {text}")


@lru_cache(maxsize=1)
def city_map():
    with CITY_DATA_FILENAME.open() as fobj:
        reader = csv.DictReader(fobj)
        return {city_key(row["state"], row["city"]): row for row in reader}


@lru_cache(maxsize=5570 * 2)
def get_city(state, city):
    result_rs = REGEXP_RS.findall(city)
    if result_rs:
        state, city = 'RS', result_rs[0]
    elif "/" in city:
        city2, state2 = city.split("/")
        if state and state != state2:
            raise ValueError(f"Conflict in state for: {city}/{state}")
        city, state = city2, state2
    city = city_map().get(city_key(state, city))
    if city is None:
        raise ValueError(f"City/state {repr(city)}/{repr(state)} not found")
    return city["state"], city["city"], city["city_ibge_code"]


STATE_CODES = read_state_codes()
