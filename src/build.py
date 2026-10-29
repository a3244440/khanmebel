#!/usr/bin/env python3
"""
Генератор сайта Khan Mebel.

Запуск из корня репозитория:  python3 src/build.py
Пишет готовые HTML-страницы, sitemap.xml, robots.txt и llms.txt в корень.
Тексты, цены, отзывы и проекты правятся в этом файле, стили в assets/css/khan.css,
калькулятор в src/partials/calculator.html и assets/js/calculator.js.
"""
import json, os, re, urllib.parse, datetime
TODAY = datetime.date.today().isoformat()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = ROOT
# Адрес сайта для canonical, sitemap и разметки. После подключения своего домена поменяйте здесь.
DOMAIN = "https://khanmebel.vercel.app"

WA_NUM = "77001116291"
PHONE_H = "+7 700 111 62 91"
ADDR = "ул. Ыкылас Дукенулы, 31/2"
WA_TEXT = "Здравствуйте! Пишу с сайта Khan Mebel. Хочу рассчитать мебель на заказ."
WA = f"https://wa.me/{WA_NUM}?text=" + urllib.parse.quote(WA_TEXT)
IG = "https://www.instagram.com/khan_mebel.kz"
GIS = "https://2gis.kz/astana/firm/70000001102661573"
GIS_REV = GIS + "/tab/reviews"
GIS_ROUTE = "https://2gis.kz/astana/directions/points/%7C71.435401%2C51.183004%3B70000001102661573"

LOGO_SVG = '''<svg viewBox="0 0 100 74" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6d474"/><stop offset="1" stop-color="#b98d2c"/></linearGradient></defs><path d="M47.6 1.6a3 3 0 0 1 4.8 0l45 68.3A2.6 2.6 0 0 1 95.2 74H79.6a4 4 0 0 1-3.4-1.9L50 30.5 23.8 72.1a4 4 0 0 1-3.4 1.9H4.8a2.6 2.6 0 0 1-2.2-4.1z" fill="url(#lg)"/></svg>'''
CHAT_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.4.8 3.2.6.5-.1 1.5-.6 1.7-1.2s.2-1.1.2-1.2-.2-.2-.4-.3Z"/></svg>'

NAV = [("kuhni-na-zakaz-astana.html", "Кухни"), ("mebel-na-zakaz-astana.html", "Мебель на заказ"),
       ("mebel-pod-klyuch-astana.html", "Под ключ"), ("{home}#projects", "Проекты"), ("{home}#calc", "Калькулятор"),
       ("{home}#reviews", "Отзывы"), ("{home}#contacts", "Контакты")]

FONTS = "https://fonts.googleapis.com/css2?family=Onest:wght@300;400;500;600;700&display=swap"

def lockup(cls="", href=None):
    inner = f'{LOGO_SVG}<b>KHAN</b><small>mebel</small>'
    if href is None:
        return f'<div class="lockup {cls}" role="img" aria-label="Khan Mebel">{inner}</div>'
    return f'<a class="lockup {cls}" href="{href}" aria-label="Khan Mebel, на главную">{inner}</a>'

def org_schema():
    return {
        "@context": "https://schema.org", "@type": "FurnitureStore", "@id": DOMAIN + "/#org",
        "name": "Khan Mebel", "alternateName": ["Хан Мебель", "Khan Mebel Astana"],
        "description": "Изготовление кухонь и корпусной мебели на заказ в Астане: кухни, шкафы, гардеробные, прихожие, мебель под ключ.",
        "url": DOMAIN + "/", "logo": DOMAIN + "/assets/img/logo.jpg", "image": DOMAIN + "/assets/img/logo.jpg",
        "telephone": "+77001116291",
        "address": {"@type": "PostalAddress", "streetAddress": ADDR, "addressLocality": "Астана",
                    "addressRegion": "Сарыаркинский район", "postalCode": "Z11E3P7", "addressCountry": "KZ"},
        "geo": {"@type": "GeoCoordinates", "latitude": 51.183004, "longitude": 71.435401},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
            "opens": "10:00", "closes": "20:00"}],
        "areaServed": {"@type": "City", "name": "Астана"},
        "priceRange": "₸₸", "currenciesAccepted": "KZT",
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5", "bestRating": "5",
                            "ratingCount": "38", "reviewCount": "33"},
        "sameAs": [IG, GIS],
        "knowsLanguage": ["ru", "kk"],
    }

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def crumbs_schema(name, path):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Khan Mebel", "item": DOMAIN + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": DOMAIN + "/" + path}]}

def ld(*objs):
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>' for o in objs)

def faq_html(faqs):
    return '<div class="faq">' + "".join(
        f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs) + '</div>'

def meta(title, desc, path):
    url = DOMAIN + "/" + path
    return f'''<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="ru_KZ">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{DOMAIN}/assets/img/logo.jpg">
<meta name="google-site-verification" content="k0fBn6_nPx2JKuDDlRyQbcTxZKTbWe0KUqQUcY7fEe4">
<meta name="yandex-verification" content="66470a072bd67517">
<meta name="msvalidate.01" content="36BB16E19D0081905987D5816AE70E80">
<meta name="geo.region" content="KZ-AST"><meta name="geo.placename" content="Астана">
<meta name="geo.position" content="51.183004;71.435401"><meta name="ICBM" content="51.183004, 71.435401">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}"><link rel="stylesheet" href="assets/css/khan.css">'''

# ---------- данные ----------
REVIEWS = [
    ("Динара Т.", "Кухня + 2 шкафа", "По договору 15 дней, а сделали за 10 дней."),
    ("Эльмира Х.", "Кухня", "На месте составили 3Д чертеж и по стоимости сразу и договор составили."),
    ("Гаухар Н.", "Кухня и прихожая", "Абылайхан сам приехал на замер и принимал участие в сборке."),
    ("Салтанат К.", "Мебель на всю квартиру", "Реально Хан мебель, Ханское качество."),
    ("Перизат К.", "3 бөлмелі пәтер", "Уақытынан ерте алып келіп, жихаздарды толық құрып, реттестіріп кетті."),
    ("Эльмира М.", "Кухня, шкафы, гардеробная", "На связи находятся 24/7, всегда укладываются в обещанные сроки."),
    ("Сауле С.", "2 шкафа на балкон", "Изготовили быстро и качественно, установили намного раньше срока."),
    ("Ержан Г.", "Вторая квартира", "Ставлю мебель уже на второй квартире, все отлично."),
    ("Мира И.", "Шкаф в детскую", "Очень красиво и аккуратно сделано до мелочей."),
    ("Зарина А.", "Проект и материалы", "Сработали чётко, профессионально и без сюрпризов."),
    ("Индира М.", "Кухня, 4 шкафа, санузел", "Всё сделали быстро, качественно и очень красиво."),
    ("Айнура А.", "Үй жиһазы", "Енді бұйырса 2 үйіме тағы тапсырыс беріп жатырмын!"),
]

USP = [
    ("10 дней", "Сдаём раньше срока", "Срок фиксируем в договоре. Клиенты чаще всего отмечают, что мебель привезли раньше обещанного.", REVIEWS[0]),
    ("1 выезд", "Замер, 3D-проект и договор за одну встречу", "Приезжаем на замер уже на следующий день, на месте рисуем 3D-проект и называем точную цену.", REVIEWS[1]),
    ("Лично", "Руководитель на вашем объекте", "Абылайхан сам выезжает на замер и контролирует сборку от начала до конца.", REVIEWS[2]),
    ("0", "Сюрпризов в смете", "Цена, материалы и сроки записаны в договоре. Итог не меняется после подписания.", REVIEWS[9]),
    ("24/7", "Всегда на связи", "Отвечаем в WhatsApp, советуем практичные решения и честно говорим, где можно сэкономить.", REVIEWS[5]),
    ("Под ключ", "Вся квартира у одного мастера", "Кухня, шкафы, гардеробная, прихожая, детская и санузел: один проект и один договор.", REVIEWS[7]),
]

