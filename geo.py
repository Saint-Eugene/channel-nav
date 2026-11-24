import re

# Формат стран: «Русское название=English_Tag»
US_STATES = """Alabama Alaska Arizona Arkansas California Colorado Connecticut
Delaware Florida Georgia_US Hawaii Idaho Illinois Indiana Iowa Kansas Kentucky
Louisiana Maine Maryland Massachusetts Michigan Minnesota Mississippi Missouri
Montana Nebraska Nevada New_Hampshire New_Jersey New_Mexico New_York
North_Carolina North_Dakota Ohio Oklahoma Oregon Pennsylvania Rhode_Island
South_Carolina South_Dakota Tennessee Texas Utah Vermont Virginia
Washington_State West_Virginia Wisconsin Wyoming District_of_Columbia"""

CANADA = """Alberta British_Columbia Manitoba New_Brunswick
Newfoundland_and_Labrador Nova_Scotia Ontario Prince_Edward_Island Quebec
Saskatchewan Northwest_Territories Nunavut Yukon"""

MEXICO = """Aguascalientes Baja_California Baja_California_Sur Campeche Chiapas
Chihuahua Coahuila Colima Mexico_City Durango Guanajuato Guerrero Hidalgo
Jalisco State_of_Mexico Michoacan Morelos Nayarit Nuevo_Leon Oaxaca Puebla
Queretaro Quintana_Roo San_Luis_Potosi Sinaloa Sonora Tabasco Tamaulipas
Tlaxcala Veracruz Yucatan Zacatecas"""

CENTRAL_AMERICA_CARIBBEAN = """Антигуа и Барбуда=Antigua_and_Barbuda, Багамы=Bahamas,
Барбадос=Barbados, Белиз=Belize, Гаити=Haiti, Гватемала=Guatemala,
Гондурас=Honduras, Гренада=Grenada, Доминика=Dominica,
Доминиканская Республика=Dominican_Republic, Коста-Рика=Costa_Rica, Куба=Cuba,
Никарагуа=Nicaragua, Панама=Panama, Сальвадор=El_Salvador,
Сент-Винсент и Гренадины=Saint_Vincent_and_the_Grenadines,
Сент-Китс и Невис=Saint_Kitts_and_Nevis, Сент-Люсия=Saint_Lucia,
Тринидад и Тобаго=Trinidad_and_Tobago, Ямайка=Jamaica"""

SOUTH_AMERICA = """Аргентина=Argentina, Боливия=Bolivia, Бразилия=Brazil,
Венесуэла=Venezuela, Гайана=Guyana, Колумбия=Colombia, Парагвай=Paraguay,
Перу=Peru, Суринам=Suriname, Уругвай=Uruguay, Чили=Chile, Эквадор=Ecuador"""

EUROPE = """Албания=Albania, Андорра=Andorra, Австрия=Austria, Беларусь=Belarus,
Бельгия=Belgium, Босния и Герцеговина=Bosnia_and_Herzegovina, Болгария=Bulgaria,
Ватикан=Vatican_City, Великобритания=United_Kingdom, Венгрия=Hungary,
Германия=Germany, Греция=Greece, Дания=Denmark, Ирландия=Ireland,
Исландия=Iceland, Испания=Spain, Италия=Italy, Кипр=Cyprus, Косово=Kosovo,
Латвия=Latvia, Литва=Lithuania, Лихтенштейн=Liechtenstein,
Люксембург=Luxembourg, Мальта=Malta, Молдова=Moldova, Монако=Monaco,
Нидерланды=Netherlands, Норвегия=Norway, Польша=Poland, Португалия=Portugal,
Россия=Russia, Румыния=Romania, Сан-Марино=San_Marino,
Северная Македония=North_Macedonia, Сербия=Serbia, Словакия=Slovakia,
Словения=Slovenia, Украина=Ukraine, Финляндия=Finland, Франция=France,
Хорватия=Croatia, Черногория=Montenegro, Чехия=Czechia,
Швейцария=Switzerland, Швеция=Sweden, Эстония=Estonia"""

