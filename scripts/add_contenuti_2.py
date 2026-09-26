# -*- coding: utf-8 -*-
"""Aggiunge a knowledge.json i contenuti del secondo blocco di novità:

- letture          racconti brevi A1 con glossario e domande di comprensione
- glossarioLetture parole frequenti (pronomi, preposizioni…) per il tocco-traduzione
- proverbi         proverbi russi con traduzione letterale e equivalente italiano
- cultura          «Russia in pillole»: schede di cultura con le loro parole
- falsiAmici       parole russe che sembrano italiane ma non lo sono
- paroleGemelle    parole russe che si capiscono al volo
- casiNomi         forme dei nomi usati negli esercizi sui casi (sing.: nom gen dat acc str prep)
- casi             frasi con il buco per l'esercizio «Casi al volo»
- verbiMoto        teoria e frasi per идти/ходить/ехать/ездить
- percorso         il Percorso A1: tappe fatte di passi che rimandano agli esercizi

Idempotente: riscrive sempre le stesse chiavi. Uso: python scripts/add_contenuti_2.py
"""
import json, io, os

P = os.path.join(os.path.dirname(__file__), '..', 'knowledge.json')
with io.open(P, encoding='utf-8') as f:
    d = json.load(f)

# ---------------------------------------------------------------- LETTURE
def lettura(id, icona, titolo, titoloRu, livello, frasi, glossario, domande):
    return {
        "id": id, "icona": icona, "titolo": titolo, "titoloRu": titoloRu, "livello": livello,
        "frasi": [{"ru": ru, "it": it} for ru, it in frasi],
        "glossario": glossario,
        "domande": [{"q": q, "it": it, "ok": ok, "opts": opts} for q, it, ok, opts in domande],
    }