FAQ_HOME = [
    ("Сколько стоит кухня на заказ в Астане?", "Ориентир: от 180 000 ₸ за погонный метр для кухни из ЛДСП с верхними и нижними шкафами. Прямая кухня 3 метра обычно выходит от 540 000 ₸. Точную цену называем на замере вместе с 3D-проектом. Предварительно посчитать можно в калькуляторе на сайте."),
    ("За сколько дней изготавливают мебель?", "Срок прописываем в договоре, обычно около 15 рабочих дней. Клиенты в отзывах на 2ГИС отмечают, что мебель часто привозим раньше: например, за 10 дней вместо 15."),
    ("Как быстро вы приедете на замер?", "Обычно на следующий день после заявки. На замере сразу делаем 3D-проект, считаем стоимость и при желании заключаем договор. Второй раз встречаться не нужно."),
    ("Делаете мебель на всю квартиру?", "Да. Делаем мебель под ключ: кухню, шкафы, гардеробные, прихожие, детские, шкафы в санузел и на балкон одним проектом и договором."),
    ("Где находится Khan Mebel?", f"Астана, {ADDR}, район Сарыарка. Работаем с 10:00 до 20:00. Удобнее всего написать в WhatsApp: {PHONE_H}."),
    ("Сколько стоит мебель на заказ в Астане и есть ли недорогие варианты?", "Шкафы и гардеробные от 60 000 ₸ за м², кухни от 180 000 ₸ за погонный метр. Недорогой вариант: ЛДСП со стандартной фурнитурой. Все цены есть на странице «Цены», свой вариант можно посчитать в калькуляторе."),
    ("Где почитать отзывы и посмотреть работы?", "Отзывы есть на странице «Отзывы» и в 2ГИС (рейтинг 5,0 по 38 оценкам). Свежие проекты и видео смотрите в разделе «Проекты» и в Instagram @khan_mebel.kz."),
    ("Можно общаться на казахском языке?", "Да, отвечаем на русском и казахском. Қазақ тілінде де сөйлесеміз."),
]

PROJECTS = [
    ("kitchen4-oak", "kitchen", "big", "Кухня до потолка: фасады под дуб, белые верхние шкафы и колонна под технику Bosch"),
    ("bedroom2-arch", "bedroom", "tall", "Шкаф с фрезеровкой-арками и латунными ручками"),
    ("kitchen5-vitrine", "kitchen", "tall", "Белая кухня с рифлёными антресолями и витриной с подсветкой"),
    ("bath5-blue", "bath", "tall", "Санузел: голубой шкаф над инсталляцией, ниша из дуба и тумба с рифлёным фасадом"),
    ("living3-tv", "living", "tall", "Гостиная: колонна с подсвеченной витриной, ТВ-панель и подвесная тумба"),
    ("hall3-closed", "hall", "tall", "Прихожая: шкаф до потолка с ручками-профилями и панель под дуб с полкой"),
    ("kitchen-green", "kitchen", "big", "Кухня с рифлёными фасадами шалфейного цвета и кварцевой столешницей"),
    ("living-tv", "living", "wide", "ТВ-зона с парящей дубовой панелью, подсветкой и биокамином"),
    ("hall-oak", "hall", "tall", "Прихожая из рифлёного дуба с сиденьем и латунными крючками"),
    ("kitchen-side", "kitchen", "", "Шкафы-витрины с полками из дуба по бокам кухни"),
    ("kids-room", "kids", "wide", "Детская на двоих: шкафы с арками, стол у окна и реечная панель"),
    ("kitchen-top", "kitchen", "", "Кварцевая столешница и латунные ручки"),
    ("bedroom-wardrobe", "bedroom", "tall", "Шкаф в спальне с дубовой нишей и подсветкой"),
    ("kitchen-glass", "kitchen", "", "Скрытая LED-подсветка под верхними шкафами"),
    ("kids-wardrobe", "kids", "", "Распашной шкаф с фрезеровкой-арками"),
    ("hall-bench", "hall", "", "Ниша с подсветкой для ключей и мелочей"),
    ("kitchen-column", "kitchen", "tall", "Колонна под встроенную технику до потолка"),
    ("bath-niche", "bath", "", "Шкаф над инсталляцией с цветной нишей"),
    ("bedroom-vanity", "bedroom", "", "Туалетный столик и скамья из дуба"),
    ("kitchen2-corner", "kitchen", "tall", "Угловая кухня до потолка: матовые фасады, рифлёные антресоли и витрина с подсветкой"),
    ("study-desk", "kids", "big", "Комната школьника: стол вдоль окна, стеллажи из дуба и шкаф с фрезеровкой-арками"),
    ("hall2-wardrobe", "hall", "tall", "Прихожая: распашной шкаф до потолка, ниша с крючками и сиденье с ящиками"),
    ("kitchen3-straight", "kitchen", "tall", "Прямая кухня в два яруса до потолка с фасадами в стиле шейкер"),
    ("bath2-cabinet", "bath", "tall", "Санузел: рифлёный шкаф над инсталляцией и подвесная тумба"),
    ("wardrobe-arch", "bedroom", "tall", "Шкаф цвета шалфей с фрезеровкой-арками и антресолями"),
    ("living2-tv", "living", "tall", "ТВ-тумба с декоративной фрезеровкой и витрина с подсветкой"),
    ("closet-laundry", "wardrobe", "tall", "Гардеробная-постирочная: ниша под стиральную и сушильную машины, полки и ящики"),
    ("kitchen2-oven", "kitchen", "tall", "Колонна под духовку и микроволновку, вытяжка спрятана в шкаф"),
    ("study-angle", "kids", "tall", "Стеллажи по бокам окна и столешница во всю стену"),
    ("closet-walnut", "wardrobe", "tall", "Гардеробная из ЛДСП цвета орех: открытые полки и выдвижные ящики"),
    ("kitchen2-vitrine", "kitchen", "tall", "Витрина в алюминиевой раме с тонированным стеклом"),
    ("study-side", "kids", "tall", "Шкаф и открытый стеллаж в детской"),
    ("kitchen3-drawers", "kitchen", "tall", "Фасады шейкер и выдвижные ящики с доводчиками"),
    ("bath2-vanity", "bath", "tall", "Подвесная тумба с рифлёными ящиками"),
    ("detail-shelves", "wardrobe", "tall", "Внутреннее наполнение шкафа: полки под размеры вещей"),
    ("study-drawers", "kids", "tall", "Тумба с ящиками под письменным столом"),
    ("detail-socket", "kids", "tall", "Выдвижная розетка с USB, встроенная в столешницу"),
    ("kitchen5-straight", "kitchen", "tall", "Прямая кухня с колонной под духовку и микроволновку, латунная вставка на антресолях"),
    ("bedroom3-circle", "bedroom", "tall", "Шкаф с круглой фрезеровкой и кольцевыми ручками"),
    ("bedroom3-open", "bedroom", "tall", "Наполнение шкафа: полки, штанга и выдвижные ящики цвета орех"),
    ("bedroom2-open", "bedroom", "tall", "Шкаф изнутри: полки, ящики и отделение для одежды"),
    ("wardrobe-wall", "wardrobe", "tall", "Стена шкафов до потолка с антресолями и ручками-профилями"),
    ("hall3-open", "hall", "tall", "Прихожая изнутри: полки, ящики и штанга для верхней одежды"),
    ("vanity-mirror", "bedroom", "tall", "Подвесной туалетный столик и зеркало с LED-подсветкой"),
    ("bath3-cabinet", "bath", "tall", "Санузел: шкафы под дуб до потолка над инсталляцией"),
    ("bath3-niche", "bath", "tall", "Открытые полки-ниши из дуба в санузле"),
    ("bath4-pink", "bath", "tall", "Санузел: шкафы и тумба под раковину пудрового цвета"),
]
FILTERS = [("all", "Все"), ("kitchen", "Кухни"), ("living", "Гостиные"), ("hall", "Прихожие"), ("kids", "Детские"), ("bedroom", "Спальни"), ("wardrobe", "Гардеробные"), ("bath", "Санузлы")]

def gallery_html(limit=None):
    f = "".join(f'<button type="button" data-f="{k}" aria-pressed="{"true" if k=="all" else "false"}">{t}</button>' for k, t in FILTERS)
    shots = "".join(
        f'''<button type="button" class="shot {size}" data-cat="{cat}" data-full="assets/media/{n}.jpg" data-cap="{cap}"><img src="assets/media/{n}{"" if size=="big" else "-s"}.jpg" alt="{cap}, Khan Mebel, Астана" loading="lazy" decoding="async"><span class="cap">{cap}</span></button>'''
        for n, cat, size, cap in (PROJECTS[:limit] if limit else PROJECTS))
    return f'<div class="filters" role="group" aria-label="Фильтр проектов">{f}</div><div class="gallery" id="gallery">{shots}</div>'