ASIA = """Азербайджан=Azerbaijan, Армения=Armenia, Афганистан=Afghanistan,
Бангладеш=Bangladesh, Бахрейн=Bahrain, Бруней=Brunei, Бутан=Bhutan,
Вьетнам=Vietnam, Грузия=Georgia, Израиль=Israel, Индия=India,
Индонезия=Indonesia, Иордания=Jordan, Ирак=Iraq, Иран=Iran, Йемен=Yemen,
Казахстан=Kazakhstan, Камбоджа=Cambodia, Катар=Qatar, Кувейт=Kuwait,
Кыргызстан=Kyrgyzstan, Китай=China, КНДР=North_Korea, Лаос=Laos,
Ливан=Lebanon, Малайзия=Malaysia, Мальдивы=Maldives, Монголия=Mongolia,
Мьянма=Myanmar, Непал=Nepal, ОАЭ=United_Arab_Emirates, Оман=Oman,
Пакистан=Pakistan, Палестина=Palestine, Саудовская Аравия=Saudi_Arabia,
Сингапур=Singapore, Сирия=Syria, Таджикистан=Tajikistan, Таиланд=Thailand,
Тайвань=Taiwan, Тимор-Лесте=Timor_Leste, Туркменистан=Turkmenistan,
Турция=Turkey, Узбекистан=Uzbekistan, Филиппины=Philippines,
Шри-Ланка=Sri_Lanka, Южная Корея=South_Korea, Япония=Japan"""

AFRICA = """Алжир=Algeria, Ангола=Angola, Бенин=Benin, Ботсвана=Botswana,
Буркина-Фасо=Burkina_Faso, Бурунди=Burundi, Габон=Gabon, Гамбия=Gambia,
Гана=Ghana, Гвинея=Guinea, Гвинея-Бисау=Guinea_Bissau, Джибути=Djibouti,
ДР Конго=DR_Congo, Египет=Egypt, Замбия=Zambia, Зимбабве=Zimbabwe,
Кабо-Верде=Cabo_Verde, Камерун=Cameroon, Кения=Kenya, Коморы=Comoros,
Конго=Republic_of_the_Congo, Кот-д’Ивуар=Cote_d_Ivoire, Лесото=Lesotho,
Либерия=Liberia, Ливия=Libya, Маврикий=Mauritius, Мавритания=Mauritania,
Мадагаскар=Madagascar, Малави=Malawi, Мали=Mali, Марокко=Morocco,
Мозамбик=Mozambique, Намибия=Namibia, Нигер=Niger, Нигерия=Nigeria,
Руанда=Rwanda, Сан-Томе и Принсипи=Sao_Tome_and_Principe, Сенегал=Senegal,
Сейшелы=Seychelles, Сомали=Somalia, Судан=Sudan, Сьерра-Леоне=Sierra_Leone,
Танзания=Tanzania, Того=Togo, Тунис=Tunisia, Уганда=Uganda,
ЦАР=Central_African_Republic, Чад=Chad, Экваториальная Гвинея=Equatorial_Guinea,
Эритрея=Eritrea, Эсватини=Eswatini, Эфиопия=Ethiopia, ЮАР=South_Africa,
Южный Судан=South_Sudan"""

OCEANIA = """Австралия=Australia, Вануату=Vanuatu, Кирибати=Kiribati,
Маршалловы Острова=Marshall_Islands, Микронезия=Micronesia, Науру=Nauru,
Новая Зеландия=New_Zealand, Палау=Palau, Папуа — Новая Гвинея=Papua_New_Guinea,
Самоа=Samoa, Соломоновы Острова=Solomon_Islands, Тонга=Tonga, Тувалу=Tuvalu,
Фиджи=Fiji"""


def parse(s):
    out = {}
    for item in s.replace("\n", " ").split(","):
        if "=" in item:
            ru, en = item.split("=")
            out[ru.strip()] = "#" + en.strip()
    return out


def subdivisions(s):
    return {re.sub(r"_(US|State)$", "", t).replace("_", " "): "#" + t for t in s.split()}


def continent(tag, countries, extra=None):
    d = {"_tag": tag, **parse(countries)}
    d.update(extra or {})
    return d


TREE = {
    "Северная Америка": continent("#North_America", CENTRAL_AMERICA_CARIBBEAN, {
        "Канада": {"_tag": "#Canada", **subdivisions(CANADA)},
        "Мексика": {"_tag": "#Mexico", **subdivisions(MEXICO)},
        "США": {"_tag": "#usa", **subdivisions(US_STATES)},
    }),
    "Южная Америка": continent("#South_America", SOUTH_AMERICA),
    "Европа": continent("#Europe", EUROPE),
    "Азия": continent("#Asia", ASIA),
    "Африка": continent("#Africa", AFRICA),
    "Австралия и Океания": continent("#Oceania", OCEANIA),
}