LETTURE = [
lettura("anna", "👩‍🏫", "Mi chiamo Anna", "Меня зовут Анна", 1, [
    ("Привет! Меня зовут Анна.", "Ciao! Mi chiamo Anna."),
    ("Я живу в Москве.", "Vivo a Mosca."),
    ("Мне двадцать пять лет.", "Ho venticinque anni."),
    ("Я работаю в школе. Я учительница.", "Lavoro in una scuola. Sono insegnante."),
    ("У меня есть брат и сестра.", "Ho un fratello e una sorella."),
    ("Мой брат Иван — врач.", "Mio fratello Ivan è medico."),
    ("Моя сестра Оля ещё учится в университете.", "Mia sorella Olja studia ancora all'università."),
    ("Вечером я читаю книги или гуляю в парке.", "La sera leggo libri o passeggio nel parco."),
    ("Я очень люблю кошек. У меня есть кошка Мурка.", "Amo molto i gatti. Ho una gatta, Murka."),
    ("А как тебя зовут?", "E tu come ti chiami?"),
], {
    "привет": "ciao", "зовут": "chiamano (меня зовут = mi chiamo)", "живу": "vivo (жить)", "москве": "Mosca (prepositivo)",
    "двадцать": "venti", "пять": "cinque", "лет": "anni (dopo i numeri)", "работаю": "lavoro (работать)",
    "школе": "scuola (prepositivo)", "учительница": "insegnante (f.)", "брат": "fratello", "сестра": "sorella",
    "врач": "medico", "учится": "studia (учиться)", "университете": "università (prepositivo)",
    "вечером": "la sera", "читаю": "leggo (читать)", "книги": "libri", "гуляю": "passeggio (гулять)",
    "парке": "parco (prepositivo)", "люблю": "amo (любить)", "кошек": "gatti (accusativo plurale)",
    "кошка": "gatta", "тебя": "te (accusativo)",
}, [
    ("Где живёт Анна?", "Dove vive Anna?", "В Москве", ["В Петербурге", "В Риме"]),
    ("Кем работает Анна?", "Che lavoro fa Anna?", "Учительницей", ["Врачом", "Студенткой"]),
    ("Кто Иван?", "Chi è Ivan?", "Её брат, врач", ["Её муж", "Её учитель"]),
    ("Как зовут кошку?", "Come si chiama la gatta?", "Мурка", ["Оля", "Анна"]),
]),
lettura("marco", "☕", "La mattina di Marco", "Утро Марко", 1, [
    ("Марко — итальянец. Он живёт в Петербурге.", "Marco è italiano. Vive a San Pietroburgo."),
    ("Каждое утро он встаёт в семь часов.", "Ogni mattina si alza alle sette."),
    ("Сначала он принимает душ.", "Prima fa la doccia."),
    ("Потом он завтракает: пьёт кофе и ест бутерброд.", "Poi fa colazione: beve un caffè e mangia un panino."),
    ("В восемь часов он идёт на работу.", "Alle otto va al lavoro."),
    ("Он работает в офисе недалеко от дома.", "Lavora in un ufficio non lontano da casa."),
    ("Обычно он ходит пешком, но когда идёт дождь, он едет на метро.", "Di solito va a piedi, ma quando piove prende la metro."),
    ("Днём он обедает в кафе с коллегами.", "A mezzogiorno pranza al bar con i colleghi."),
    ("Вечером он учит русский язык.", "La sera studia il russo."),
    ("Марко говорит: «Русский язык трудный, но очень красивый!»", "Marco dice: «Il russo è difficile, ma molto bello!»"),
], {
    "итальянец": "italiano (uomo)", "живёт": "vive (жить)", "петербурге": "San Pietroburgo (prepositivo)",
    "каждое": "ogni (n.)", "утро": "mattina", "встаёт": "si alza (вставать)", "семь": "sette", "часов": "ore (dopo 5+)",
    "сначала": "prima, all'inizio", "принимает": "prende (принимать душ = fare la doccia)", "душ": "doccia",
    "завтракает": "fa colazione", "пьёт": "beve (пить)", "кофе": "caffè", "ест": "mangia (есть)",
    "бутерброд": "panino, tartina", "восемь": "otto", "идёт": "va (a piedi, adesso)", "работу": "lavoro (accusativo)",
    "работает": "lavora", "офисе": "ufficio (prepositivo)", "недалеко": "non lontano", "дома": "casa (genitivo) / a casa",
    "обычно": "di solito", "ходит": "va (a piedi, di solito)", "пешком": "a piedi", "дождь": "pioggia (идёт дождь = piove)",
    "едет": "va (con un mezzo)", "метро": "metro", "днём": "di giorno, a mezzogiorno", "обедает": "pranza",
    "кафе": "bar, caffè", "коллегами": "colleghi (strumentale)", "учит": "studia, impara", "русский": "russo",
    "язык": "lingua", "говорит": "dice, parla", "трудный": "difficile", "красивый": "bello",
}, [
    ("Во сколько встаёт Марко?", "A che ora si alza Marco?", "В семь часов", ["В восемь часов", "В десять часов"]),
    ("Что он пьёт утром?", "Cosa beve la mattina?", "Кофе", ["Чай", "Сок"]),
    ("Как он едет на работу, когда идёт дождь?", "Come va al lavoro quando piove?", "На метро", ["Пешком", "На такси"]),
    ("Что он делает вечером?", "Cosa fa la sera?", "Учит русский язык", ["Смотрит футбол", "Работает в офисе"]),
]),
lettura("mercato", "🥕", "Al mercato", "На рынке", 1, [
    ("Сегодня суббота. Бабушка Нина идёт на рынок.", "Oggi è sabato. Nonna Nina va al mercato."),
    ("На рынке много людей.", "Al mercato c'è molta gente."),
    ("Там продают овощи, фрукты, мясо и рыбу.", "Lì vendono verdura, frutta, carne e pesce."),
    ("Бабушка покупает картошку, морковь и капусту.", "La nonna compra patate, carote e cavolo."),
    ("Она хочет приготовить борщ.", "Vuole preparare il boršč."),
    ("Ещё она покупает килограмм яблок для внуков.", "Compra anche un chilo di mele per i nipoti."),
    ("Продавец говорит: «Яблоки очень сладкие!»", "Il venditore dice: «Le mele sono dolcissime!»"),
    ("Всё стоит пятьсот рублей.", "Tutto costa cinquecento rubli."),
    ("Дома бабушка готовит борщ весь день.", "A casa la nonna cucina il boršč tutto il giorno."),
    ("Вечером приходят внуки, и все вместе ужинают.", "La sera arrivano i nipoti e cenano tutti insieme."),
], {
    "сегодня": "oggi", "суббота": "sabato", "бабушка": "nonna", "рынок": "mercato", "рынке": "mercato (prepositivo)",
    "много": "molto, molti", "людей": "persone (genitivo plurale)", "продают": "vendono", "овощи": "verdure",
    "фрукты": "frutta", "мясо": "carne", "рыбу": "pesce (accusativo)", "покупает": "compra",
    "картошку": "patate (accusativo)", "морковь": "carote", "капусту": "cavolo (accusativo)", "хочет": "vuole",
    "приготовить": "preparare, cucinare", "борщ": "boršč (zuppa di barbabietole)", "килограмм": "chilo",
    "яблок": "mele (genitivo plurale)", "для": "per", "внуков": "nipoti (genitivo plurale)", "продавец": "venditore",
    "яблоки": "mele", "сладкие": "dolci", "стоит": "costa", "пятьсот": "cinquecento", "рублей": "rubli",
    "дома": "a casa", "готовит": "cucina, prepara", "весь": "tutto (m.)", "день": "giorno",
    "приходят": "arrivano, vengono", "внуки": "nipoti", "вместе": "insieme", "ужинают": "cenano",
}, [
    ("Какой сегодня день?", "Che giorno è oggi?", "Суббота", ["Понедельник", "Воскресенье"]),
    ("Что хочет приготовить бабушка?", "Cosa vuole preparare la nonna?", "Борщ", ["Пельмени", "Салат"]),
    ("Для кого яблоки?", "Per chi sono le mele?", "Для внуков", ["Для продавца", "Для соседки"]),
    ("Сколько всё стоит?", "Quanto costa tutto?", "Пятьсот рублей", ["Пятьдесят рублей", "Пять тысяч рублей"]),
]),
lettura("meteo", "❄️", "Il tempo a Mosca", "Погода в Москве", 1, [
    ("В Москве зима длинная и холодная.", "A Mosca l'inverno è lungo e freddo."),
    ("Часто идёт снег, и на улице минус пятнадцать.", "Nevica spesso e fuori ci sono meno quindici gradi."),
    ("Люди носят тёплые куртки, шапки и шарфы.", "La gente porta giacche calde, berretti e sciarpe."),
    ("Весной погода меняется: то солнце, то дождь.", "In primavera il tempo cambia: ora sole, ora pioggia."),
    ("Летом в Москве тепло, иногда даже жарко.", "D'estate a Mosca fa caldo, a volte perfino molto caldo."),
    ("Все гуляют в парках и едят мороженое.", "Tutti passeggiano nei parchi e mangiano il gelato."),
    ("Осенью деревья жёлтые и красные.", "In autunno gli alberi sono gialli e rossi."),
    ("Это очень красиво, но часто идёт дождь.", "È molto bello, ma piove spesso."),
    ("А какое время года любишь ты?", "E tu quale stagione preferisci?"),
], {
    "москве": "Mosca (prepositivo)", "зима": "inverno", "длинная": "lunga", "холодная": "fredda", "часто": "spesso", "снег": "neve (идёт снег = nevica)",
    "улице": "strada (на улице = fuori)", "минус": "meno", "пятнадцать": "quindici", "люди": "persone, gente",
    "носят": "portano, indossano", "тёплые": "calde", "куртки": "giacche", "шапки": "berretti", "шарфы": "sciarpe",
    "весной": "in primavera", "погода": "tempo (meteo)", "меняется": "cambia", "то": "ora… ora (то… то)",
    "солнце": "sole", "дождь": "pioggia", "летом": "d'estate", "тепло": "fa caldo (mite)", "иногда": "a volte",
    "даже": "perfino", "жарко": "fa molto caldo", "гуляют": "passeggiano", "парках": "parchi (prepositivo plurale)",
    "едят": "mangiano", "мороженое": "gelato", "осенью": "in autunno", "деревья": "alberi", "жёлтые": "gialli",
    "красные": "rossi", "красиво": "(è) bello", "какое": "quale (n.)", "время": "tempo (время года = stagione)",
    "года": "dell'anno", "любишь": "ami, preferisci (tu)",
}, [
    ("Какая зима в Москве?", "Com'è l'inverno a Mosca?", "Длинная и холодная", ["Короткая и тёплая", "Жаркая"]),
    ("Что люди делают летом?", "Cosa fa la gente d'estate?", "Гуляют в парках", ["Носят шапки", "Катаются на лыжах"]),
    ("Какие деревья осенью?", "Come sono gli alberi in autunno?", "Жёлтые и красные", ["Зелёные", "Белые"]),
]),
lettura("sasha", "🧑‍💻", "Il mio amico Saša", "Мой друг Саша", 1, [
    ("У меня есть друг. Его зовут Саша.", "Ho un amico. Si chiama Saša."),
    ("Саша высокий, у него короткие тёмные волосы и голубые глаза.", "Saša è alto, ha i capelli corti e scuri e gli occhi azzurri."),
    ("Он очень весёлый и добрый.", "È molto allegro e gentile."),
    ("Саша программист. Он работает дома за компьютером.", "Saša è programmatore. Lavora a casa al computer."),
    ("Он любит спорт: по утрам он бегает, а по субботам играет в футбол.", "Ama lo sport: la mattina corre e il sabato gioca a calcio."),
    ("Ещё он хорошо готовит. Его любимое блюдо — пельмени.", "Inoltre cucina bene. Il suo piatto preferito sono i pel'meni."),
    ("Саша не говорит по-итальянски, но хочет выучить язык.", "Saša non parla italiano, ma vuole impararlo."),
    ("Мы часто говорим по телефону: я помогаю ему с итальянским, а он мне — с русским.", "Parliamo spesso al telefono: io lo aiuto con l'italiano e lui aiuta me con il russo."),
], {
    "друг": "amico", "его": "lui / suo (di lui)", "зовут": "chiamano (его зовут = si chiama)", "высокий": "alto",
    "него": "lui (у него = lui ha)", "короткие": "corti", "тёмные": "scuri", "волосы": "capelli", "голубые": "azzurri",
    "глаза": "occhi", "весёлый": "allegro", "добрый": "buono, gentile", "программист": "programmatore",
    "работает": "lavora", "дома": "a casa", "компьютером": "computer (strumentale: за компьютером = al computer)",
    "любит": "ama", "спорт": "sport", "утрам": "mattine (по утрам = la mattina, di solito)", "бегает": "corre",
    "субботам": "sabati (по субботам = il sabato)", "играет": "gioca", "футбол": "calcio", "хорошо": "bene",
    "готовит": "cucina", "любимое": "preferito (n.)", "блюдо": "piatto", "пельмени": "pel'meni (ravioli di carne)",
    "говорит": "parla", "по-итальянски": "in italiano", "хочет": "vuole", "выучить": "imparare (bene, fino in fondo)",
    "язык": "lingua", "говорим": "parliamo", "телефону": "telefono (по телефону = al telefono)", "помогаю": "aiuto",
    "ему": "a lui", "итальянским": "italiano (strumentale)", "русским": "russo (strumentale)",
}, [
    ("Какие глаза у Саши?", "Di che colore ha gli occhi Saša?", "Голубые", ["Карие", "Зелёные"]),
    ("Кем работает Саша?", "Che lavoro fa Saša?", "Программистом", ["Врачом", "Поваром"]),
    ("Что Саша делает по субботам?", "Cosa fa Saša il sabato?", "Играет в футбол", ["Бегает", "Готовит пельмени"]),
]),
lettura("metro", "🚇", "In metro", "В метро", 2, [
    ("Московское метро — одно из самых красивых в мире.", "La metro di Mosca è una delle più belle del mondo."),
    ("Некоторые станции похожи на музеи: там есть мозаики, статуи и люстры.", "Alcune stazioni sembrano musei: ci sono mosaici, statue e lampadari."),
    ("Метро работает с шести утра до часа ночи.", "La metro è aperta dalle sei di mattina all'una di notte."),
    ("Поезда ходят очень часто, каждые две-три минуты.", "I treni passano molto spesso, ogni due o tre minuti."),
    ("Чтобы войти, нужна карта «Тройка» или банковская карта.", "Per entrare serve la tessera «Trojka» o una carta bancaria."),
    ("В вагоне голос говорит: «Осторожно, двери закрываются!»", "Nel vagone una voce dice: «Attenzione, le porte si chiudono!»"),
    ("Потом он называет следующую станцию.", "Poi annuncia la prossima fermata."),
    ("Люди в метро читают, слушают музыку или спят.", "In metro la gente legge, ascolta musica o dorme."),
    ("Если вы потерялись, спросите: «Как доехать до Красной площади?»", "Se vi perdete, chiedete: «Come si arriva alla Piazza Rossa?»"),
], {
    "московское": "di Mosca (n.)", "две-три": "due o tre", "тройка": "Trojka, la tessera dei trasporti di Mosca", "одно": "uno (n.; одно из = uno dei)", "самых": "i più (superlativo)",
    "красивых": "belli (genitivo plurale)", "мире": "mondo (prepositivo)", "некоторые": "alcuni",
    "станции": "stazioni", "похожи": "somigliano (похожи на = somigliano a)", "музеи": "musei", "мозаики": "mosaici",
    "статуи": "statue", "люстры": "lampadari", "работает": "funziona, è aperto", "шести": "sei (genitivo)",
    "утра": "di mattina", "часа": "l'una (genitivo)", "ночи": "di notte", "поезда": "treni", "ходят": "passano, circolano",
    "каждые": "ogni", "минуты": "minuti", "чтобы": "per (+ infinito)", "войти": "entrare", "нужна": "serve (f.)",
    "карта": "tessera, carta", "банковская": "bancaria", "вагоне": "vagone (prepositivo)", "голос": "voce",
    "осторожно": "attenzione", "двери": "porte", "закрываются": "si chiudono", "называет": "annuncia, nomina",
    "следующую": "prossima (accusativo)", "станцию": "stazione (accusativo)", "читают": "leggono",
    "слушают": "ascoltano", "музыку": "musica (accusativo)", "спят": "dormono", "если": "se",
    "потерялись": "vi siete persi", "спросите": "chiedete", "доехать": "arrivare (con un mezzo)",
    "красной": "rossa (genitivo)", "площади": "piazza (genitivo)",
}, [
    ("На что похожи некоторые станции?", "A cosa somigliano alcune stazioni?", "На музеи", ["На магазины", "На парки"]),
    ("Как часто ходят поезда?", "Ogni quanto passano i treni?", "Каждые две-три минуты", ["Каждый час", "Раз в день"]),
    ("Что говорит голос в вагоне?", "Cosa dice la voce nel vagone?", "Осторожно, двери закрываются!", ["Добро пожаловать!", "Приятного аппетита!"]),
]),
lettura("dacia", "🏡", "Alla dacia", "Дача", 2, [
    ("Летом многие русские ездят на дачу.", "D'estate molti russi vanno alla dacia."),
    ("Дача — это маленький дом за городом, обычно с садом.", "La dacia è una casetta fuori città, di solito con l'orto."),
    ("Семья Петровых едет на дачу каждую пятницу вечером.", "La famiglia Petrov va alla dacia ogni venerdì sera."),
    ("Дорога занимает два часа, потому что на шоссе пробки.", "Il viaggio dura due ore, perché sulla statale c'è traffico."),
    ("На даче папа работает в саду, а мама собирает ягоды.", "Alla dacia il papà lavora nell'orto e la mamma raccoglie i frutti di bosco."),
    ("Дети купаются в речке и играют с собакой.", "I bambini fanno il bagno nel fiumiciattolo e giocano con il cane."),
    ("Вечером все пьют чай на веранде.", "La sera tutti bevono il tè sulla veranda."),
    ("Иногда соседи приходят в гости с пирогом.", "A volte i vicini vengono a trovarli con una torta."),
    ("В воскресенье вечером семья возвращается в город — усталая, но счастливая.", "Domenica sera la famiglia torna in città: stanca, ma felice."),
], {
    "летом": "d'estate", "многие": "molti", "русские": "russi", "ездят": "vanno (con un mezzo, di solito)", "дачу": "dacia (accusativo)",
    "дача": "dacia, casa di campagna", "маленький": "piccolo", "дом": "casa", "городом": "città (за городом = fuori città)",
    "садом": "orto, giardino (strumentale)", "семья": "famiglia", "петровых": "dei Petrov", "едет": "va (con un mezzo)",
    "каждую": "ogni (f. accusativo)", "пятницу": "venerdì (accusativo)", "дорога": "strada, viaggio",
    "занимает": "richiede, dura", "часа": "ore (dopo 2, 3, 4)", "потому": "perché (потому что)", "шоссе": "strada statale",
    "пробки": "ingorghi", "даче": "dacia (prepositivo)", "папа": "papà", "саду": "orto, giardino (в саду)",
    "мама": "mamma", "собирает": "raccoglie", "ягоды": "frutti di bosco", "дети": "bambini",
    "купаются": "fanno il bagno", "речке": "fiumiciattolo (prepositivo)", "играют": "giocano",
    "собакой": "cane (strumentale)", "пьют": "bevono", "чай": "tè", "веранде": "veranda (prepositivo)",
    "соседи": "vicini", "гости": "ospiti (приходить в гости = andare a trovare)", "пирогом": "torta (strumentale)",
    "воскресенье": "domenica", "возвращается": "torna", "город": "città", "усталая": "stanca", "счастливая": "felice",
}, [
    ("Что такое дача?", "Che cos'è la dacia?", "Дом за городом", ["Квартира в центре", "Гостиница"]),
    ("Когда Петровы едут на дачу?", "Quando vanno alla dacia i Petrov?", "В пятницу вечером", ["В понедельник утром", "Только зимой"]),
    ("Что делают дети?", "Cosa fanno i bambini?", "Купаются и играют с собакой", ["Работают в саду", "Смотрят телевизор"]),
]),
lettura("capodanno", "🎄", "Capodanno", "Новый год", 2, [
    ("Новый год — самый любимый праздник в России.", "Il Capodanno è la festa più amata in Russia."),
    ("В декабре люди покупают ёлку и подарки.", "A dicembre la gente compra l'albero e i regali."),
    ("Дети ждут Деда Мороза и Снегурочку.", "I bambini aspettano Nonno Gelo e Sneguročka."),
    ("Тридцать первого декабря вся семья сидит за большим столом.", "Il trentuno dicembre tutta la famiglia siede a una grande tavola."),
    ("На столе салат «Оливье», селёдка под шубой и мандарины.", "In tavola ci sono l'insalata Olivier, l'aringa «in pelliccia» e i mandarini."),
    ("В полночь бьют куранты, и все кричат: «С Новым годом!»", "A mezzanotte suonano i rintocchi del Cremlino e tutti gridano: «Buon anno!»"),
    ("Потом люди пьют шампанское и загадывают желание.", "Poi si beve lo spumante e si esprime un desiderio."),
    ("Праздник длится долго: в январе почти две недели не работают.", "La festa dura a lungo: a gennaio per quasi due settimane non si lavora."),
    ("А седьмого января — Рождество.", "E il sette gennaio è Natale."),
], {
    "новый": "nuovo", "год": "anno", "самый": "il più", "любимый": "amato, preferito", "праздник": "festa",
    "россии": "Russia (prepositivo)", "декабре": "dicembre (prepositivo)", "покупают": "comprano",
    "ёлку": "albero di Natale (accusativo)", "подарки": "regali", "дети": "bambini", "ждут": "aspettano",
    "деда": "nonno (accusativo)", "мороза": "gelo (Дед Мороз = Nonno Gelo)", "снегурочку": "Sneguročka, la nipote di Nonno Gelo",
    "тридцать": "trenta", "первого": "primo (il trentuno = тридцать первое)", "декабря": "di dicembre",
    "вся": "tutta", "семья": "famiglia", "сидит": "siede", "большим": "grande (strumentale)",
    "столом": "tavola (strumentale; за столом = a tavola)", "столе": "tavola (prepositivo)", "салат": "insalata", "оливье": "Olivier (la nostra insalata russa)",
    "селёдка": "aringa", "шубой": "pelliccia (strumentale)", "мандарины": "mandarini", "полночь": "mezzanotte",
    "бьют": "battono, suonano", "куранты": "i rintocchi (dell'orologio del Cremlino)", "кричат": "gridano",
    "новым": "nuovo (strumentale; с Новым годом = buon anno)", "годом": "anno (strumentale)", "пьют": "bevono",
    "шампанское": "spumante", "загадывают": "esprimono (un desiderio)", "желание": "desiderio", "длится": "dura",
    "долго": "a lungo", "январе": "gennaio (prepositivo)", "почти": "quasi", "недели": "settimane",
    "работают": "lavorano", "седьмого": "il sette", "января": "di gennaio", "рождество": "Natale",
}, [
    ("Кого ждут дети?", "Chi aspettano i bambini?", "Деда Мороза и Снегурочку", ["Папу", "Учителя"]),
    ("Что все кричат в полночь?", "Cosa gridano tutti a mezzanotte?", "С Новым годом!", ["Спокойной ночи!", "Приятного аппетита!"]),
    ("Когда в России Рождество?", "Quando è Natale in Russia?", "Седьмого января", ["Двадцать пятого декабря", "Первого мая"]),
]),
lettura("petersburg", "🌉", "Le notti bianche", "Белые ночи", 2, [
    ("Лаура из Милана. Она первый раз в России.", "Laura è di Milano. È in Russia per la prima volta."),
    ("Сначала она была в Москве, а теперь едет в Петербург.", "Prima è stata a Mosca e ora va a San Pietroburgo."),
    ("Она едет на поезде «Сапсан». Поездка занимает четыре часа.", "Viaggia sul treno «Sapsan». Il viaggio dura quattro ore."),
    ("В поезде она смотрит в окно: леса, деревни, реки.", "In treno guarda dal finestrino: boschi, villaggi, fiumi."),
    ("В Петербурге её гостиница находится на Невском проспекте.", "A San Pietroburgo il suo albergo è sulla Prospettiva Nevskij."),
    ("Вечером она гуляет по городу. Уже одиннадцать часов, но на улице светло!", "La sera passeggia per la città. Sono già le undici, ma fuori è chiaro!"),
    ("Это белые ночи: в июне солнце почти не заходит.", "Sono le notti bianche: a giugno il sole quasi non tramonta."),
    ("Завтра Лаура пойдёт в Эрмитаж.", "Domani Laura andrà all'Ermitage."),
    ("Она пишет маме: «Здесь очень красиво! Я не хочу уезжать!»", "Scrive alla mamma: «Qui è bellissimo! Non voglio partire!»"),
], {
    "милана": "Milano (genitivo)", "сапсан": "Sapsan, il treno veloce (lett. falco pellegrino)", "первый": "primo (первый раз = la prima volta)", "раз": "volta", "россии": "Russia (prepositivo)",
    "сначала": "prima", "была": "è stata (f.)", "москве": "Mosca (prepositivo)", "теперь": "ora", "едет": "va (con un mezzo)",
    "петербург": "San Pietroburgo", "поезде": "treno (prepositivo)", "поездка": "viaggio", "занимает": "dura, richiede",
    "четыре": "quattro", "часа": "ore (dopo 2, 3, 4)", "смотрит": "guarda", "окно": "finestra, finestrino", "леса": "boschi",
    "деревни": "villaggi", "реки": "fiumi", "петербурге": "San Pietroburgo (prepositivo)", "её": "suo (di lei)",
    "гостиница": "albergo", "находится": "si trova", "невском": "Nevskij (prepositivo)", "проспекте": "viale, prospettiva",
    "гуляет": "passeggia", "городу": "città (по городу = per la città)", "уже": "già", "одиннадцать": "undici",
    "часов": "ore (dopo 5+)", "улице": "strada (на улице = fuori)", "светло": "c'è luce, è chiaro", "белые": "bianche",
    "ночи": "notti", "июне": "giugno (prepositivo)", "солнце": "sole", "почти": "quasi", "заходит": "tramonta",
    "завтра": "domani", "пойдёт": "andrà (a piedi)", "эрмитаж": "Ermitage", "пишет": "scrive", "маме": "alla mamma",
    "красиво": "(è) bello", "хочу": "voglio", "уезжать": "partire, andarsene",
}, [
    ("Откуда Лаура?", "Di dov'è Laura?", "Из Милана", ["Из Рима", "Из Москвы"]),
    ("Сколько времени едет «Сапсан»?", "Quanto ci mette il «Sapsan»?", "Четыре часа", ["Два часа", "Десять часов"]),
    ("Почему вечером на улице светло?", "Perché la sera fuori è chiaro?", "Это белые ночи", ["Это зима", "Это утро"]),
    ("Куда Лаура пойдёт завтра?", "Dove andrà Laura domani?", "В Эрмитаж", ["В Кремль", "На вокзал"]),
]),
lettura("compleanno", "🎂", "Il compleanno di Katja", "День рождения", 2, [
    ("Сегодня у Кати день рождения. Ей тридцать лет.", "Oggi è il compleanno di Katja. Compie trent'anni."),
    ("Утром ей звонят родители и друзья.", "La mattina la chiamano i genitori e gli amici."),
    ("Коллеги на работе дарят ей цветы и торт.", "I colleghi al lavoro le regalano fiori e una torta."),
    ("Вечером Катя приглашает гостей домой.", "La sera Katja invita gli ospiti a casa."),
    ("Гости приносят подарки: книгу, духи и красивую чашку.", "Gli ospiti portano regali: un libro, un profumo e una bella tazza."),
    ("Все садятся за стол и говорят тосты.", "Tutti si siedono a tavola e fanno i brindisi."),
    ("Брат Кати говорит: «Желаю тебе здоровья, счастья и любви!»", "Il fratello di Katja dice: «Ti auguro salute, felicità e amore!»"),
    ("Потом Катя задувает свечи на торте.", "Poi Katja spegne le candeline sulla torta."),
    ("Все поют песню и танцуют до полуночи.", "Tutti cantano e ballano fino a mezzanotte."),
], {
    "сегодня": "oggi", "кати": "Katja (genitivo)", "день": "giorno (день рождения = compleanno)", "рождения": "della nascita",
    "ей": "a lei", "тридцать": "trenta", "лет": "anni", "утром": "la mattina", "звонят": "telefonano",
    "родители": "genitori", "друзья": "amici", "коллеги": "colleghi", "работе": "lavoro (prepositivo)",
    "дарят": "regalano", "цветы": "fiori", "торт": "torta", "вечером": "la sera", "приглашает": "invita",
    "гостей": "ospiti (accusativo)", "домой": "a casa (moto)", "гости": "ospiti", "приносят": "portano",
    "подарки": "regali", "книгу": "libro (accusativo)", "духи": "profumo", "красивую": "bella (accusativo)",
    "чашку": "tazza (accusativo)", "садятся": "si siedono", "стол": "tavola (за стол = a tavola)",
    "говорят": "dicono", "тосты": "brindisi", "брат": "fratello", "желаю": "auguro", "тебе": "a te",
    "здоровья": "salute (genitivo)", "счастья": "felicità (genitivo)", "любви": "amore (genitivo)",
    "задувает": "spegne soffiando", "свечи": "candeline", "торте": "torta (prepositivo)", "поют": "cantano",
    "песню": "canzone (accusativo)", "танцуют": "ballano", "полуночи": "mezzanotte (genitivo)",
}, [
    ("Сколько лет Кате?", "Quanti anni ha Katja?", "Тридцать", ["Двадцать", "Сорок"]),
    ("Что дарят коллеги?", "Cosa regalano i colleghi?", "Цветы и торт", ["Книгу", "Духи"]),
    ("Что желает брат?", "Cosa augura il fratello?", "Здоровья, счастья и любви", ["Хорошей погоды", "Много денег"]),
]),
]