SOUND_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M18.5 5.5a9 9 0 0 1 0 13"/></svg>'
REELS = [
    ("kitchen-tour", "Обзор кухни", "Абылайхан показывает, как устроены ящики, сушка и колонна под технику."),
    ("client-review", "Отзыв клиентки", "Хозяйка квартиры рассказывает, как прошли замер, проект и сборка."),
    ("apartment-tour", "Тур по квартире", "Вся мебель квартиры под ключ: гостиная, спальни, детская, санузлы."),
]
def reels_html():
    return '<div class="reels">' + "".join(f'''<article class="reel"><div class="reel-frame">
<video src="assets/media/{n}.mp4" poster="assets/media/{n}.jpg" muted loop playsinline preload="none" aria-label="{t}"></video>
<button class="reel-sound" type="button" aria-label="Включить звук: {t}">{SOUND_SVG}<span>Со звуком</span></button></div>
<h3>{t}</h3><p>{d}</p></article>''' for n, t, d in REELS) + '</div>'

PAGE_PHOTOS = {
    "kuhni-na-zakaz-astana.html": [("kitchen-green", "Кухня на заказ с рифлёными фасадами, Астана"), ("kitchen-top", "Кварцевая столешница"), ("kitchen-glass", "Подсветка под шкафами")],
    "mebel-na-zakaz-astana.html": [("hall-oak", "Прихожая на заказ из дуба, Астана"), ("kids-wardrobe", "Шкаф в детскую"), ("bedroom-wardrobe", "Шкаф в спальню")],
    "mebel-pod-klyuch-astana.html": [("living-tv", "Мебель под ключ: ТВ-зона, Астана"), ("kids-room", "Детская"), ("hall-bench", "Прихожая")],
}
def photo_strip(path):
    ph = PAGE_PHOTOS.get(path)
    if not ph:
        return ""
    imgs = "".join(f'<img src="assets/media/{n}{"" if i==0 else "-s"}.jpg" alt="{a}" loading="lazy">' for i, (n, a) in enumerate(ph))
    return f'<div class="wrap"><div class="photo-strip">{imgs}</div></div>'

CALC_HTML = open(os.path.join(ROOT, 'src', 'partials', 'calculator.html'), encoding='utf-8').read()
FAN = ["living-tv", "kitchen2-corner", "kitchen-green", "hall2-wardrobe", "study-desk"]  # на телефоне видны 2-4
FAN_HTML = '<div class="fan" aria-hidden="true">' + "".join(f'<div class="card"><img src="assets/media/{n}-s.jpg" alt=""></div>' for n in FAN) + '</div>'

STATS = [("5,0", "Рейтинг в 2ГИС по 38 оценкам"), ("10", "дней: сдали кухню вместо 15 по договору"),
         ("1", "встреча: замер, 3D-проект и договор"), ("24/7", "на связи в WhatsApp")]
STAGE = ('<section class="stage dark" id="stage"><div class="stage-pin"><span class="stage-mark">(02)</span>'
         '<h2 class="giant">Ханское качество</h2>'
         '<div class="stage-video"><video src="assets/media/apartment-tour.mp4" poster="assets/media/apartment-tour.jpg" muted loop playsinline autoplay preload="metadata" aria-label="Тур по квартире с мебелью Khan Mebel"></video></div>'
         + "".join(f'<div class="stat s{i+1}"><b>{n}</b><span>{t}</span></div>' for i, (n, t) in enumerate(STATS))
         + '</div><div class="stage-copy"><span class="slash">// Так нас называют клиенты</span>'
         '<p>«Реально Хан мебель, Ханское качество». Мы взяли эти слова из отзыва и сделали их своим стандартом: точные размеры, аккуратная сборка и сроки, которые мы держим.</p>'
         '<span class="mark">Салтанат К., отзыв в 2ГИС</span></div></section>')

PILLARS = [
    ("1", "// Быстро", "Замер завтра, проект сразу", "Приезжаем на следующий день, рисуем 3D на месте и называем цену.", REVIEWS[1]),
    ("2", "// Честно", "Цена не меняется после договора", "Материалы, фурнитура и сроки записаны в договоре.", REVIEWS[9]),
    ("3", "// Лично", "Руководитель на объекте", "Абылайхан сам приезжает на замер и следит за сборкой.", REVIEWS[2]),
]
def pillars_html():
    return '<div class="pillars">' + "".join(f'''<article class="pillar"><span class="n">{n}</span><span class="slash">{s}</span><h3>{t}</h3><p>{d}</p><blockquote>«{r[2]}»<cite>{r[0]}, 2ГИС</cite></blockquote></article>''' for n, s, t, d, r in PILLARS) + '</div>'

FLOAT = [("c1", "bath-niche"), ("c2", "kids-room"), ("c3", "kitchen-side"), ("c4", "hall-bench"), ("c5", "kitchen-top")]
SVC6 = [
    ("kuhni-na-zakaz-astana.html", "Кухни", "Прямые, угловые, с островом. ЛДСП, МДФ в плёнке и в краске.", "от 180 000 ₸ / м"),
    ("mebel-na-zakaz-astana.html", "Шкафы и гардеробные", "Распашные, в нишу и до потолка, с продуманным наполнением.", "от 60 000 ₸ / м²"),
    ("mebel-na-zakaz-astana.html", "Прихожие", "Шкаф, обувница и сиденье одним модулем.", "от 85 000 ₸ / м"),
    ("mebel-na-zakaz-astana.html", "Детские и спальни", "Шкафы, столы и стеллажи под вашу комнату.", "по проекту"),
    ("mebel-na-zakaz-astana.html", "ТВ-зоны и санузлы", "Панели, тумбы, шкафы над инсталляцией.", "от 70 000 ₸ / м"),
    ("mebel-pod-klyuch-astana.html", "Под ключ", "Вся квартира одним договором.", "от 980 000 ₸"),
]
def float_html():
    cards = "".join(f'<div class="fcard {c}" aria-hidden="true"><img src="assets/media/{n}-s.jpg" alt=""></div>' for c, n in FLOAT)
    rows = "".join(f'<a class="svc-row" href="{h}"><h3>{t}</h3><p>{d}</p><span class="price">{p}</span></a>' for h, t, d, p in SVC6)
    return f'''<section class="float-sec dark" id="services">{cards}<div class="wrap">
<div class="sec-title"><span class="mark">(05)</span><h2>Мебель для всей квартиры</h2><p class="lead">Образцы фасадов, столешниц и фурнитуры привозим на замер.</p></div>
<div class="svc-list">{rows}</div></div></section>'''


SPEC_K = ["Корпус из ЛДСП Томск или Ламарти", "Фасады из МДФ в плёнке или в краске", "Фурнитура GTV (Польша), все механизмы с доводчиками",
          "Ящики скрытого монтажа выдерживают 25-30 кг", "Гигиенический поддон", "Термопланки", "Подсветка", "Столешница ЛДСП Скиф или Кедр"]
SPEC_W = ["Корпус из ЛДСП Томск или Ламарти", "Фасады и видимые части из МДФ", "Фурнитура GTV (Польша)", "Турникеты",
          "Ящики: до 4 шт.", "Наполнение по вашему желанию"]
def spec_html():
    card = lambda t, sub, items: f'<article class="plan"><span class="name">{t}</span><p class="muted">{sub}</p><ul>' + "".join(f"<li>{x}</li>" for x in items) + '</ul></article>'
    return f'''<section id="spec" style="padding-top:0"><div class="wrap">
<div class="sec-title"><span class="slash">// Без сюрпризов</span><h2>Что входит в стоимость</h2><p class="lead">Материалы и фурнитура, из которых мы делаем мебель. Всё это записываем в договор.</p></div>
<div class="plans two">{card("Кухня", "Базовая комплектация", SPEC_K)}{card("Шкаф", "Базовая комплектация", SPEC_W)}</div>
</div></section>'''