GLOSSARIO_COMUNE = {
    "я": "io", "ты": "tu", "он": "lui", "она": "lei", "оно": "esso", "мы": "noi", "вы": "voi / Lei", "они": "loro",
    "меня": "me", "мне": "a me", "тебе": "a te", "нас": "noi (acc.)", "их": "loro (acc.) / il loro",
    "и": "e", "а": "e, invece", "но": "ma", "или": "o, oppure", "что": "che, cosa", "как": "come", "где": "dove",
    "когда": "quando", "куда": "dove (moto)", "кто": "chi", "почему": "perché", "в": "in, a", "во": "in, a",
    "на": "su, a", "с": "con / da", "со": "con", "у": "presso (у меня есть = ho)", "к": "verso, da", "по": "per, lungo",
    "о": "di, su (argomento)", "об": "di, su", "из": "da (provenienza)", "до": "fino a", "от": "da", "за": "dietro, per",
    "для": "per", "под": "sotto", "не": "non", "нет": "no / non c'è", "да": "sì", "это": "questo, è", "там": "lì",
    "здесь": "qui", "тут": "qui", "всё": "tutto", "все": "tutti", "очень": "molto", "ещё": "ancora, anche",
    "уже": "già", "тоже": "anche", "потом": "poi", "есть": "c'è / mangiare", "мой": "mio", "моя": "mia",
    "моё": "mio (n.)", "мои": "miei", "твой": "tuo", "наш": "nostro", "ваш": "vostro", "её": "suo (di lei)",
    "его": "suo (di lui)", "так": "così", "один": "uno", "одна": "una", "два": "due", "две": "due (f.)",
    "три": "tre", "сейчас": "adesso", "вечером": "la sera", "утром": "la mattina", "днём": "di giorno",
    "ночью": "di notte", "часто": "spesso", "иногда": "a volte", "всегда": "sempre", "люди": "persone, gente",
    "много": "molto, molti", "хорошо": "bene", "плохо": "male", "дома": "a casa", "говорит": "dice, parla",
    "потому": "perché (потому что)", "чтобы": "per (+ infinito)", "если": "se", "бы": "(condizionale)",
}

# ---------------------------------------------------------------- PROVERBI
PROVERBI = [
    ("Без труда не выловишь и рыбку из пруда.", "Senza fatica non tiri fuori neanche un pesciolino dallo stagno.", "Chi dorme non piglia pesci."),
    ("Тише едешь — дальше будешь.", "Più piano vai, più lontano arrivi.", "Chi va piano va sano e va lontano."),
    ("Не имей сто рублей, а имей сто друзей.", "Non avere cento rubli, ma cento amici.", "Chi trova un amico trova un tesoro."),
    ("Утро вечера мудренее.", "Il mattino è più saggio della sera.", "La notte porta consiglio."),
    ("Друг познаётся в беде.", "L'amico si riconosce nella sventura.", "Nel bisogno si conosce l'amico."),
    ("Лучше поздно, чем никогда.", "Meglio tardi che mai.", "Meglio tardi che mai."),
    ("Век живи — век учись.", "Vivi un secolo, impara un secolo.", "Non si finisce mai di imparare."),
    ("Повторение — мать учения.", "La ripetizione è la madre dell'apprendimento.", "Repetita iuvant."),
    ("Что посеешь, то и пожнёшь.", "Ciò che semini, quello raccoglierai.", "Si raccoglie ciò che si semina."),
    ("Не всё то золото, что блестит.", "Non è tutto oro quello che luccica.", "Non è tutto oro quel che luccica."),
    ("Москва не сразу строилась.", "Mosca non è stata costruita tutta in una volta.", "Roma non fu fatta in un giorno."),
    ("В гостях хорошо, а дома лучше.", "Da ospite si sta bene, ma a casa si sta meglio.", "Casa dolce casa."),
    ("Любишь кататься — люби и саночки возить.", "Se ti piace andare in slitta, ti deve piacere anche tirarla su.", "Hai voluto la bicicletta? Adesso pedala."),
    ("Слово — серебро, молчание — золото.", "La parola è d'argento, il silenzio è d'oro.", "Il silenzio è d'oro."),
    ("Яблоко от яблони недалеко падает.", "La mela non cade lontano dal melo.", "Tale padre, tale figlio."),
    ("Аппетит приходит во время еды.", "L'appetito viene durante il pasto.", "L'appetito vien mangiando."),
    ("На вкус и цвет товарищей нет.", "Sui gusti e sui colori non ci sono compagni.", "Tutti i gusti sono gusti."),
    ("Первый блин комом.", "La prima frittella viene a grumi.", "La prima volta non viene mai bene."),
    ("Не откладывай на завтра то, что можно сделать сегодня.", "Non rimandare a domani quello che puoi fare oggi.", "Non rimandare a domani quello che puoi fare oggi."),
    ("Под лежачий камень вода не течёт.", "Sotto una pietra ferma l'acqua non scorre.", "Aiutati che il ciel t'aiuta."),
    ("Глаза боятся, а руки делают.", "Gli occhi hanno paura, ma le mani lavorano.", "Il difficile è cominciare."),
    ("Волков бояться — в лес не ходить.", "Se hai paura dei lupi, non andare nel bosco.", "Chi non risica non rosica."),
    ("Семь раз отмерь, один раз отрежь.", "Misura sette volte, taglia una volta sola.", "Pensaci bene prima di agire."),
    ("Где хотенье, там и уменье.", "Dove c'è la voglia, c'è anche la capacità.", "Volere è potere."),
    ("Язык до Киева доведёт.", "La lingua ti porta fino a Kiev.", "Domandando si arriva a Roma."),
    ("Нет худа без добра.", "Non c'è male senza bene.", "Non tutto il male vien per nuocere."),
    ("Кто рано встаёт, тому Бог подаёт.", "A chi si alza presto, Dio dà.", "Il mattino ha l'oro in bocca."),
    ("Беда не приходит одна.", "La sventura non arriva mai da sola.", "Le disgrazie non vengono mai sole."),
    ("Сделал дело — гуляй смело.", "Finito il lavoro, vai a spasso tranquillo.", "Prima il dovere, poi il piacere."),
    ("Всему своё время.", "A ogni cosa il suo tempo.", "Ogni cosa a suo tempo."),
    ("Одна голова хорошо, а две лучше.", "Una testa va bene, ma due vanno meglio.", "Quattro occhi vedono meglio di due."),
    ("Лучше синица в руках, чем журавль в небе.", "Meglio una cinciallegra in mano che una gru in cielo.", "Meglio un uovo oggi che una gallina domani."),
    ("Цыплят по осени считают.", "I pulcini si contano in autunno.", "Non dire gatto se non ce l'hai nel sacco."),
    ("Не в деньгах счастье.", "La felicità non sta nei soldi.", "I soldi non fanno la felicità."),
    ("Время — деньги.", "Il tempo è denaro.", "Il tempo è denaro."),
    ("Как аукнется, так и откликнется.", "Come chiami nel bosco, così ti risponde l'eco.", "Chi la fa l'aspetti."),
    ("Ученье — свет, а неученье — тьма.", "Lo studio è luce, l'ignoranza è buio.", ""),
    ("Хлеб всему голова.", "Il pane è a capo di tutto.", ""),
]