MATS = [
    ("mat-mdf", "МДФ", "Фасады и видимые части",
     "Плотная однородная плита из мелкой древесной фибры. Хорошо держит фрезеровку и покраску, торец ровный и не крошится.",
     ["Фасады кухонь и шкафов", "В плёнке или в краске, любой цвет", "Фрезеровка: рамка, арки, рифление"]),
    ("mat-ldsp", "ЛДСП", "Корпуса и столешницы",
     "Древесно-стружечная плита с прочным ламинированным покрытием. Крепко держит крепёж и не боится ежедневной нагрузки.",
     ["Корпуса из ЛДСП Томск или Ламарти", "Столешницы из ЛДСП Скиф или Кедр", "Декоры под дерево, камень и однотонные"]),
]
def mat_html(pad=' style="padding-top:0"'):
    cards = "".join(f'''<article class="mat-card"><img src="assets/media/{img}.jpg" alt="{name}, срез плиты, материал для мебели Khan Mebel" loading="lazy" width="869" height="1010">
<div class="mat-body"><span class="mat-tag">{role}</span><h3>{name}</h3><p>{text}</p><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></div></article>''' for img, name, role, text, items in MATS)
    return f'''<section id="materials"{pad}><div class="wrap">
<div class="sec-title"><span class="slash">// Материалы</span><h2>МДФ и ЛДСП</h2><p class="lead">Из чего сделана ваша мебель и почему мы сочетаем два материала.</p></div>
<div class="mats">{cards}</div>
</div></section>'''

PLANS = [
    ("", "Кухня", "180 000 ₸", "за погонный метр", ["Корпус ЛДСП Томск / Ламарти, фасады МДФ", "Фурнитура GTV (Польша) с доводчиками", "Подсветка, термопланки, поддон", "Замер, 3D-проект, доставка и сборка"], "btn-ink", "Рассчитать кухню", "#calc"),
    ("featured", "Под ключ", "980 000 ₸", "за однокомнатную", ["Кухня, шкаф, прихожая", "Один проект и один договор", "Единый стиль всех комнат", "Руководитель ведёт объект"], "btn-gold", "Обсудить проект", WA),
    ("", "Шкаф", "60 000 ₸", "за м² (ширина × высота)", ["Корпус ЛДСП Томск / Ламарти", "Фасады ЛДСП или МДФ в плёнке (от 80 000&nbsp;₸/м²)", "Фурнитура GTV (Польша), турникеты", "До 4 ящиков, наполнение по желанию"], "btn-ink", "Рассчитать шкаф", "#calc"),
]
def plans_html():
    out = []
    for cls, name, price, unit, items, btn, label, href in PLANS:
        tgt = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        lis = "".join(f"<li>{x}</li>" for x in items)
        out.append(f'<article class="plan {cls}"><span class="name">{name}</span><span class="price">от {price}<small>{unit}</small></span><ul>{lis}</ul><a class="btn {btn}" href="{href}"{tgt}>{label}</a></article>')
    return '<div class="plans">' + "".join(out) + '</div>'

CALC6 = (CALC_HTML.replace("{{WA_NUM}}", WA_NUM)
         .replace('<span class="qc-title">Калькулятор <em>за 30 секунд</em></span>', '<span class="qc-title">Калькулятор мебели</span>'))

def review_cards6(items):
    return "".join(f'''<article class="rev"><p>«{t}»</p><footer><span class="who">{n}</span><span>{w}</span></footer></article>''' for n, w, t in items)

idx_title = "Кухни и мебель на заказ в Астане | Khan Mebel"
idx_desc = "Кухни, шкафы, гардеробные и мебель под ключ в Астане. Калькулятор стоимости онлайн, замер и 3D-проект за одну встречу, изготовление от 10 дней. Рейтинг 5.0 в 2ГИС."
USP_SHORT = '''<ul>
<li><b>Замер, 3D-проект и договор за один выезд.</b> Приезжаем на следующий день после заявки.</li>
<li><b>Срок в договоре, и часто раньше.</b> Клиентка в 2ГИС: по договору 15 дней, сделали за 10.</li>
<li><b>Руководитель лично на объекте.</b> Абылайхан сам выезжает на замер и следит за сборкой.</li>
<li><b>Без сюрпризов.</b> Цена, материалы и фурнитура зафиксированы в договоре.</li>
<li><b>Чистая сборка.</b> Аккуратно собираем, регулируем фасады и убираем за собой.</li>
</ul>'''