# ---------------------------------------------------------------- CULTURA
CULTURA = [
    ("capodanno", "🎄", "Capodanno e Nonno Gelo",
     "In Russia la festa più grande non è Natale, ma Capodanno (Новый год). I regali li porta Дед Мороз, «Nonno Gelo», insieme alla nipote Снегурочка. A mezzanotte si ascoltano in tv i rintocchi dell'orologio del Cremlino e si esprime un desiderio. Il Natale ortodosso arriva dopo, il 7 gennaio.",
     [("Новый год", "Capodanno"), ("Дед Мороз", "Nonno Gelo"), ("ёлка", "albero di Natale"), ("подарок", "regalo"), ("С Новым годом!", "Buon anno!")]),
    ("te", "🫖", "Il tè e il samovar",
     "In Russia si beve tè a tutte le ore, spesso con la marmellata (варенье), il limone o lo zucchero in zollette. Il самовар è il grande bollitore tradizionale di metallo. «Пойдём попьём чаю» (andiamo a bere un tè) vuol dire anche: sediamoci a chiacchierare.",
     [("чай", "tè"), ("самовар", "samovar"), ("варенье", "marmellata"), ("сахар", "zucchero"), ("с лимоном", "al limone")]),
    ("dacia", "🏡", "La dacia",
     "Tantissime famiglie hanno una дача, una casetta di campagna con l'orto. Ci si va nei fine settimana d'estate: si coltivano patate, cetrioli e fragole, si fanno le conserve per l'inverno e si riposa lontano dalla città.",
     [("дача", "dacia"), ("огород", "orto"), ("огурец", "cetriolo"), ("клубника", "fragola"), ("за городом", "fuori città")]),
    ("banja", "🧖", "La banja",
     "La баня è la sauna russa a vapore. Ci si batte dolcemente con un mazzo di rametti di betulla (веник), poi ci si tuffa nell'acqua fredda o, d'inverno, nella neve. A chi esce dalla banja si dice «С лёгким паром!», più o meno «buon vapore leggero!».",
     [("баня", "sauna russa"), ("пар", "vapore"), ("веник", "mazzo di rametti"), ("берёза", "betulla"), ("С лёгким паром!", "Buon vapore!")]),
    ("nomi", "🪪", "Nome, patronimico e diminutivi",
     "I russi hanno nome, patronimico (отчество, dal nome del padre) e cognome: Анна Ивановна Петрова è Anna, figlia di Ivan. Con insegnanti, colleghi più anziani e sconosciuti si usa nome + patronimico: «Анна Ивановна». Tra amici si usano i diminutivi: Александр → Саша, Мария → Маша, Дмитрий → Дима, Екатерина → Катя.",
     [("имя", "nome"), ("отчество", "patronimico"), ("фамилия", "cognome"), ("Как вас зовут?", "Come si chiama?")]),
    ("tu-lei", "🤝", "Ты o вы?",
     "Funziona come il nostro «tu» e «Lei»: ты con amici, familiari e bambini; вы con sconosciuti, adulti e in situazioni formali (ed è anche il plurale, «voi»). Il passaggio al ты di solito si propone: «Давай на ты?», «Diamoci del tu?».",
     [("ты", "tu"), ("вы", "Lei / voi"), ("Давай на ты?", "Diamoci del tu?"), ("Можно на ты?", "Posso darti del tu?")]),
    ("superstizioni", "🐈‍⬛", "Superstizioni",
     "Prima di un viaggio ci si siede un attimo in silenzio: si chiama присесть на дорожку. Non ci si stringe la mano sopra la soglia di casa, e non si fischia in casa perché «si fischiano via i soldi». Se torni indietro perché hai dimenticato qualcosa, guardati allo specchio prima di uscire di nuovo.",
     [("примета", "superstizione"), ("порог", "soglia"), ("на дорожку", "per il viaggio"), ("зеркало", "specchio"), ("чёрная кошка", "gatto nero")]),
    ("fiori", "💐", "Fiori e regali",
     "I fiori si regalano in numero dispari: i mazzi con un numero pari si portano ai funerali. Quando si è ospiti non si arriva mai a mani vuote: fiori, una torta o qualcosa per il tè. E a tavola chi ospita insiste perché si mangi ancora: rifiutare con garbo fa parte del gioco.",
     [("цветы", "fiori"), ("букет", "mazzo di fiori"), ("в гости", "(andare) da qualcuno"), ("торт", "torta"), ("Угощайтесь!", "Si serva!")]),
    ("maslenica", "🥞", "Maslenica",
     "Масленица è la settimana che saluta l'inverno prima della Quaresima. Si mangiano i блины, frittelle rotonde e dorate come il sole, con panna acida, miele o caviale. L'ultimo giorno si brucia un fantoccio di paglia che rappresenta l'inverno e ci si chiede perdono a vicenda: è la «Domenica del perdono».",
     [("Масленица", "Maslenica"), ("блины", "frittelle, crêpes"), ("сметана", "panna acida"), ("мёд", "miele"), ("прости", "perdonami")]),
    ("vittoria", "🎖️", "Il 9 maggio",
     "Il Giorno della Vittoria (День Победы) ricorda la fine della Seconda guerra mondiale, che in Russia si chiama «Grande guerra patriottica». Quasi ogni famiglia ha perso qualcuno, per questo è una ricorrenza molto sentita: si portano fiori ai monumenti e molti sfilano con le foto dei propri nonni.",
     [("День Победы", "Giorno della Vittoria"), ("победа", "vittoria"), ("война", "guerra"), ("память", "memoria"), ("дедушка", "nonno")]),
    ("matrioska", "🪆", "La matrioska",
     "La матрёшка è una bambola di legno che ne contiene altre, sempre più piccole. È più giovane di quanto si pensi: nacque alla fine dell'Ottocento, ispirata a una bambola giapponese. Il nome viene da Матрёна, un nome femminile di campagna molto diffuso allora.",
     [("матрёшка", "matrioska"), ("кукла", "bambola"), ("дерево", "legno, albero"), ("сувенир", "souvenir")]),
    ("tavola", "🍽️", "A tavola",
     "Il pranzo russo comincia spesso con una zuppa: борщ, щи (di cavolo) o солянка. Il pane non manca mai, nero o bianco. Durante le cene si fanno molti brindisi (тосты), e non si beve «a vuoto», senza dire qualcosa. Prima di mangiare si augura «Приятного аппетита!».",
     [("суп", "zuppa"), ("хлеб", "pane"), ("тост", "brindisi"), ("За здоровье!", "Alla salute!"), ("Приятного аппетита!", "Buon appetito!")]),
    ("casa", "🥿", "Entrare in una casa russa",
     "Appena entrati ci si toglie le scarpe, e spesso il padrone di casa offre le pantofole (тапочки). Per strada i russi non sorridono agli sconosciuti: non è freddezza, un sorriso senza motivo sembra solo strano. Tra amici, invece, l'accoglienza è calorosissima.",
     [("тапочки", "pantofole"), ("разуваться", "togliersi le scarpe"), ("улыбка", "sorriso"), ("Проходите!", "Entri pure!")]),
    ("notti-bianche", "🌉", "Le notti bianche",
     "A San Pietroburgo, tra fine maggio e luglio, il sole tramonta appena e la notte resta chiara: sono le белые ночи. Di notte sulla Neva si aprono i ponti levatoi (разводные мосты) per far passare le navi: se sei dall'altra parte, a casa non torni fino al mattino!",
     [("белые ночи", "notti bianche"), ("мост", "ponte"), ("река", "fiume"), ("корабль", "nave")]),
    ("lingua", "🌍", "Il russo nel mondo",
     "Il russo è la lingua slava più parlata: lo usano circa 250 milioni di persone ed è una delle sei lingue ufficiali dell'ONU. L'alfabeto cirillico porta il nome di san Cirillo, il monaco che nel IX secolo, con il fratello Metodio, portò la scrittura agli slavi; il cirillico vero e proprio lo svilupparono i loro discepoli.",
     [("язык", "lingua"), ("алфавит", "alfabeto"), ("буква", "lettera"), ("кириллица", "cirillico")]),
    ("metro-mosca", "🚇", "La metro di Mosca",
     "Aperta nel 1935, la metro di Mosca è famosa per le stazioni-palazzo: marmi, mosaici, lampadari. Sulle linee circolari gli annunci cambiano voce: verso il centro parla un uomo, verso la periferia una donna. Un trucco per orientarsi a occhi chiusi!",
     [("станция", "stazione"), ("вход", "entrata"), ("выход", "uscita"), ("пересадка", "cambio di linea"), ("линия", "linea")]),
]

# ---------------------------------------------------------------- FALSI AMICI / GEMELLE
FALSI_AMICI = [
    ("магазин", "magazzino", "negozio (il magazzino è склад)"),
    ("фамилия", "famiglia", "cognome (la famiglia è семья)"),
    ("кабинет", "gabinetto", "studio, ufficio, ambulatorio"),
    ("банка", "banca", "barattolo (la banca è банк)"),
    ("камера", "camera", "macchina fotografica / cella (la stanza è комната)"),
    ("мост", "mosto", "ponte"),
    ("конфета", "confetto", "caramella, cioccolatino"),
    ("палка", "palco", "bastone"),
    ("портфель", "portafoglio", "cartella per documenti (il portafoglio è кошелёк)"),
    ("карта", "carta", "mappa / carta bancaria (la carta da scrivere è бумага)"),
    ("гастроном", "gastronomo", "negozio di alimentari"),
    ("анекдот", "aneddoto", "barzelletta"),
    ("ремонт", "rimonta", "ristrutturazione, riparazione"),
    ("симпатичный", "simpatico", "carino, di bell'aspetto (simpatico si dice приятный, милый)"),
    ("ангина", "angina", "tonsillite, mal di gola forte"),
    ("бланк", "bianco", "modulo da compilare"),
    ("духи", "duchi", "profumo"),
    ("спирт", "spirito (anima)", "alcol etilico"),
    ("стол", "stola", "tavolo"),
    ("батон", "bastone", "filone di pane"),
    ("мармелад", "marmellata", "gelatine di frutta (la marmellata è варенье o джем)"),
    ("журнал", "giornale", "rivista (il giornale è газета)"),
    ("палата", "palato", "corsia d'ospedale / camera del parlamento"),
    ("артист", "artista (pittore)", "attore, artista di spettacolo (il pittore è художник)"),
]
GEMELLE = [
    ("театр", "teatro"), ("музыка", "musica"), ("телефон", "telefono"), ("машина", "macchina"), ("банк", "banca"),
    ("кофе", "caffè"), ("паспорт", "passaporto"), ("пальто", "cappotto (paltò)"), ("фото", "foto"), ("радио", "radio"),
    ("опера", "opera"), ("балет", "balletto"), ("компьютер", "computer"), ("университет", "università"),
    ("студент", "studente"), ("профессор", "professore"), ("доктор", "dottore"), ("музей", "museo"), ("парк", "parco"),
    ("метро", "metro"), ("такси", "taxi"), ("автобус", "autobus"), ("ресторан", "ristorante"), ("меню", "menù"),
    ("пицца", "pizza"), ("лимон", "limone"), ("банан", "banana"), ("шоколад", "cioccolato"), ("аэропорт", "aeroporto"),
    ("гитара", "chitarra"), ("роза", "rosa"), ("лампа", "lampada"), ("календарь", "calendario"), ("минута", "minuto"),
    ("момент", "momento"), ("идея", "idea"), ("проблема", "problema"), ("программа", "programma"),
    ("президент", "presidente"), ("поэт", "poeta"), ("фильм", "film"), ("газета", "giornale (gazzetta)"),
    ("фабрика", "fabbrica"), ("трамвай", "tram"), ("капитан", "capitano"), ("пилот", "pilota"), ("торт", "torta"),
    ("банкомат", "bancomat"),
]

# ---------------------------------------------------------------- CASI
# forme singolari: nominativo, genitivo, dativo, accusativo, strumentale, prepositivo
NOMI = {
    "Москва": ["Москва", "Москвы", "Москве", "Москву", "Москвой", "Москве"],
    "школа": ["школа", "школы", "школе", "школу", "школой", "школе"],
    "мама": ["мама", "мамы", "маме", "маму", "мамой", "маме"],
    "брат": ["брат", "брата", "брату", "брата", "братом", "брате"],
    "друг": ["друг", "друга", "другу", "друга", "другом", "друге"],
    "сестра": ["сестра", "сестры", "сестре", "сестру", "сестрой", "сестре"],
    "книга": ["книга", "книги", "книге", "книгу", "книгой", "книге"],
    "парк": ["парк", "парка", "парку", "парк", "парком", "парке"],
    "работа": ["работа", "работы", "работе", "работу", "работой", "работе"],
    "вода": ["вода", "воды", "воде", "воду", "водой", "воде"],
    "машина": ["машина", "машины", "машине", "машину", "машиной", "машине"],
    "Италия": ["Италия", "Италии", "Италии", "Италию", "Италией", "Италии"],
    "Рим": ["Рим", "Рима", "Риму", "Рим", "Римом", "Риме"],
    "театр": ["театр", "театра", "театру", "театр", "театром", "театре"],
    "врач": ["врач", "врача", "врачу", "врача", "врачом", "враче"],
    "подруга": ["подруга", "подруги", "подруге", "подругу", "подругой", "подруге"],
    "папа": ["папа", "папы", "папе", "папу", "папой", "папе"],
    "ручка": ["ручка", "ручки", "ручке", "ручку", "ручкой", "ручке"],
    "сыр": ["сыр", "сыра", "сыру", "сыр", "сыром", "сыре"],
    "молоко": ["молоко", "молока", "молоку", "молоко", "молоком", "молоке"],
    "стол": ["стол", "стола", "столу", "стол", "столом", "столе"],
    "город": ["город", "города", "городу", "город", "городом", "городе"],
    "университет": ["университет", "университета", "университету", "университет", "университетом", "университете"],
    "музыка": ["музыка", "музыки", "музыке", "музыку", "музыкой", "музыке"],
    "учитель": ["учитель", "учителя", "учителю", "учителя", "учителем", "учителе"],
    "собака": ["собака", "собаки", "собаке", "собаку", "собакой", "собаке"],
    "лимон": ["лимон", "лимона", "лимону", "лимон", "лимоном", "лимоне"],
    "сахар": ["сахар", "сахара", "сахару", "сахар", "сахаром", "сахаре"],
    "Анна": ["Анна", "Анны", "Анне", "Анну", "Анной", "Анне"],
    "Иван": ["Иван", "Ивана", "Ивану", "Ивана", "Иваном", "Иване"],
    "поезд": ["поезд", "поезда", "поезду", "поезд", "поездом", "поезде"],
    "автобус": ["автобус", "автобуса", "автобусу", "автобус", "автобусом", "автобусе"],
    "море": ["море", "моря", "морю", "море", "морем", "море"],
    "кухня": ["кухня", "кухни", "кухне", "кухню", "кухней", "кухне"],
    "семья": ["семья", "семьи", "семье", "семью", "семьёй", "семье"],
    "магазин": ["магазин", "магазина", "магазину", "магазин", "магазином", "магазине"],
}
CASO_IDX = {"gen": 1, "dat": 2, "acc": 3, "str": 4, "pre": 5}
PERCHE = {
    "pre_v": "в + prepositivo: dove si è (stato in luogo).",
    "pre_na": "на + prepositivo: alcuni luoghi vogliono на (lavoro, mare, cucina…).",
    "pre_o": "о + prepositivo: «a proposito di, a».",
    "pre_mezzo": "на + prepositivo per il mezzo di trasporto: на поезде, на автобусе.",
    "acc_v": "в + accusativo: dove si va (moto a luogo).",
    "acc_ogg": "complemento oggetto: accusativo (femminile -а → -у).",
    "acc_anim": "complemento oggetto maschile animato: accusativo = genitivo (-а).",
    "acc_inan": "complemento oggetto maschile inanimato: accusativo = nominativo.",
    "gen_net": "нет + genitivo: «non c'è, non ho».",
    "gen_poss": "possesso («di qualcuno»): genitivo.",
    "gen_qta": "quantità o contenuto (un bicchiere di…): genitivo.",
    "gen_iz": "из + genitivo: da dove vieni (provenienza).",
    "gen_u": "у + genitivo: у брата есть = mio fratello ha.",
    "gen_bez": "без + genitivo: «senza».",
    "gen_ot": "от + genitivo: «da» (distanza, provenienza).",
    "gen_dlya": "для + genitivo: «per».",
    "dat_a": "a chi? → dativo (dare, scrivere, telefonare a qualcuno).",
    "dat_k": "к + dativo: andare da una persona.",
    "dat_nrav": "нравиться: chi prova il piacere va al dativo (Анне нравится = ad Anna piace).",
    "dat_pomog": "помогать + dativo: aiutare qualcuno.",
    "dat_po": "по + dativo: «per, lungo» (in giro per).",
    "str_mezzo": "strumento (con cosa?): strumentale, senza preposizione.",
    "str_s": "с + strumentale: «con, insieme a».",
    "str_prof": "работать / стать + strumentale: la professione.",
    "str_int": "интересоваться + strumentale: interessarsi di.",
}
CASI = [
    # frase, nome base, caso, italiano, perché
    ("Я живу в ___.", "Москва", "pre", "Vivo a Mosca.", "pre_v"),
    ("Мы гуляем в ___.", "парк", "pre", "Passeggiamo nel parco.", "pre_v"),
    ("Дети сейчас в ___.", "школа", "pre", "I bambini ora sono a scuola.", "pre_v"),
    ("Папа сейчас на ___.", "работа", "pre", "Papà ora è al lavoro.", "pre_na"),
    ("Я часто думаю о ___.", "мама", "pre", "Penso spesso alla mamma.", "pre_o"),
    ("Книга лежит на ___.", "стол", "pre", "Il libro è sul tavolo.", "pre_na"),
    ("Мой брат учится в ___.", "университет", "pre", "Mio fratello studia all'università.", "pre_v"),
    ("Мама готовит на ___.", "кухня", "pre", "La mamma cucina in cucina.", "pre_na"),
    ("Летом мы отдыхаем на ___.", "море", "pre", "D'estate ci riposiamo al mare.", "pre_na"),
    ("В прошлом году я был в ___.", "Рим", "pre", "L'anno scorso sono stato a Roma.", "pre_v"),
    ("Мы едем на ___.", "поезд", "pre", "Viaggiamo in treno.", "pre_mezzo"),
    ("Я еду на работу на ___.", "автобус", "pre", "Vado al lavoro in autobus.", "pre_mezzo"),
    ("Я иду в ___.", "школа", "acc", "Vado a scuola.", "acc_v"),
    ("Завтра мы едем в ___.", "Москва", "acc", "Domani andiamo a Mosca.", "acc_v"),
    ("Вечером мы идём в ___.", "театр", "acc", "Stasera andiamo a teatro.", "acc_inan"),
    ("Я читаю ___.", "книга", "acc", "Leggo un libro.", "acc_ogg"),
    ("Я люблю ___.", "музыка", "acc", "Amo la musica.", "acc_ogg"),
    ("Я вижу ___.", "Анна", "acc", "Vedo Anna.", "acc_ogg"),
    ("Я жду ___.", "брат", "acc", "Aspetto mio fratello.", "acc_anim"),
    ("Мы покупаем ___.", "машина", "acc", "Compriamo una macchina.", "acc_ogg"),
    ("Я пью ___.", "вода", "acc", "Bevo acqua.", "acc_ogg"),
    ("Я хорошо знаю ___.", "Иван", "acc", "Conosco bene Ivan.", "acc_anim"),
    ("У меня нет ___.", "машина", "gen", "Non ho la macchina.", "gen_net"),
    ("Это книга ___.", "сестра", "gen", "È il libro di mia sorella.", "gen_poss"),
    ("Дайте, пожалуйста, стакан ___.", "молоко", "gen", "Mi dia un bicchiere di latte, per favore.", "gen_qta"),
    ("Я из ___.", "Италия", "gen", "Vengo dall'Italia.", "gen_iz"),
    ("У ___ есть собака.", "брат", "gen", "Mio fratello ha un cane.", "gen_u"),
    ("Чай без ___, пожалуйста.", "лимон", "gen", "Un tè senza limone, per favore.", "gen_bez"),
    ("Я живу недалеко от ___.", "парк", "gen", "Abito non lontano dal parco.", "gen_ot"),
    ("Это подарок для ___.", "мама", "gen", "È un regalo per la mamma.", "gen_dlya"),
    ("Сегодня нет ___.", "учитель", "gen", "Oggi l'insegnante non c'è.", "gen_net"),
    ("Дайте, пожалуйста, бутылку ___.", "вода", "gen", "Mi dia una bottiglia d'acqua, per favore.", "gen_qta"),
    ("Я звоню ___.", "мама", "dat", "Telefono alla mamma.", "dat_a"),
    ("Я даю книгу ___.", "друг", "dat", "Do il libro a un amico.", "dat_a"),
    ("Завтра я иду к ___.", "врач", "dat", "Domani vado dal medico.", "dat_k"),
    ("Я пишу письмо ___.", "сестра", "dat", "Scrivo una lettera a mia sorella.", "dat_a"),
    ("___ нравится музыка.", "Анна", "dat", "Ad Anna piace la musica.", "dat_nrav"),
    ("Я помогаю ___.", "папа", "dat", "Aiuto papà.", "dat_pomog"),
    ("Мы гуляем по ___.", "город", "dat", "Passeggiamo per la città.", "dat_po"),
    ("Я покупаю подарок ___.", "подруга", "dat", "Compro un regalo all'amica.", "dat_a"),
    ("Я пишу ___.", "ручка", "str", "Scrivo con la penna.", "str_mezzo"),
    ("Чай с ___, пожалуйста.", "лимон", "str", "Un tè al limone, per favore.", "str_s"),
    ("Я гуляю с ___.", "собака", "str", "Passeggio con il cane.", "str_s"),
    ("Мой брат работает ___.", "врач", "str", "Mio fratello fa il medico.", "str_prof"),
    ("Мы разговариваем с ___.", "учитель", "str", "Parliamo con l'insegnante.", "str_s"),
    ("Он хочет стать ___.", "врач", "str", "Vuole diventare medico.", "str_prof"),
    ("Я интересуюсь ___.", "музыка", "str", "Mi interesso di musica.", "str_int"),
    ("Хлеб с ___.", "сыр", "str", "Pane con il formaggio.", "str_s"),
    ("Я живу с ___.", "семья", "str", "Vivo con la mia famiglia.", "str_s"),
    ("Мы идём в кино с ___.", "друг", "str", "Andiamo al cinema con un amico.", "str_s"),
]