def table(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="table-wrap"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'

def offer(name, price_from, unit):
    return {"@context": "https://schema.org", "@type": "Service", "serviceType": name,
            "provider": {"@id": DOMAIN + "/#org"}, "areaServed": {"@type": "City", "name": "Астана"},
            "offers": {"@type": "Offer", "priceCurrency": "KZT", "price": price_from,
                       "priceSpecification": {"@type": "UnitPriceSpecification", "price": price_from,
                                              "priceCurrency": "KZT", "unitText": unit}}}

# Кухни

# ======================================================================
#  Каркас страниц
# ======================================================================
NAV = [("proekty.html", "Проекты"), ("kuhni-na-zakaz-astana.html", "Кухни"), ("mebel-na-zakaz-astana.html", "Мебель на заказ"),
       ("mebel-pod-klyuch-astana.html", "Под ключ"), ("ceny.html", "Цены"), ("otzyvy.html", "Отзывы"), ("kontakty.html", "Контакты")]

GSAP = ('<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>'
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>')

def header(current=""):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == current else ""}>{t}</a>' for h, t in NAV)
    return f'''<header class="top" id="top-bar"><div class="wrap">
{lockup("", "./")}
<nav class="nav" aria-label="Разделы">{links}</nav>
<div class="top-cta"><a class="plain" href="{WA}" target="_blank" rel="noopener">WhatsApp</a><a class="btn btn-ink" href="kalkulyator.html">Калькулятор цены</a>
<details class="menu"><summary aria-label="Меню"><span></span><span></span></summary><nav class="menu-list" aria-label="Меню">{links}<a href="kalkulyator.html">Калькулятор</a></nav></details></div>
</div></header>'''

def footer():
    return f'''<footer class="foot"><div class="wrap">
<div style="display:grid;gap:18px;justify-items:start">{lockup("", "./")}
<p>Кухни и корпусная мебель на заказ в Астане. Замер, 3D-проект и договор за одну встречу.</p></div>
<div><h4>Разделы</h4><ul>
<li><a href="kuhni-na-zakaz-astana.html">Кухни на заказ</a></li>
<li><a href="mebel-na-zakaz-astana.html">Мебель на заказ</a></li>
<li><a href="mebel-pod-klyuch-astana.html">Мебель под ключ</a></li>
<li><a href="kalkulyator.html">Калькулятор</a></li>
<li><a href="proekty.html">Проекты</a> · <a href="ceny.html">Цены</a> · <a href="otzyvy.html">Отзывы</a></li></ul></div>
<div><h4>Контакты</h4><ul>
<li>Астана, {ADDR}</li>
<li>WhatsApp: <span style="user-select:all">{PHONE_H}</span></li>
<li>Ежедневно 10:00-20:00</li>
<li><a href="{IG}" target="_blank" rel="noopener">Instagram</a> · <a href="{GIS}" target="_blank" rel="noopener">2ГИС</a></li></ul></div>
<div class="foot-word" aria-hidden="true">khan<span>/</span>mebel</div>
</div></footer>
<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="Написать в WhatsApp">{CHAT_SVG}<span>WhatsApp</span></a>'''

YM_HEAD = """<!-- Yandex.Metrika counter -->
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){
        m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    })(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=113868698', 'ym');

    ym(113868698, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});
</script>
<!-- /Yandex.Metrika counter -->"""
YM_NOSCRIPT = '<noscript><div><img src="https://mc.yandex.ru/watch/113868698" style="position:absolute; left:-9999px;" alt="" /></div></noscript>'

# Чистые адреса без .html (на Vercel включено cleanUrls в vercel.json)
SLUGS = ["kalkulyator", "proekty", "kuhni-na-zakaz-astana", "mebel-na-zakaz-astana", "mebel-pod-klyuch-astana",
         "ceny", "otzyvy", "kontakty"]
def clean(s):
    s = re.sub(r'(?<![\w/.-])index\.html', '/', s)
    s = s.replace(DOMAIN + '//', DOMAIN + '/')
    return re.sub(r'\b(' + '|'.join(SLUGS) + r')\.html\b', r'\1', s)

def doc(path, title, desc, body, schemas=(), calc=False, anim=True):
    scripts = (GSAP if anim else "") + ('<script src="assets/js/calculator.js" defer></script>' if calc else "") + \
        '<script src="assets/js/site.js" defer></script>' + ('<script src="assets/js/animations.js" defer></script>' if anim else "")
    html = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
{meta(title, desc, path)}
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#f1f1f1">
{ld(org_schema(), *schemas)}
{YM_HEAD}
</head>
<body>
{YM_NOSCRIPT}
<div id="top"></div>
{header(path)}
<main>
{body}
</main>
{footer()}
{scripts}
</body>
</html>
'''
    with open(os.path.join(OUT, path or "index.html"), "w", encoding="utf-8") as f:
        f.write(clean(html))
    PAGES.append(path)

PAGES = []

def page_head(h1, lead, crumb, cta=True):
    btns = f'''<div class="hero-cta"><a class="btn btn-ink" href="kalkulyator.html">Рассчитать стоимость</a>
<a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{CHAT_SVG} Написать в WhatsApp</a></div>''' if cta else ""
    return f'''<section class="hero-plain"><div class="wrap"><div class="hero-text">
<nav class="crumbs" aria-label="Навигация"><a href="./">Khan Mebel</a> / {crumb}</nav>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
{btns}
<div class="rating"><span class="stars" aria-hidden="true">★★★★★</span><span><b>5,0</b> в 2ГИС · 38 оценок</span></div>
</div></div></section>'''

# ======================================================================
#  Разделы (используются на нескольких страницах)
# ======================================================================
def sec_hero():
    return f'''<section class="hero"><div class="wrap">
<p class="pre">Мебель, в которую хочется возвращаться</p>
<h1>Кухни и мебель на заказ в <u>Астане</u></h1>
<p class="lead">Своё производство. Замер, 3D-проект и договор за одну встречу. Изготовление от 10 дней.</p>
<div class="hero-cta"><a class="btn btn-ink" href="#calc">Рассчитать стоимость</a><a class="btn btn-paper" href="#video">Смотреть видео</a></div>
<div class="rating"><span class="stars" aria-hidden="true">★★★★★</span><span><b>5,0</b> в 2ГИС · 38 оценок · 33 отзыва</span></div>
</div>{FAN_HTML}</section>'''

def sec_video(mark="(01)", pad=""):
    return f'''<section id="video"{pad}><div class="wrap">
<div class="sec-title"><span class="mark">{mark}</span><span class="slash">// Без постановки</span><h2>Смотрите вживую</h2><p class="lead">Обзор кухни, отзыв клиентки и тур по квартире. Включите звук на любом ролике.</p></div>
{reels_html()}
</div></section>'''

def sec_projects(mark="(03)", more=True):
    link = '<div class="center" style="margin-top:32px;text-align:center"><a class="btn btn-ink" href="proekty.html">Все проекты</a></div>' if more else ""
    return f'''<section id="projects"><div class="wrap">
<div class="sec-title"><span class="mark">{mark}</span><h2>Наши проекты</h2><p class="lead">Реальные квартиры в Астане. Нажмите на фото, чтобы рассмотреть детали.</p></div>
{gallery_html(16 if more else None)}{link}
</div></section>'''

def sec_pillars():
    return f'''<section id="why" style="padding-top:0"><div class="wrap">
<div class="sec-title"><span class="mark">(04)</span><h2>Быстро. Честно. Лично.</h2></div>
{pillars_html()}
</div></section>'''

def sec_calc(mark="", standalone=False):
    m = f'<span class="mark">{mark}</span>' if mark else ""
    intro = ('''<div class="calc-intro"><span class="slash">// Как это работает</span>
<ol class="calc-steps"><li><span><b>Выберите</b> тип мебели, форму и фасады.</span></li><li><span><b>Добавьте</b> позиции в смету, так можно посчитать всю квартиру.</span></li><li><span><b>Отправьте</b> смету в WhatsApp, мы уточним детали и назначим замер.</span></li></ol></div>''' if standalone else
             f'''<div class="calc-intro">{m}<span class="slash">// Цена за 30 секунд</span><h2>Посчитайте свою мебель</h2>
<p class="lead">Выберите форму, размеры и фасады. Добавьте несколько позиций в смету и отправьте её нам в WhatsApp.</p></div>''')
    pad = ' style="padding-top:0"' if standalone else ""
    return f'''<section class="calc-sec" id="calc-sec"{pad}><div class="wrap calc-grid">
{intro}
{CALC6}
</div></section>'''

def sec_reviews(pad=' style="padding-top:0"', more=True):
    link = f'<a class="link-btn" style="margin-left:8px" href="{"otzyvy.html" if more else GIS_REV}"{"" if more else " target=\"_blank\" rel=\"noopener\""}>Все отзывы</a>'
    return f'''<section id="reviews"{pad}><div class="wrap">
<div class="rev-head"><div class="rev-score"><b>5,0</b><span>38 оценок и 33 отзыва в 2ГИС</span></div>
<div class="rev-nav"><button class="arrow" type="button" data-rev="-1" aria-label="Предыдущие отзывы">←</button><button class="arrow" type="button" data-rev="1" aria-label="Следующие отзывы">→</button>{link}</div></div>
<div class="rev-track" id="rev-track" tabindex="0" aria-label="Отзывы клиентов">{review_cards6(REVIEWS)}</div>
</div></section>'''

def sec_prices(mark="(06)", pad=' style="padding-top:0"'):
    return f'''<section id="prices"{pad}><div class="wrap">
<div class="sec-title"><span class="mark">{mark}</span><h2>Цены</h2><p class="lead">Ориентиры для бюджета. Точную стоимость фиксируем в договоре после замера.</p></div>
{plans_html()}
</div></section>'''

def sec_lead():
    return f'''<section id="lead" class="dark"><div class="wrap cta">
<div style="display:grid;gap:18px"><span class="slash">// Замер и 3D-проект</span><h2>Запишитесь на замер</h2><p class="lead">Приедем на следующий день, привезём образцы и сразу покажем проект в 3D.</p></div>
<form class="form" id="cta_form" style="color:var(--ink);--muted:#7a7a7a">
<div class="line-in"><label for="cta_name">Имя</label><input id="cta_name" autocomplete="name" placeholder="Айгерим"></div>
<div class="line-in"><label for="cta_phone">Телефон</label><input id="cta_phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="+7 7__ ___ __ __"></div>
<div class="line-in"><label for="cta_what">Что нужно</label><select id="cta_what"><option>Кухня на заказ</option><option>Шкаф или гардеробная</option><option>Прихожая</option><option>Мебель под ключ на всю квартиру</option><option>Другое</option></select></div>
<div class="form-foot"><a class="btn btn-wa" id="cta_send" href="https://wa.me/{WA_NUM}" target="_blank" rel="noopener">{CHAT_SVG} Отправить в WhatsApp</a><span class="note">Ответим с 10:00 до 20:00</span></div>
</form>
</div></section>'''

def sec_faq(faqs):
    return f'''<section id="faq"><div class="wrap">
<div class="sec-title"><span class="slash">// Вопросы и ответы</span><h2>Частые вопросы</h2></div>
{faq_html(faqs)}
</div></section>'''

def sec_contacts(pad=' style="padding-top:0"', h="Приезжайте в шоурум"):
    return f'''<section id="contacts"{pad}><div class="wrap contact">
<div><h2>{h}</h2>
<dl><dt>Адрес</dt><dd>Астана, {ADDR}, район Сарыарка, Z11E3P7</dd>
<dt>Часы</dt><dd>Ежедневно 10:00-20:00</dd>
<dt>WhatsApp</dt><dd style="user-select:all">{PHONE_H}</dd>
<dt>Instagram</dt><dd><a href="{IG}" target="_blank" rel="noopener">@khan_mebel.kz</a></dd>
<dt>2ГИС</dt><dd><a href="{GIS}" target="_blank" rel="noopener">Khan Mebel, рейтинг 5,0</a></dd></dl>
<a class="btn btn-ink" href="{GIS_ROUTE}" target="_blank" rel="noopener">Построить маршрут в 2ГИС</a></div>
<div class="cta-box"><h3>О компании</h3>
<p>Khan Mebel: мебельное производство в Астане. Делаем кухни, шкафы, гардеробные, прихожие и мебель под ключ. Руководитель Абылайхан сам выезжает на замеры и следит за сборкой. Изготовление занимает 10-15 рабочих дней. Рейтинг 5,0 по 38 оценкам в 2ГИС (октябрь 2026).</p>
<a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener">{CHAT_SVG} Написать в WhatsApp</a></div>
</div></section>'''

WEBSITE = {"@context": "https://schema.org", "@type": "WebSite", "name": "Khan Mebel", "url": DOMAIN + "/", "inLanguage": "ru-KZ"}

# ======================================================================
#  Страницы
# ======================================================================
# Главная
doc("", "Кухни и мебель на заказ в Астане | Khan Mebel",
    "Кухни, шкафы, гардеробные и мебель под ключ в Астане. Калькулятор стоимости онлайн, замер и 3D-проект за одну встречу, изготовление от 10 дней. Рейтинг 5.0 в 2ГИС.",
    sec_hero() + sec_video() + STAGE + sec_projects() + sec_pillars() + float_html() + sec_calc() +
    sec_reviews() + sec_prices() + spec_html() + mat_html() + sec_lead() + sec_faq(FAQ_HOME) + sec_contacts(),
    (faq_schema(FAQ_HOME), WEBSITE), calc=True)

# Калькулятор
FAQ_CALC = [FAQ_HOME[0],
    ("Насколько точен онлайн-калькулятор?", "Калькулятор даёт ориентир с разбросом около ±10%. Точную цену называем на замере вместе с 3D-проектом и фиксируем в договоре."),
    ("Что входит в цену из калькулятора?", "Кухня: корпус ЛДСП Томск или Ламарти, фасады МДФ, фурнитура GTV (Польша) с доводчиками, ящики скрытого монтажа, гигиенический поддон, термопланки, подсветка и столешница ЛДСП Скиф или Кедр. Шкаф: корпус ЛДСП, фасады и видимые части из МДФ, фурнитура GTV, турникеты, до 4 ящиков. Плюс доставка и сборка. Бытовая техника, мойка и смеситель в цену не входят."),
    ("Можно посчитать сразу несколько предметов?", "Да. Нажмите «Добавить в смету» после каждого расчёта, и смета соберётся внизу и целиком отправится нам в WhatsApp.")]
doc("kalkulyator.html", "Калькулятор стоимости кухни и мебели | Khan Mebel, Астана",
    "Онлайн-калькулятор стоимости кухни, шкафа, прихожей и ТВ-зоны в Астане. Цена за 30 секунд, смета в WhatsApp, точный расчёт на бесплатном замере.",
    page_head("Калькулятор стоимости мебели", "Посчитайте кухню, шкаф, прихожую или ТВ-зону за 30 секунд. Соберите смету из нескольких позиций и отправьте её нам.", "Калькулятор", cta=False)
    + sec_calc(standalone=True) + sec_prices(mark="", pad="") + spec_html() + sec_faq(FAQ_CALC) + sec_lead(),
    (faq_schema(FAQ_CALC), crumbs_schema("Калькулятор", "kalkulyator.html")), calc=True)

# Проекты
doc("proekty.html", "Проекты Khan Mebel: фото кухонь и мебели на заказ в Астане",
    "Фото и видео реальных проектов Khan Mebel в Астане: кухни, прихожие, детские, спальни, ТВ-зоны и санузлы. Мебель на заказ и под ключ.",
    page_head("Наши проекты", "Кухни, прихожие, детские, спальни и ТВ-зоны, которые мы сделали для квартир в Астане.", "Проекты")
    + sec_projects(mark="", more=False) + sec_video(mark="", pad=' style="padding-top:0"') + sec_lead(),
    (crumbs_schema("Проекты", "proekty.html"),))

# Отзывы
doc("otzyvy.html", "Мебель на заказ Астана: отзывы клиентов, 5.0 в 2ГИС | Khan Mebel",
    "Мебель на заказ в Астане: отзывы клиентов Khan Mebel. 38 оценок и рейтинг 5.0 в 2ГИС. Кухни, шкафы, мебель под ключ. Сроки, качество, сервис.",
    page_head("Отзывы о мебели на заказ", "38 оценок и 33 отзыва в 2ГИС. Средний рейтинг 5,0 из 5. Короткие выдержки ниже, полные тексты на странице компании в 2ГИС.", "Отзывы")
    + sec_reviews(pad="", more=False) + sec_pillars() + sec_video(mark="", pad=' style="padding-top:0"') + sec_lead(),
    (crumbs_schema("Отзывы", "otzyvy.html"),))

# Цены
PRICE_TABLE = table(["Изделие", "Как считаем", "Цена"], [
    ["Кухня, фасады ЛДСП", "погонный метр", "от 180 000 ₸"], ["Кухня, МДФ в плёнке", "погонный метр", "от 250 000 ₸"], ["Кухня, МДФ в краске", "погонный метр", "от 300 000 ₸"],
        ["Шкаф, фасады ЛДСП", "м² (ширина × высота)", "от 60 000 ₸"], ["Шкаф, фасады МДФ в плёнке", "м² (ширина × высота)", "от 80 000 ₸"],
    ["Гардеробная", "м² (ширина × высота)", "от 60 000 ₸"], ["Прихожая", "погонный метр", "от 85 000 ₸"],
    ["ТВ-зона", "погонный метр", "от 70 000 ₸"], ["Мебель под ключ, 1-комнатная", "квартира", "от 980 000 ₸"]])
doc("ceny.html", "Мебель на заказ Астана: цены 2026 | Khan Mebel",
    "Мебель на заказ в Астане: цены 2026. Кухни от 180 000 ₸ за погонный метр, шкафы от 60 000 ₸ за м², корпусная мебель под ключ от 980 000 ₸. Недорого, от производителя.",
    page_head("Мебель на заказ в Астане: цены", "Ориентиры для бюджета. Точную стоимость считаем на замере и фиксируем в договоре.", "Цены")
    + sec_prices(mark="", pad="") + spec_html() + mat_html() + f'<section style="padding-top:0"><div class="wrap prose"><h2>Прайс-лист</h2>{PRICE_TABLE}<p>Цены ориентировочные. В них входят корпус, фасады, стандартная фурнитура с доводчиками, доставка и сборка. Посчитать свой вариант можно <a href="kalkulyator.html">в калькуляторе</a>.</p></div></section>'
    + sec_faq(FAQ_CALC) + sec_lead(),
    (faq_schema(FAQ_CALC), crumbs_schema("Цены", "ceny.html")))

# Контакты
doc("kontakty.html", "Контакты Khan Mebel: Астана, WhatsApp, Instagram",
    "Мебель на заказ в Астане: Khan Mebel, ул. Ыкылас Дукенулы, 31/2, район Сарыарка. Ежедневно 10:00-20:00. WhatsApp +7 700 111 62 91, Instagram @khan_mebel.kz.",
    page_head("Контакты", "Приезжайте в шоурум или позовите нас на замер, приедем на следующий день.", "Контакты", cta=False)
    + sec_contacts(pad="", h="Шоурум и производство") + sec_lead(),
    (crumbs_schema("Контакты", "kontakty.html"),), anim=False)

# SEO-страницы услуг
def page(path, title, desc, h1, crumb, intro, body, faqs, extra_ld=()):
    doc(path, title, desc,
        page_head(h1, intro, crumb) + photo_strip(path) +
        f'''<section style="padding-top:56px"><div class="wrap prose">
{body}
</div></section>
''' + (mat_html() if path in ("kuhni-na-zakaz-astana.html", "mebel-na-zakaz-astana.html") else "") + f'''<section class="band-light"><div class="wrap prose">
<h2 style="margin-top:0">Частые вопросы</h2>
{faq_html(faqs)}
<h2>Смотрите также</h2>
<div class="pills"><a href="kuhni-na-zakaz-astana.html">Кухни на заказ</a><a href="mebel-na-zakaz-astana.html">Мебель на заказ</a><a href="mebel-pod-klyuch-astana.html">Мебель под ключ</a><a href="kalkulyator.html">Калькулятор</a><a href="proekty.html">Проекты</a><a href="ceny.html">Цены</a><a href="otzyvy.html">Отзывы</a></div>
</div></section>''' + sec_lead(),
        (faq_schema(faqs), crumbs_schema(crumb, path), *extra_ld))

FAQ_K = [
    ("Сколько стоит изготовление кухни в Астане?", "Кухня из ЛДСП от 180 000 ₸ за погонный метр, МДФ в плёнке от 250 000 ₸, МДФ в краске от 300 000 ₸. Столешница считается отдельно. Прямая кухня 3 м из ЛДСП обычно стоит от 540 000 ₸."),
    ("Где купить кухню недорого в Астане?", "Сэкономить без потери качества помогает корпус и фасады из ЛДСП, столешница из ЛДСП с постформингом и стандартная фурнитура. На замере покажем, где экономия разумна, а где лучше не урезать."),
    ("Сколько дней делается кухня на заказ?", "Обычно 10-15 рабочих дней после подписания договора. Срок фиксируется в договоре."),
    ("Делаете угловые и П-образные кухни?", "Да: прямые, угловые, П-образные, с островом, с пеналами под технику и антресолями до потолка."),
    ("Доставляете кухни по Казахстану?", "Основная работа: Астана и пригород (Косшы, Коянды и др.). По другим городам Казахстана уточняйте в WhatsApp."),
]
page("kuhni-na-zakaz-astana.html",
     "Кухни на заказ в Астане от 180 000 ₸/п.м. | Khan Mebel",
     "Изготовление кухни на заказ в Астане: ЛДСП, МДФ в плёнке и МДФ в краске. Замер и 3D-проект за 1 выезд, срок от 10 дней. Кухни недорого от производителя, рейтинг 5.0 в 2ГИС.",
     "Кухни на заказ в Астане от производителя",
     "Кухни на заказ",
     "Изготавливаем кухни по вашим размерам: прямые, угловые и П-образные, из ЛДСП, МДФ в плёнке и МДФ в краске. Замер, 3D-проект и точная цена за одну встречу.",
     f'''<h2>Цены на кухни на заказ</h2>
<p>Цена за погонный метр включает комплект нижних и верхних шкафов высотой 720 мм с фасадами, корпусом и стандартной фурнитурой. Столешница, стеновая панель и подсветка считаются отдельно.</p>
{table(["Фасады", "Для кого", "Цена за п.м."], [
    ["ЛДСП", "Практичная кухня недорого, съёмная квартира", "от 180 000 ₸"],
    ["МДФ в плёнке ПВХ", "Фрезеровка, матовые и древесные текстуры", "от 250 000 ₸"],
    ["МДФ в краске", "Любой цвет, матовая или глянцевая покраска", "от 300 000 ₸"]])}
<p>Цены ориентировочные. Точную стоимость считаем на замере. Предварительно можно посчитать <a href="index.html#calc">в калькуляторе кухни</a>.</p>
<h2>Изготовление кухни: что входит</h2>
<ul><li>Выезд на замер и 3D-проект кухни на месте</li><li>Корпус ЛДСП Томск или Ламарти, фасады МДФ, фурнитура GTV (Польша) с доводчиками, ящики скрытого монтажа на 25-30 кг, гигиенический поддон, термопланки, подсветка, столешница ЛДСП Скиф или Кедр</li><li>Производство корпусов и фасадов в нашем цеху</li><li>Доставка, сборка, врезка мойки и варочной панели, установка встроенной техники</li></ul>
<h2>Почему кухни Khan Mebel</h2>
{USP_SHORT}
<h2>Кухни Астана недорого: как сэкономить без потери качества</h2>
<p>Самая большая экономия в фасадах: ЛДСП заметно дешевле МДФ в краске. Столешница из ЛДСП обходится в несколько раз дешевле искусственного камня. А вот петли и направляющие лучше брать с доводчиками: на них приходится вся ежедневная нагрузка.</p>
<h2>Купить кухню в Казахстане: заказ или готовая?</h2>
<p>Готовая кухня дешевле на старте, но редко встаёт точно в размер: остаются щели, не помещается техника. Кухня на заказ делается под ваши стены, трубы и розетки, поэтому служит дольше и использует каждый сантиметр.</p>''',
     FAQ_K, (offer("Изготовление кухни на заказ", "180000", "погонный метр"),))

# Мебель на заказ
FAQ_M = [
    ("Сколько стоит мебель на заказ в Астане?", "Шкаф с фасадами ЛДСП от 60 000 ₸ за м², с фасадами МДФ в плёнке от 80 000 ₸ за м², гардеробная от 60 000 ₸ за м² (площадь = ширина × высота), прихожая от 85 000 ₸ за погонный метр. Точную цену называем после замера."),
    ("Какие материалы используете?", "Корпус из ЛДСП Томск или Ламарти, фасады и видимые части - МДФ в плёнке или в краске. Фурнитура GTV (Польша), все механизмы с доводчиками. В шкафах турникеты, до 4 ящиков и наполнение по вашему желанию."),
    ("Сколько делается шкаф на заказ?", "В среднем 10-15 рабочих дней. Срок фиксируем в договоре."),
    ("Делаете мебель в санузел и на балкон?", "Да, делаем шкафы над инсталляцией, тумбы в санузел и шкафы на балкон по размерам."),
    ("Можно заказать мебель недорого?", "Да. Самый доступный вариант: корпус и фасады из ЛДСП со стандартной фурнитурой с доводчиками. На замере покажем, где можно сэкономить без потери качества, а где лучше не урезать."),
    ("Вы делаете деталировку мебели?", "Да, деталировку и карты раскроя делаем сами по 3D-проекту, это часть заказа. Поэтому детали приходят точно в размер и собираются без подгонки на месте."),
    ("Чем заказ у вас отличается от мебели с центрального рынка или OLX?", "Готовая мебель с рынка или объявления на OLX сделана под чужие размеры. Мы приезжаем на замер, рисуем 3D-проект под вашу квартиру, фиксируем цену и сроки в договоре, сами собираем и даём гарантию. Рейтинг 5,0 в 2ГИС можно проверить до заказа."),
    ("Где посмотреть ваши работы?", "В разделе «Проекты» на сайте и в Instagram @khan_mebel.kz: там новые кухни, шкафы и видео-обзоры квартир."),
]
page("mebel-na-zakaz-astana.html",
     "Корпусная мебель на заказ в Астане недорого: цены, отзывы | Khan Mebel",
     "Корпусная мебель на заказ в Астане от производителя: шкафы, гардеробные, прихожие, детские. Цены от 60 000 ₸/м², недорого, деталировка и 3D-проект на замере. Отзывы: 5.0 в 2ГИС.",
     "Корпусная мебель на заказ в Астане",
     "Мебель на заказ",
     "Изготовление корпусной мебели по вашим размерам: шкафы, гардеробные, прихожие, детские, ТВ-зоны, шкафы для санузла и балкона. Своё производство в Астане.",
     f'''<h2>Цены на мебель на заказ</h2>
{table(["Изделие", "Как считаем", "Цена"], [
    ["Шкаф, фасады ЛДСП", "м² (ширина × высота)", "от 60 000 ₸"],
    ["Шкаф, фасады МДФ в плёнке", "м² (ширина × высота)", "от 80 000 ₸"],
    ["Гардеробная", "м² (ширина × высота)", "от 60 000 ₸"],
    ["Прихожая", "погонный метр", "от 85 000 ₸"],
    ["ТВ-зона", "погонный метр", "от 70 000 ₸"]])}
<p>Цена шкафа считается по площади: ширина × высота × ставка за м². Ящики (до 4 шт.), турникеты и наполнение по желанию уже входят в стоимость. Подсветка считается дополнительно. Посчитать свой вариант можно <a href="kalkulyator.html">в калькуляторе</a>.</p>
<h2>Что изготавливаем</h2>
<ul><li><b>Распашные шкафы</b>: в нишу и до потолка, фасады ЛДСП, МДФ в плёнке или в краске</li><li><b>Гардеробные</b>: открытые системы и отдельные комнаты</li><li><b>Прихожие</b>: шкаф, обувница, сиденье, зеркало</li><li><b>Детская мебель</b>: шкафы, столы, кровати-чердаки</li><li><b>Санузел и балкон</b>: шкафы над инсталляцией, тумбы, балконные шкафы</li><li><b>ТВ-зоны и тумбы</b></li></ul>
<h2>Почему Khan Mebel</h2>
{USP_SHORT}
<h2>Мебель Астана: заказ напрямую у производителя</h2>
<p>Заказывая у производителя, вы не платите наценку салона и общаетесь напрямую с теми, кто делает и собирает мебель. Все решения обсуждаются на замере, а итог записывается в договор.</p>
<h2>Мебель на заказ в Астане недорого</h2>
<p>Недорого не значит плохо. Корпус и фасады из ЛДСП стоят дешевле МДФ в краске и служат годами, если фурнитура качественная. Мы предлагаем практичные материалы, а экономить советуем на отделке, а не на петлях и направляющих. Посчитать свой вариант можно <a href="kalkulyator.html">в калькуляторе</a>, все цены есть на странице <a href="ceny.html">«Цены»</a>.</p>
<h2>Деталировка мебели</h2>
<p>Каждый заказ проходит путь от 3D-проекта до деталировки: мы готовим чертежи и карты раскроя для каждого корпуса, фасада и полки. Поэтому мебель встаёт в нишу точно в размер, а сборка проходит без подпилов и подгонки на месте.</p>
<h2>Рынок, OLX или производство?</h2>
<p>На центральном рынке и на OLX продают готовые модули стандартных размеров. Они подходят, если размеры совпали. Если нет, остаются щели, неудобные углы и пустые места под потолком. Мебель на заказ делается под вашу квартиру, с договором, гарантией и сборкой. Отзывы о нас читайте <a href="otzyvy.html">на странице «Отзывы»</a> и в 2ГИС, свежие работы в <a href="https://www.instagram.com/khan_mebel.kz" target="_blank" rel="noopener">Instagram @khan_mebel.kz</a>.</p>''',
     FAQ_M, (offer("Изготовление мебели на заказ", "60000", "м²"),))

# Под ключ
FAQ_P = [
    ("Сколько стоит мебель под ключ для квартиры в Астане?", "Ориентир: однокомнатная квартира от ~980 000 ₸, двухкомнатная около 1,75 млн ₸, трёхкомнатная около 2,65 млн ₸. Сумма зависит от материалов и состава мебели."),
    ("Что входит в мебель под ключ?", "Проект, изготовление, доставка и сборка всей корпусной мебели квартиры: кухня, шкафы, гардеробная, прихожая, детская, санузел, балкон."),
    ("Можно заказать мебель для новостройки до ремонта?", "Лучше пригласить нас на замер после чистовой отделки стен и пола. Проект можно обсудить заранее, чтобы электрик вывел розетки под кухню."),
    ("Вы делаете мебель для частных домов?", "Да. Клиенты заказывают у нас мебель для новых домов и вторых квартир."),
]
page("mebel-pod-klyuch-astana.html",
     "Мебель под ключ в Астане для квартиры и дома | Khan Mebel",
     "Мебель под ключ в Астане: кухня, шкафы, гардеробная, прихожая, санузел одним проектом и договором. Квартира 1-комн от ~980 000 ₸. Замер и 3D за 1 выезд.",
     "Мебель под ключ в Астане",
     "Мебель под ключ",
     "Вся корпусная мебель квартиры или дома одним проектом, одним договором и одной командой. От кухни до шкафа над инсталляцией.",
     f'''<h2>Сколько стоит мебель под ключ</h2>
<p>Расчёт на материалах ЛДСП и МДФ в плёнке со стандартной фурнитурой, включая доставку и сборку. Это ориентир для бюджета, точную цену назовём на замере.</p>
{table(["Квартира", "Что входит", "Ориентир"], [
    ["1-комнатная", "Кухня 2,6 м, шкаф 1,8 м, прихожая 1,2 м", "от 980 000 ₸"],
    ["2-комнатная", "Угловая кухня 3,2 м (МДФ), 2 шкафа, прихожая", "≈ 1 750 000 ₸"],
    ["3-комнатная", "Кухня 3,8 м, гардеробная, шкаф, детская, прихожая, санузел", "≈ 2 650 000 ₸"]])}
<p>Соберите свою смету из нескольких позиций <a href="index.html#calc">в калькуляторе</a> и отправьте нам в WhatsApp.</p>
<h2>Как проходит проект под ключ</h2>
<ul><li>Один выезд: замеряем все комнаты и делаем 3D-проект на месте</li><li>Согласуем материалы и цвета, чтобы мебель смотрелась единым интерьером</li><li>Фиксируем цену и сроки в договоре</li><li>Изготавливаем и собираем комнату за комнатой, убираем за собой</li></ul>
<h2>Почему под ключ выгоднее</h2>
<p>Один подрядчик отвечает за всё: размеры стыкуются, цвета совпадают, сроки не зависят от нескольких мастеров. Клиенты, заказавшие у нас всю квартиру, возвращаются со вторыми квартирами и домами.</p>
<h2>Почему Khan Mebel</h2>
{USP_SHORT}''',
     FAQ_P, (offer("Мебель под ключ", "980000", "квартира"),))

# llms.txt, robots, sitemap
llms = f"""# Khan Mebel

> Мебельная компания в Астане (Казахстан). Изготовление кухонь и корпусной мебели на заказ: кухни, шкафы, гардеробные, прихожие, детские, мебель для санузла и балкона, мебель под ключ.

## Основные факты
- Адрес: Астана, {ADDR}, район Сарыарка, Z11E3P7
- Координаты: 51.183004, 71.435401
- Часы работы: 10:00-20:00
- WhatsApp: {PHONE_H}
- Instagram: {IG}
- 2ГИС: {GIS}, рейтинг 5.0 по 38 оценкам, 33 отзыва (октябрь 2026)
- Руководитель: Абылайхан, лично выезжает на замеры и контролирует сборку
- Замер, 3D-проект и договор за один выезд; замер обычно на следующий день после заявки
- Срок изготовления: обычно 10-15 рабочих дней, фиксируется в договоре
- Языки: русский, казахский

## Ориентировочные цены (KZT)
- Кухня на заказ: от 180 000 ₸ за погонный метр (ЛДСП), МДФ в плёнке от 250 000, МДФ в краске от 300 000
- Шкаф: от 60 000 ₸ за м² (фасады ЛДСП), от 80 000 ₸ за м² (МДФ в плёнке); площадь = ширина × высота
- Гардеробная: от 60 000 ₸ за м²
- Кухня: корпус ЛДСП Томск/Ламарти, фасады МДФ, фурнитура GTV (Польша) с доводчиками, ящики скрытого монтажа на 25-30 кг, гигиенический поддон, термопланки, подсветка, столешница ЛДСП Скиф/Кедр
- Шкаф: корпус ЛДСП Томск/Ламарти, фасады и видимые части МДФ, фурнитура GTV, турникеты, до 4 ящиков, наполнение по желанию
- Прихожая: от 85 000 ₸ за погонный метр
- Мебель под ключ: 1-комнатная квартира от ~980 000 ₸

## Страницы
- [Главная и калькулятор]({DOMAIN}/)
- [Кухни на заказ в Астане]({DOMAIN}/kuhni-na-zakaz-astana.html)
- [Мебель на заказ в Астане]({DOMAIN}/mebel-na-zakaz-astana.html)
- [Мебель под ключ в Астане]({DOMAIN}/mebel-pod-klyuch-astana.html)
"""
# 404
doc("404.html", "Страница не найдена | Khan Mebel", "Такой страницы нет. Перейдите на главную Khan Mebel или посчитайте мебель в калькуляторе.",
    page_head("Такой страницы нет", "Возможно, ссылка устарела. Начните с главной или посчитайте стоимость мебели в калькуляторе.", "404"), anim=False)
PAGES.remove("404.html")

# llms.txt: список страниц
llms = llms.replace("## Страницы\n", "## Страницы\n" + "".join(
    f"- [{t}]({DOMAIN}/{p})\n" for p, t in [("kalkulyator.html", "Калькулятор стоимости"), ("proekty.html", "Проекты: фото и видео"),
    ("ceny.html", "Цены"), ("otzyvy.html", "Отзывы"), ("kontakty.html", "Контакты")]))
llms = llms.replace("- [Главная и калькулятор]", "- [Главная]")
with open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8") as f:
    f.write(clean(llms))
with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
PRIORITY = {"": "1.0", "kuhni-na-zakaz-astana.html": "0.9", "mebel-na-zakaz-astana.html": "0.9", "mebel-pod-klyuch-astana.html": "0.9", "kalkulyator.html": "0.8"}
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
    f"  <url><loc>{DOMAIN}/{clean(p)}</loc><lastmod>{TODAY}</lastmod><priority>{PRIORITY.get(p, '0.7')}</priority></url>\n" for p in PAGES) + "</urlset>\n"
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sm)
print("Готово:", ", ".join(p or "index.html" for p in PAGES))