# ---------------------------------------------------------------- VERBI DI MOTO
MOTO = {
    "verbi": [
        {"inf": "идти", "it": "andare a piedi — adesso, in una direzione", "pres": ["иду", "идёшь", "идёт", "идём", "идёте", "идут"], "pass": "шёл, шла, шли"},
        {"inf": "ходить", "it": "andare a piedi — di solito, spesso, andata e ritorno", "pres": ["хожу", "ходишь", "ходит", "ходим", "ходите", "ходят"], "pass": "ходил, ходила, ходили"},
        {"inf": "ехать", "it": "andare con un mezzo — adesso, in una direzione", "pres": ["еду", "едешь", "едет", "едем", "едете", "едут"], "pass": "ехал, ехала, ехали"},
        {"inf": "ездить", "it": "andare con un mezzo — di solito, spesso, andata e ritorno", "pres": ["езжу", "ездишь", "ездит", "ездим", "ездите", "ездят"], "pass": "ездил, ездила, ездили"},
    ],
    "regole": [
        "A piedi → идти / ходить. Con un mezzo (macchina, treno, autobus, metro) → ехать / ездить.",
        "Adesso, in una direzione («sto andando») → идти / ехать.",
        "Di solito, spesso, ogni giorno, oppure andata e ritorno («ci sono stato») → ходить / ездить.",
        "«Вчера я ходил в театр» = ieri sono andato a teatro (e sono tornato): è come «я был в театре».",
    ],
    "frasi": [
        ("Сейчас я ___ в магазин.", "иду", ["хожу", "еду", "езжу"], "Adesso sto andando al negozio (a piedi).", "adesso, a piedi, in una direzione → идти"),
        ("Каждый день я ___ на работу пешком.", "хожу", ["иду", "езжу", "еду"], "Ogni giorno vado al lavoro a piedi.", "abitudine + a piedi → ходить"),
        ("Завтра мы ___ в Москву на поезде.", "едем", ["ездим", "идём", "ходим"], "Domani andiamo a Mosca in treno.", "un viaggio preciso, con un mezzo → ехать"),
        ("Летом мы часто ___ на дачу.", "ездим", ["едем", "ходим", "идём"], "D'estate andiamo spesso alla dacia.", "spesso + con un mezzo → ездить"),
        ("Куда ты ___? — В парк.", "идёшь", ["ходишь", "едешь", "ездишь"], "Dove stai andando? — Al parco (a piedi).", "adesso, verso un posto → идти"),
        ("Дети ___ в школу каждое утро.", "ходят", ["идут", "ездят", "едут"], "I bambini vanno a scuola ogni mattina.", "ogni mattina = abitudine → ходить"),
        ("Вчера я ___ в театр.", "ходил", ["шёл", "ездил", "ехал"], "Ieri sono andato a teatro (a piedi, e sono tornato).", "andata e ritorno nel passato → ходить"),
        ("Мой папа ___ на работу на машине.", "ездит", ["едет", "ходит", "идёт"], "Mio papà va al lavoro in macchina (di solito).", "abitudine + con un mezzo → ездить"),
        ("Когда я ___ домой, я встретил друга.", "шёл", ["ходил", "ехал", "ездил"], "Mentre tornavo a casa a piedi, ho incontrato un amico.", "in quel momento, in una direzione → идти (шёл)"),
        ("Вы часто ___ в кино?", "ходите", ["идёте", "ездите", "едете"], "Andate spesso al cinema?", "spesso → ходить"),
        ("Мы ___ на такси в аэропорт.", "едем", ["ездим", "идём", "ходим"], "Stiamo andando in taxi all'aeroporto.", "adesso, con un mezzo → ехать"),
        ("Я не люблю ___ на метро.", "ездить", ["ехать", "ходить", "идти"], "Non mi piace andare in metro.", "in generale, con un mezzo → ездить"),
        ("Анна ___ в бассейн три раза в неделю.", "ходит", ["идёт", "ездит", "едет"], "Anna va in piscina tre volte a settimana.", "tre volte a settimana = abitudine → ходить"),
        ("Прошлым летом мы ___ в Италию.", "ездили", ["ехали", "ходили", "шли"], "L'estate scorsa siamo stati in Italia.", "andata e ritorno, con un mezzo → ездить"),
        ("Куда вы ___ на машине?", "едете", ["ездите", "идёте", "ходите"], "Dove state andando in macchina?", "adesso, con un mezzo → ехать"),
        ("Моему сыну год, и он уже ___.", "ходит", ["идёт", "ездит", "едет"], "Mio figlio ha un anno e cammina già.", "saper camminare → ходить"),
        ("Сейчас они ___ в театр на автобусе.", "едут", ["ездят", "идут", "ходят"], "Adesso stanno andando a teatro in autobus.", "adesso, con un mezzo → ехать"),
        ("Обычно я ___ в университет пешком.", "хожу", ["иду", "езжу", "еду"], "Di solito vado all'università a piedi.", "di solito → ходить"),
        ("Мы ___ по парку и разговариваем.", "ходим", ["идём", "ездим", "едем"], "Camminiamo per il parco e chiacchieriamo.", "in giro, senza una direzione → ходить"),
        ("Смотри, вон ___ Маша!", "идёт", ["ходит", "едет", "ездит"], "Guarda, sta arrivando Maša!", "la vedi adesso, a piedi → идти"),
    ],
}

# ---------------------------------------------------------------- PERCORSO A1
def P_(t, titolo, **kw):
    x = {"t": t, "titolo": titolo}; x.update(kw); return x

PERCORSO = [
    {"id": "primi-passi", "icona": "👋", "titolo": "Primi passi", "desc": "Le lettere, salutare e presentarsi", "passi": [
        P_("cyr", "Quiz sulle lettere"),
        P_("flash", "Parole: saluti e cortesia", tags=["saluti", "cortesia"], n=12),
        P_("frasi", "Frasi per presentarsi", tags=["saluti", "presentarsi", "cortesia"]),
        P_("recita", "Dialogo: fare conoscenza", id="conoscenza"),
    ]},
    {"id": "numeri", "icona": "🔢", "titolo": "I numeri", "desc": "Da 0 a 100 e i primi prezzi", "passi": [
        P_("numLeggi", "Leggi i numeri 0–20", range="r20"),
        P_("numDettato", "Ascolta e scrivi 0–20", range="r20"),
        P_("numLeggi", "Leggi i numeri 21–100", range="r100"),
        P_("prezzi", "Quanto costa?"),
    ]},
    {"id": "famiglia", "icona": "👨‍👩‍👧", "titolo": "Famiglia e persone", "desc": "Parlare di sé e dei propri cari", "passi": [
        P_("flash", "Parole: famiglia", tags=["famiglia"], n=12),
        P_("lettura", "Lettura: Mi chiamo Anna", id="anna"),
        P_("frasi", "Frasi sulla famiglia", tags=["famiglia", "presentarsi"]),
        P_("lettura", "Lettura: Il mio amico Saša", id="sasha"),
    ]},
    {"id": "bar", "icona": "☕", "titolo": "Al bar e a tavola", "desc": "Ordinare, pagare, il cibo", "passi": [
        P_("flash", "Parole: cibo", tags=["cibo"], n=12),
        P_("recita", "Dialogo: al bar", id="bar"),
        P_("dlgquiz", "Cosa rispondi? Al ristorante", id="ristorante"),
        P_("lettura", "Lettura: Al mercato", id="mercato"),
        P_("componi", "Componi: cibo e ristorante", tags=["cibo", "ristorante"]),
    ]},
    {"id": "citta", "icona": "🏙️", "titolo": "In città", "desc": "Chiedere la strada, dove sei", "passi": [
        P_("flash", "Parole: città", tags=["città"], n=12),
        P_("recita", "Dialogo: chiedere la strada", id="strada"),
        P_("casi", "Casi: dove sei? (prepositivo)", caso="pre"),
        P_("lettura", "Lettura: In metro", id="metro"),
    ]},
    {"id": "tempo", "icona": "🕒", "titolo": "Ore, giorni e meteo", "desc": "Che ore sono, che tempo fa", "passi": [
        P_("ore", "Che ore sono?"),
        P_("flash", "Parole: tempo", tags=["tempo"], n=12),
        P_("flash", "Parole: meteo", tags=["meteo"], n=12),
        P_("lettura", "Lettura: Il tempo a Mosca", id="meteo"),
        P_("recita", "Dialogo: che tempo fa?", id="meteo"),
    ]},
    {"id": "casa", "icona": "🏠", "titolo": "Casa e giornata", "desc": "La routine di tutti i giorni", "passi": [
        P_("flash", "Parole: casa", tags=["casa"], n=12),
        P_("lettura", "Lettura: La mattina di Marco", id="marco"),
        P_("frasi", "Frasi di tutti i giorni", tags=["quotidiano", "routine"]),
        P_("componi", "Componi: la giornata", tags=["quotidiano", "routine"]),
    ]},
    {"id": "andare", "icona": "🚶", "titolo": "Andare: i verbi di moto", "desc": "идти, ходить, ехать, ездить", "passi": [
        P_("moto", "Verbi di moto"),
        P_("casi", "Casi: dove vai? (accusativo)", caso="acc"),
        P_("recita", "Dialogo: in taxi", id="taxi"),
        P_("lettura", "Lettura: Alla dacia", id="dacia"),
    ]},
    {"id": "viaggio", "icona": "✈️", "titolo": "In viaggio", "desc": "Stazione, aeroporto, albergo", "passi": [
        P_("flash", "Parole: viaggio", tags=["viaggio"], n=12),
        P_("recita", "Dialogo: alla stazione", id="stazione"),
        P_("recita", "Dialogo: in albergo", id="albergo"),
        P_("dlgquiz", "Cosa rispondi? Controllo passaporti", id="aeroporto"),
        P_("lettura", "Lettura: Le notti bianche", id="petersburg"),
    ]},
    {"id": "negozi", "icona": "🛍️", "titolo": "Negozi e vestiti", "desc": "Comprare, provare, pagare", "passi": [
        P_("flash", "Parole: vestiti", tags=["vestiti"], n=12),
        P_("recita", "Dialogo: al mercato", id="mercato"),
        P_("recita", "Dialogo: comprare una giacca", id="vestiti"),
        P_("casi", "Casi: di chi? quanto? (genitivo)", caso="gen"),
    ]},
    {"id": "salute", "icona": "💊", "titolo": "Salute", "desc": "Il corpo, la farmacia, il medico", "passi": [
        P_("flash", "Parole: corpo", tags=["corpo"], n=12),
        P_("recita", "Dialogo: in farmacia", id="farmacia"),
        P_("recita", "Dialogo: dal medico", id="medico"),
        P_("frasi", "Frasi: salute", tags=["salute", "corpo", "urgenza"]),
    ]},
    {"id": "feste", "icona": "🎉", "titolo": "Feste e ospiti", "desc": "Auguri, regali, cultura", "passi": [
        P_("lettura", "Lettura: Capodanno", id="capodanno"),
        P_("lettura", "Lettura: Il compleanno di Katja", id="compleanno"),
        P_("recita", "Dialogo: ospiti a cena", id="ospiti"),
        P_("casi", "Casi: a chi? (dativo)", caso="dat"),
        P_("casi", "Casi: con chi? (strumentale)", caso="str"),
    ]},
]

# ---------------------------------------------------------------- CONTROLLI E SCRITTURA
dlg_ids = {x["id"] for x in d.get("dialoghi", [])}
let_ids = {x["id"] for x in LETTURE}
for tappa in PERCORSO:
    for p in tappa["passi"]:
        if p["t"] == "recita" or p["t"] == "dlgquiz":
            assert p["id"] in dlg_ids, p
        if p["t"] == "lettura":
            assert p["id"] in let_ids, p
for fr, base, caso, it, why in CASI:
    assert base in NOMI and caso in CASO_IDX and why in PERCHE and "___" in fr, fr
for l in LETTURE:
    for q in l["domande"]:
        assert q["ok"] not in q["opts"], q

d["letture"] = LETTURE
d["glossarioLetture"] = GLOSSARIO_COMUNE
d["proverbi"] = [{"ru": ru, "lett": lett, "it": it} for ru, lett, it in PROVERBI]
d["cultura"] = [{"id": i, "icona": e, "titolo": t, "testo": tx, "parole": [{"ru": r, "it": it} for r, it in pw]}
                for i, e, t, tx, pw in CULTURA]
d["falsiAmici"] = [{"ru": ru, "sembra": s, "it": it} for ru, s, it in FALSI_AMICI]
d["paroleGemelle"] = [{"ru": ru, "it": it} for ru, it in GEMELLE]
d["casiNomi"] = NOMI
d["casi"] = [{"frase": fr, "base": base, "caso": caso, "ok": NOMI[base][CASO_IDX[caso]], "it": it, "perche": PERCHE[why]}
             for fr, base, caso, it, why in CASI]
d["verbiMoto"] = {"verbi": MOTO["verbi"], "regole": MOTO["regole"],
                  "frasi": [{"frase": fr, "ok": ok, "opts": opts, "it": it, "perche": why} for fr, ok, opts, it, why in MOTO["frasi"]]}
d["percorso"] = PERCORSO

nota = (" Secondo blocco (scripts/add_contenuti_2.py): 'letture' (racconti A1 con glossario e domande),"
        " 'proverbi', 'cultura', 'falsiAmici', 'paroleGemelle', 'casi' + 'casiNomi', 'verbiMoto', 'percorso' (Percorso A1).")
if "add_contenuti_2" not in d["meta"].get("note", ""):
    d["meta"]["note"] = d["meta"].get("note", "") + nota

with io.open(P, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("OK: letture", len(LETTURE), "| proverbi", len(PROVERBI), "| cultura", len(CULTURA),
      "| falsi amici", len(FALSI_AMICI), "| gemelle", len(GEMELLE), "| casi", len(CASI),
      "| moto", len(MOTO["frasi"]), "| tappe", len(PERCORSO), "| passi", sum(len(t["passi"]) for t in PERCORSO))
