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
DOMAIN = "https://khanmebel.kz"

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
    ("kitchen6-corner", "kitchen", "big", "Угловая кухня: матовые фасады, рифлёные антресоли и витрина в чёрной раме с подсветкой"),
    ("hall4-wardrobe", "hall", "tall", "Прихожая в стиле шейкер: шкаф до потолка, ниша с крючками и сиденье"),
    ("kids2-desk", "kids", "tall", "Детская: розовый стеллаж с подсветкой, стол с ящиками над радиатором и пенал"),
    ("bath7-room", "bath", "tall", "Санузел: рифлёный шкаф над инсталляцией с нишей и тумба под раковину"),
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
    ("kitchen7-straight", "kitchen", "tall", "Прямая кухня до потолка: фасады шейкер, столешница ЛДСП под дуб"),
    ("kitchen6-oven", "kitchen", "tall", "Колонна под духовку и микроволновку, вытяжка в верхнем шкафу"),
    ("kitchen6-side", "kitchen", "tall", "Подсветка рабочей зоны и витрина из стекла"),
    ("kids2-wardrobe", "kids", "tall", "Шкаф в детскую: белые и розовые фасады с фрезеровкой, полки для обуви снизу"),
    ("kids2-shelf", "kids", "tall", "Стеллаж до потолка со встроенной LED-подсветкой"),
    ("kids2-shelf-detail", "kids", "tall", "Подсветка в стеллаже: свет вдоль каждой полки"),
    ("kids2-handles", "kids", "tall", "Фрезеровка-арки и золотые ручки на розовых фасадах"),
    ("hall4-bench", "hall", "tall", "Сиденье с мягкой подушкой и ящиком для обуви"),
    ("bath7-detail", "bath", "tall", "Подвесная тумба с рифлёными ящиками и ручками-профилями"),
    ("bath6-door", "bath", "tall", "Шкафы под дуб над инсталляцией и открытые полки"),
    ("kitchen6-drawers", "kitchen", "tall", "Ящики с доводчиками и ручки-профили"),
    ("kitchen7-drawers", "kitchen", "tall", "Фасады шейкер и чёрные ручки"),
    ("detail2-shelves", "wardrobe", "tall", "Наполнение шкафа: полки и вертикальные отсеки"),
]
FILTERS = [("all", "Все"), ("kitchen", "Кухни"), ("living", "Гостиные"), ("hall", "Прихожие"), ("kids", "Детские"), ("bedroom", "Спальни"), ("wardrobe", "Гардеробные"), ("bath", "Санузлы")]

def gallery_html(limit=None):
    f = "".join(f'<button type="button" data-f="{k}" aria-pressed="{"true" if k=="all" else "false"}">{t}</button>' for k, t in FILTERS)
    shots = "".join(
        f'''<button type="button" class="shot {size}" data-cat="{cat}" data-full="assets/media/{n}.jpg" data-cap="{cap}"><img src="assets/media/{n}{"" if size=="big" else "-s"}.jpg" alt="{cap}, Khan Mebel, Астана" loading="lazy" decoding="async"><span class="cap">{cap}</span></button>'''
        for n, cat, size, cap in (PROJECTS[:limit] if limit else PROJECTS))
    return f'<div class="filters" role="group" aria-label="Фильтр проектов">{f}</div><div class="gallery" id="gallery">{shots}</div>'

def gallery_only(cat):
    # Галерея одной категории без фильтров (для страниц «фото»)
    shots = "".join(
        f'''<button type="button" class="shot {size}" data-cat="{c}" data-full="assets/media/{n}.jpg" data-cap="{cap}"><img src="assets/media/{n}{"" if size=="big" else "-s"}.jpg" alt="{cap}, кухня на заказ, Khan Mebel, Астана" loading="lazy" decoding="async"><span class="cap">{cap}</span></button>'''
        for n, c, size, cap in PROJECTS if c == cat)
    return f'<div class="gallery" id="gallery">{shots}</div>'

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
    "shkafy-na-zakaz-astana.html": [("wardrobe-arch", "Распашной шкаф на заказ с фрезеровкой-арками, Астана"), ("bedroom-wardrobe", "Шкаф в спальню с нишей и подсветкой"), ("bedroom3-open", "Наполнение шкафа: полки, штанга, ящики")],
    "garderobnye-na-zakaz-astana.html": [("closet-walnut", "Гардеробная на заказ из ЛДСП цвета орех, Астана"), ("closet-laundry", "Гардеробная с нишей под стиральную машину"), ("detail-shelves", "Полки под размеры вещей")],
    "prihozhie-na-zakaz-astana.html": [("hall2-wardrobe", "Прихожая на заказ со шкафом до потолка, Астана"), ("hall-oak", "Прихожая из рифлёного дуба с сиденьем"), ("hall4-bench", "Сиденье с ящиком для обуви")],
    "detskaya-mebel-na-zakaz-astana.html": [("kids-room", "Детская на двоих на заказ, Астана"), ("kids2-desk", "Стол и стеллаж с подсветкой"), ("kids2-wardrobe", "Шкаф в детскую с фрезеровкой")],
    "mebel-dlya-sanuzla-astana.html": [("bath5-blue", "Шкаф над инсталляцией на заказ, Астана"), ("bath7-room", "Рифлёный шкаф и тумба под раковину"), ("bath2-vanity", "Подвесная тумба с ящиками")],
    "uglovye-kuhni-na-zakaz-astana.html": [("kitchen6-corner", "Угловая кухня на заказ до потолка, Астана"), ("kitchen2-corner", "Угловая кухня с витриной"), ("kitchen6-oven", "Колонна под духовку")],
    "mebel-na-zakaz-nedorogo-astana.html": [("kitchen7-straight", "Прямая кухня со столешницей ЛДСП, Астана"), ("closet-walnut", "Гардеробная из ЛДСП"), ("hall3-closed", "Прихожая со шкафом")],
    "kuhni-nedorogo-astana.html": [("kitchen7-straight", "Недорогая прямая кухня со столешницей ЛДСП, Астана"), ("kitchen3-straight", "Прямая кухня в стиле шейкер"), ("kitchen7-drawers", "Ящики с доводчиками")],
    "gotovye-kuhni-astana.html": [("kitchen4-oak", "Кухня на заказ до потолка, Астана"), ("kitchen-column", "Колонна под встроенную технику"), ("kitchen5-straight", "Прямая кухня с колонной")],
    "gde-zakazat-mebel-astana.html": [("kitchen-green", "Кухня на заказ от производства в Астане"), ("detail-shelves", "Наполнение шкафа под размеры вещей"), ("kitchen3-drawers", "Ящики с доводчиками")],
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
<li><a href="shkafy-na-zakaz-astana.html">Шкафы</a> · <a href="garderobnye-na-zakaz-astana.html">Гардеробные</a> · <a href="prihozhie-na-zakaz-astana.html">Прихожие</a></li>
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
         "ceny", "otzyvy", "kontakty",
         "shkafy-na-zakaz-astana", "garderobnye-na-zakaz-astana", "prihozhie-na-zakaz-astana", "detskaya-mebel-na-zakaz-astana", "mebel-dlya-sanuzla-astana", "uglovye-kuhni-na-zakaz-astana", "mebel-na-zakaz-nedorogo-astana", "gde-zakazat-mebel-astana",
         "kuhni-nedorogo-astana", "gotovye-kuhni-astana", "kuhni-foto"]
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
doc("kalkulyator.html", "Калькулятор кухни онлайн: расчёт стоимости кухни и мебели | Khan Mebel",
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
# Все страницы услуг: для блока «Смотрите также», llms.txt и sitemap
SEE_ALSO = [("kuhni-na-zakaz-astana.html", "Кухни на заказ"), ("uglovye-kuhni-na-zakaz-astana.html", "Угловые кухни"), ("kuhni-nedorogo-astana.html", "Кухни недорого"), ("gotovye-kuhni-astana.html", "Готовые или на заказ"), ("kuhni-foto.html", "Фото кухонь"),
            ("mebel-na-zakaz-astana.html", "Мебель на заказ"), ("shkafy-na-zakaz-astana.html", "Шкафы"),
            ("garderobnye-na-zakaz-astana.html", "Гардеробные"), ("prihozhie-na-zakaz-astana.html", "Прихожие"),
            ("detskaya-mebel-na-zakaz-astana.html", "Детская мебель"), ("mebel-dlya-sanuzla-astana.html", "Мебель для санузла"),
            ("mebel-pod-klyuch-astana.html", "Мебель под ключ"), ("mebel-na-zakaz-nedorogo-astana.html", "Недорого"),
            ("gde-zakazat-mebel-astana.html", "Где заказать мебель"), ("kalkulyator.html", "Калькулятор"),
            ("proekty.html", "Проекты"), ("ceny.html", "Цены"), ("otzyvy.html", "Отзывы")]
MAT_PAGES = ("kuhni-na-zakaz-astana.html", "kuhni-nedorogo-astana.html", "mebel-na-zakaz-astana.html", "shkafy-na-zakaz-astana.html",
             "uglovye-kuhni-na-zakaz-astana.html", "mebel-na-zakaz-nedorogo-astana.html")

def answer_box(text):
    # Короткий прямой ответ в начале страницы: его проще всего процитировать поиску и ИИ-ассистентам
    return f'''<section style="padding:40px 0 0"><div class="wrap"><div class="answer"><span class="slash">// Коротко</span>
<p>{text}</p></div></div></section>''' if text else ""

def page(path, title, desc, h1, crumb, intro, body, faqs, extra_ld=(), answer=""):
    see = "".join(f'<a href="{h}">{t}</a>' for h, t in SEE_ALSO if h != path)
    doc(path, title, desc,
        page_head(h1, intro, crumb) + answer_box(answer) + photo_strip(path) +
        f'''<section style="padding-top:56px"><div class="wrap prose">
{body}
</div></section>
''' + (mat_html() if path in MAT_PAGES else "") + f'''<section class="band-light"><div class="wrap prose">
<h2 style="margin-top:0">Частые вопросы</h2>
{faq_html(faqs)}
<h2>Смотрите также</h2>
<div class="pills">{see}</div>
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
     "Кухни на заказ в Астане: цены от 180 000 ₸/п.м. | Khan Mebel",
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
<p>Цены ориентировочные. Точную стоимость считаем на замере. Предварительно можно посчитать <a href="kalkulyator.html">в калькуляторе кухни онлайн</a>, а готовые работы посмотреть на странице <a href="kuhni-foto.html">«Фото кухонь»</a>.</p>
<h2>Изготовление кухни: что входит</h2>
<ul><li>Выезд на замер и 3D-проект кухни на месте</li><li>Корпус ЛДСП Томск или Ламарти, фасады МДФ, фурнитура GTV (Польша) с доводчиками, ящики скрытого монтажа на 25-30 кг, гигиенический поддон, термопланки, подсветка, столешница ЛДСП Скиф или Кедр</li><li>Производство корпусов и фасадов в нашем цеху</li><li>Доставка, сборка, врезка мойки и варочной панели, установка встроенной техники</li></ul>
<h2>Почему кухни Khan Mebel</h2>
{USP_SHORT}
<h2>Кухни Астана недорого: как сэкономить без потери качества</h2>
<p>Самая большая экономия в фасадах: ЛДСП заметно дешевле МДФ в краске. Столешница из ЛДСП обходится в несколько раз дешевле искусственного камня. А вот петли и направляющие лучше брать с доводчиками: на них приходится вся ежедневная нагрузка. Примеры цен на бюджетные кухни: <a href="kuhni-nedorogo-astana.html">«Кухни Астана недорого»</a>.</p>
<h2>Купить кухню в Казахстане: заказ или готовая?</h2>
<p>Готовая кухня дешевле на старте, но редко встаёт точно в размер: остаются щели, не помещается техника. Кухня на заказ делается под ваши стены, трубы и розетки, поэтому служит дольше и использует каждый сантиметр. Подробное сравнение: <a href="gotovye-kuhni-astana.html">«Готовая модульная кухня или кухня на заказ»</a>, угловые варианты: <a href="uglovye-kuhni-na-zakaz-astana.html">«Угловые кухни»</a>.</p>''',
     FAQ_K, (offer("Изготовление кухни на заказ", "180000", "погонный метр"),))

# Мебель на заказ
FAQ_M = [
    ("Сколько стоит мебель на заказ в Астане?", "Шкаф с фасадами ЛДСП от 60 000 ₸ за м², с фасадами МДФ в плёнке от 80 000 ₸ за м², гардеробная от 60 000 ₸ за м² (площадь = ширина × высота), прихожая от 85 000 ₸ за погонный метр. Точную цену называем после замера."),
    ("Какие материалы используете?", "Корпус из ЛДСП Томск или Ламарти, фасады и видимые части - МДФ в плёнке или в краске. Фурнитура GTV (Польша), все механизмы с доводчиками. В шкафах турникеты, до 4 ящиков и наполнение по вашему желанию."),
    ("Сколько делается шкаф на заказ?", "В среднем 10-15 рабочих дней. Срок фиксируем в договоре."),
    ("Делаете мебель в санузел и на балкон?", "Да, делаем шкафы над инсталляцией, тумбы в санузел и шкафы на балкон по размерам."),
    ("Можно заказать мебель недорого?", "Да. Самый доступный вариант: корпус и фасады из ЛДСП со стандартной фурнитурой с доводчиками. На замере покажем, где можно сэкономить без потери качества, а где лучше не урезать."),
    ("Вы делаете деталировку мебели?", "Да, деталировку и карты раскроя делаем сами по 3D-проекту, это часть заказа. Поэтому детали приходят точно в размер и собираются без подгонки на месте."),
    ("Чем заказ у вас отличается от мебели с центрального рынка или OLX?", "Готовая мебель с рынка или объявления на OLX сделана под чужие размеры. Мы приезжаем на замер, рисуем 3D-проект под вашу квартиру, фиксируем цену и сроки в договоре и сами собираем. Рейтинг 5,0 в 2ГИС можно проверить до заказа."),
    ("Где посмотреть ваши работы?", "В разделе «Проекты» на сайте и в Instagram @khan_mebel.kz: там новые кухни, шкафы и видео-обзоры квартир."),
]
page("mebel-na-zakaz-astana.html",
     "Корпусная мебель на заказ в Астане от производителя | Khan Mebel",
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
<ul><li><a href="shkafy-na-zakaz-astana.html"><b>Распашные шкафы</b></a>: в нишу и до потолка, фасады ЛДСП, МДФ в плёнке или в краске</li><li><a href="garderobnye-na-zakaz-astana.html"><b>Гардеробные</b></a>: открытые системы и отдельные комнаты</li><li><a href="prihozhie-na-zakaz-astana.html"><b>Прихожие</b></a>: шкаф, обувница, сиденье, зеркало</li><li><a href="detskaya-mebel-na-zakaz-astana.html"><b>Детская мебель</b></a>: шкафы, столы, кровати-чердаки</li><li><a href="mebel-dlya-sanuzla-astana.html"><b>Санузел</b></a> и балкон: шкафы над инсталляцией, тумбы, балконные шкафы</li><li><b>ТВ-зоны и тумбы</b></li></ul>
<h2>Почему Khan Mebel</h2>
{USP_SHORT}
<h2>Мебель Астана: заказ напрямую у производителя</h2>
<p>Заказывая у производителя, вы не платите наценку салона и общаетесь напрямую с теми, кто делает и собирает мебель. Все решения обсуждаются на замере, а итог записывается в договор.</p>
<h2>Мебель на заказ в Астане недорого</h2>
<p>Недорого не значит плохо. Корпус и фасады из ЛДСП стоят дешевле МДФ в краске и служат годами, если фурнитура качественная. Мы предлагаем практичные материалы, а экономить советуем на отделке, а не на петлях и направляющих. Примеры бюджетных комплектаций собрали на странице <a href="mebel-na-zakaz-nedorogo-astana.html">«Мебель на заказ недорого»</a>, все цены есть на странице <a href="ceny.html">«Цены»</a>.</p>
<h2>Деталировка мебели</h2>
<p>Каждый заказ проходит путь от 3D-проекта до деталировки: мы готовим чертежи и карты раскроя для каждого корпуса, фасада и полки. Поэтому мебель встаёт в нишу точно в размер, а сборка проходит без подпилов и подгонки на месте.</p>
<h2>Рынок, OLX или производство?</h2>
<p>На центральном рынке и на OLX продают готовые модули стандартных размеров. Они подходят, если размеры совпали. Если нет, остаются щели, неудобные углы и пустые места под потолком. Мебель на заказ делается под вашу квартиру, с договором и сборкой. Отзывы о нас читайте <a href="otzyvy.html">на странице «Отзывы»</a> и в 2ГИС, свежие работы в <a href="https://www.instagram.com/khan_mebel.kz" target="_blank" rel="noopener">Instagram @khan_mebel.kz</a>. Подробное сравнение с чек-листом проверки мастера: <a href="gde-zakazat-mebel-astana.html">«Где заказать мебель в Астане»</a>.</p>''',
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

# ======================================================================
#  Страницы под отдельные запросы (17.11.2026)
#  Цены в примерах посчитаны по ставкам из assets/js/calculator.js.
#  Если меняете ставки там, поправьте примеры и здесь.
# ======================================================================

# Шкафы
FAQ_SH = [
    ("Сколько стоит шкаф на заказ в Астане?", "Шкаф с фасадами ЛДСП стоит от 60 000 ₸ за м², с фасадами МДФ в плёнке от 80 000 ₸ за м², с фасадами МДФ в краске от 100 000 ₸ за м². Площадь считается как ширина × высота. Шкаф 2 × 2,6 м из ЛДСП выходит примерно в 312 000 ₸."),
    ("Что входит в цену шкафа?", "Корпус из ЛДСП Томск или Ламарти, фасады, фурнитура GTV (Польша) с доводчиками, турникеты, до 4 выдвижных ящиков и внутреннее наполнение по вашему желанию. LED-подсветка считается отдельно."),
    ("Делаете шкафы-купе?", "Нет, шкафы-купе не делаем. Делаем распашные шкафы: в нишу, во всю стену и до потолка. У распашного шкафа открывается вся ширина сразу, и внутри нет мёртвых зон за створками."),
    ("Сколько делается шкаф на заказ?", "Обычно 10-15 рабочих дней после подписания договора. Срок записываем в договор."),
    ("Можно сделать шкаф до потолка?", "Да. Шкафы до потолка с антресолями используют всю высоту комнаты, и сверху не собирается пыль. Цена считается по той же формуле: ширина × высота × ставка за м²."),
]
page("shkafy-na-zakaz-astana.html",
     "Шкаф на заказ в Астане от 60 000 ₸/м² | Khan Mebel",
     "Распашные шкафы на заказ в Астане: в нишу, во всю стену, до потолка. ЛДСП от 60 000 ₸/м², МДФ от 80 000 ₸/м². Замер и 3D-проект за один выезд, изготовление 10-15 дней.",
     "Шкафы на заказ в Астане",
     "Шкафы",
     "Распашные шкафы по вашим размерам: в нишу, во всю стену и до потолка. Наполнение продумываем под ваши вещи на замере.",
     f'''<h2>Цены на шкафы на заказ</h2>
<p>Цена считается по площади фасада: ширина × высота × ставка за м². В ставку уже входят корпус, фасады, фурнитура с доводчиками, турникеты и до 4 ящиков.</p>
{table(["Фасады", "Ставка за м²", "Шкаф 2 × 2,6 м (5,2 м²)"], [
    ["ЛДСП", "от 60 000 ₸", "≈ 312 000 ₸"],
    ["МДФ в плёнке", "от 80 000 ₸", "≈ 416 000 ₸"],
    ["МДФ в краске", "от 100 000 ₸", "≈ 520 000 ₸"]])}
<p>LED-подсветка добавляет около 15 000 ₸ на погонный метр ширины. Свой размер можно посчитать <a href="kalkulyator.html">в калькуляторе</a>, точную цену называем на замере.</p>
<h2>Какие шкафы делаем</h2>
<ul><li><b>В нишу</b>: от стены до стены, без зазоров и заглушек</li><li><b>Во всю стену</b>: в спальню, гостиную или коридор</li><li><b>До потолка</b>: с антресолями для сезонных вещей и чемоданов</li><li><b>С открытой нишей</b>: под телевизор, книги, туалетный столик</li><li><b>С декором</b>: фрезеровка-арки, рифлёные фасады, латунные и кольцевые ручки</li></ul>
<h2>Как продумываем наполнение</h2>
<p>На замере спрашиваем, что будет храниться в шкафу: платья и пальто, постельное бельё, обувь, пылесос. Под это рисуем полки, штанги и ящики в 3D-проекте. Вы видите шкаф изнутри до того, как его начнут делать.</p>
<h2>Почему Khan Mebel</h2>
{USP_SHORT}''',
     FAQ_SH, (offer("Изготовление шкафа на заказ", "60000", "м²"),),
     answer="Распашной шкаф на заказ в Астане в Khan Mebel стоит от 60 000 ₸ за м² с фасадами ЛДСП и от 80 000 ₸ за м² с фасадами МДФ. Шкаф 2 × 2,6 м из ЛДСП выходит примерно в 312 000 ₸. Замер, 3D-проект и договор делаем за один выезд, изготовление занимает 10-15 рабочих дней.")

# Гардеробные
FAQ_G = [
    ("Сколько стоит гардеробная на заказ в Астане?", "От 60 000 ₸ за м², площадь считается как ширина × высота. Гардеробная система вдоль стены 2,4 м высотой 2,6 м выходит примерно в 374 000 ₸."),
    ("Что лучше: гардеробная или шкаф?", "Гардеробная вмещает больше и дешевле за м², потому что у открытой системы нет фасадов. Шкаф лучше, если нет отдельного помещения или вещи должны быть закрыты от пыли."),
    ("Можно сделать гардеробную из кладовки?", "Да, если ширина кладовки позволяет поставить систему хотя бы с одной стороны и оставить проход. На замере проверим размеры и предложим планировку."),
    ("Можно совместить гардеробную и постирочную?", "Да. Мы делаем гардеробные с нишей под стиральную и сушильную машины, полками и ящиками."),
]
page("garderobnye-na-zakaz-astana.html",
     "Гардеробная на заказ в Астане от 60 000 ₸/м² | Khan Mebel",
     "Гардеробные на заказ в Астане: системы вдоль стены, гардеробные комнаты, гардеробные с постирочной. От 60 000 ₸/м². 3D-проект на замере, изготовление 10-15 дней.",
     "Гардеробные на заказ в Астане",
     "Гардеробные",
     "Открытые гардеробные системы и гардеробные комнаты по размерам вашей квартиры. Полки, штанги и ящики под ваши вещи.",
     f'''<h2>Сколько стоит гардеробная</h2>
<p>Гардеробную считаем так же, как шкаф: ширина × высота × ставка. Ставка за открытую систему от 60 000 ₸ за м².</p>
{table(["Вариант", "Размер", "Ориентир"], [
    ["Система вдоль одной стены", "2,4 × 2,6 м (6,24 м²)", "≈ 374 000 ₸"],
    ["Небольшая система в нишу", "1,6 × 2,6 м (4,16 м²)", "≈ 250 000 ₸"]])}
<p>Угловые и П-образные гардеробные считаем по проекту. Предварительную цену даст <a href="kalkulyator.html">калькулятор</a> (вкладка «Шкаф», тип «Гардеробная»).</p>
<h2>Какие гардеробные делаем</h2>
<ul><li><b>Открытая система</b> вдоль стены в спальне или отдельной комнате</li><li><b>Гардеробная комната</b> с системой по нескольким стенам</li><li><b>Гардеробная-постирочная</b> с нишей под стиральную и сушильную машины</li><li><b>Гардеробная в кладовке</b>, если позволяет ширина</li></ul>
<h2>Из чего состоит гардеробная</h2>
<p>Корпус из ЛДСП Томск или Ламарти, полки, штанги для длинной и короткой одежды, выдвижные ящики с доводчиками, полки для обуви. Расстояния между полками подбираем под ваши вещи, поэтому в гардеробной не остаётся пустого места.</p>
<h2>Почему Khan Mebel</h2>
{USP_SHORT}''',
     FAQ_G, (offer("Изготовление гардеробной на заказ", "60000", "м²"),),
     answer="Гардеробная на заказ в Астане в Khan Mebel стоит от 60 000 ₸ за м² (ширина × высота). Система вдоль стены 2,4 × 2,6 м выходит примерно в 374 000 ₸. Делаем открытые системы, гардеробные комнаты и гардеробные с постирочной, срок 10-15 рабочих дней.")

# Прихожие
FAQ_PR = [
    ("Сколько стоит прихожая на заказ в Астане?", "Открытая прихожая от 85 000 ₸ за погонный метр, прихожая со шкафом от 110 000 ₸ за погонный метр при высоте 2,4 м. Зеркало добавляет около 25 000 ₸, сиденье около 30 000 ₸."),
    ("Можно сделать прихожую в узкий коридор?", "Да. Для узкого коридора делаем неглубокие шкафы, открытые вешалки и обувницы с откидными полками. На замере подберём глубину, чтобы осталось место для прохода."),
    ("Что входит в прихожую?", "Обычно шкаф для верхней одежды, обувница, сиденье, открытая ниша с крючками и зеркало. Состав подбираем под размер коридора и количество людей в семье."),
    ("Сколько делается прихожая?", "Обычно 10-15 рабочих дней после подписания договора."),
]
page("prihozhie-na-zakaz-astana.html",
     "Прихожая на заказ в Астане от 85 000 ₸/п.м. | Khan Mebel",
     "Прихожие на заказ в Астане: шкаф до потолка, обувница, сиденье, ниша с крючками, зеркало. От 85 000 ₸ за погонный метр. Замер и 3D-проект за один выезд.",
     "Прихожие на заказ в Астане",
     "Прихожие",
     "Прихожая под размер вашего коридора: шкаф для верхней одежды, обувница, сиденье, ниша с крючками и зеркало.",
     f'''<h2>Цены на прихожие</h2>
{table(["Вариант", "Цена за п.м. (высота 2,4 м)"], [
    ["Открытая: вешалка, полки, обувница", "от 85 000 ₸"],
    ["Со шкафом для верхней одежды", "от 110 000 ₸"]])}
<p>Пример: прихожая со шкафом шириной 1,5 м, с сиденьем и зеркалом стоит около 220 000 ₸ (165 000 + 30 000 + 25 000). Если прихожая выше или ниже 2,4 м, цена меняется пропорционально высоте. Свой вариант можно посчитать <a href="kalkulyator.html">в калькуляторе</a>.</p>
<h2>Что можно встроить в прихожую</h2>
<ul><li><b>Шкаф до потолка</b> для пуховиков, пылесоса и сезонных вещей</li><li><b>Обувница</b> с наклонными или откидными полками</li><li><b>Сиденье</b> с мягкой подушкой и ящиком для обуви</li><li><b>Открытая ниша</b> с крючками и подсветкой для ключей и сумок</li><li><b>Зеркало</b> в полный рост или над консолью</li></ul>
<h2>Прихожая в стиле остальной квартиры</h2>
<p>Прихожую видят первой, поэтому её удобно делать вместе с кухней и шкафами: в одних цветах и с одинаковыми ручками. Если заказываете мебель на всю квартиру, посмотрите страницу <a href="mebel-pod-klyuch-astana.html">«Мебель под ключ»</a>.</p>
<h2>Почему Khan Mebel</h2>
{USP_SHORT}''',
     FAQ_PR, (offer("Изготовление прихожей на заказ", "85000", "погонный метр"),),
     answer="Прихожая на заказ в Астане в Khan Mebel стоит от 85 000 ₸ за погонный метр (открытая) и от 110 000 ₸ за погонный метр со шкафом для одежды. Прихожая со шкафом 1,5 м, сиденьем и зеркалом выходит примерно в 220 000 ₸. Срок изготовления 10-15 рабочих дней.")

# Детская мебель
FAQ_D = [
    ("Сколько стоит детская мебель на заказ?", "Шкаф в детскую считается по площади: от 60 000 ₸ за м² с фасадами ЛДСП и от 80 000 ₸ за м² с фасадами МДФ. Стол, стеллажи и кровать считаем по проекту после замера."),
    ("Какие материалы безопасны для детской?", "Корпус делаем из ЛДСП Томск или Ламарти, фасады из ЛДСП или МДФ. Все ящики и двери на доводчиках, поэтому ребёнок не прищемит пальцы и не хлопнет дверцей."),
    ("Можно сделать детскую на двоих детей?", "Да. Делаем детские на двоих: два шкафа, общий стол у окна или два рабочих места, место для игрушек."),
    ("Делаете рабочее место для школьника?", "Да: стол вдоль окна, стеллажи по бокам, тумба с ящиками и встроенная розетка с USB в столешнице."),
]
page("detskaya-mebel-na-zakaz-astana.html",
     "Детская мебель на заказ в Астане | Khan Mebel",
     "Детская мебель на заказ в Астане: шкафы, стол для школьника, стеллажи с подсветкой, детская на двоих. Шкаф от 60 000 ₸/м². Доводчики на всех ящиках. Замер и 3D-проект за один выезд.",
     "Детская мебель на заказ в Астане",
     "Детская мебель",
     "Шкафы, рабочие места для школьников, стеллажи и детские на двоих. Делаем мебель, которая подходит и малышу, и подростку.",
     f'''<h2>Цены на детскую мебель</h2>
{table(["Изделие", "Как считаем", "Цена"], [
    ["Шкаф, фасады ЛДСП", "м² (ширина × высота)", "от 60 000 ₸"],
    ["Шкаф, фасады МДФ в плёнке", "м² (ширина × высота)", "от 80 000 ₸"],
    ["Стол, стеллажи, кровать", "по проекту", "после замера"]])}
<p>Пример: шкаф в детскую 1,6 × 2,4 м из ЛДСП выходит около 230 000 ₸. Стол и стеллажи считаем вместе со шкафом в одном проекте.</p>
<h2>Что делаем для детской</h2>
<ul><li><b>Шкафы</b> с фрезеровкой-арками, цветными фасадами и полками для обуви</li><li><b>Рабочее место школьника</b>: стол вдоль окна, тумба с ящиками, розетка с USB в столешнице</li><li><b>Стеллажи</b> до потолка с LED-подсветкой каждой полки</li><li><b>Детская на двоих</b>: два шкафа, общий стол, место для игр</li><li><b>Кровати-чердаки</b> и места для хранения игрушек</li></ul>
<h2>Мебель на вырост</h2>
<p>Ребёнок растёт быстрее, чем изнашивается мебель. Поэтому корпус делаем нейтральным, а цвет добавляем фасадами, ручками и подсветкой. Через несколько лет можно поменять фасады, не переделывая шкаф целиком.</p>
<h2>Почему Khan Mebel</h2>
{USP_SHORT}''',
     FAQ_D, (offer("Детская мебель на заказ", "60000", "м²"),),
     answer="Детскую мебель на заказ в Астане Khan Mebel делает по размерам комнаты: шкафы, рабочее место школьника, стеллажи с подсветкой и детские на двоих. Шкаф стоит от 60 000 ₸ за м², стол и стеллажи считаются по проекту. Все ящики и двери на доводчиках.")

# Санузел
FAQ_S = [
    ("Сколько стоит шкаф над инсталляцией?", "Цена на мебель для санузла индивидуальная и считается по проекту: размеры ниши, фасады и наполнение сильно отличаются от квартиры к квартире. Пришлите размеры или фото в WhatsApp, назовём ориентир, точную цену на замере."),
    ("Можно ли сделать шкаф в санузле с доступом к счётчикам?", "Да. Шкаф над инсталляцией делаем с дверцами или съёмной панелью напротив счётчиков, кранов и люка инсталляции."),
    ("Какая тумба под раковину нужна?", "Чаще всего подвесная: под ней легко мыть пол. Делаем тумбы с ящиками на доводчиках под вашу раковину."),
    ("Мебель не испортится от влажности?", "В санузле важна вентиляция и аккуратная обработка кромок. На замере подскажем, какие фасады и материалы лучше подходят именно для вашей ванной."),
]
page("mebel-dlya-sanuzla-astana.html",
     "Мебель для санузла на заказ в Астане: шкаф над инсталляцией | Khan Mebel",
     "Мебель для ванной и санузла на заказ в Астане: шкаф над инсталляцией, подвесная тумба под раковину, открытые ниши. По размерам вашего санузла, замер и 3D-проект за один выезд.",
     "Мебель для санузла на заказ в Астане",
     "Мебель для санузла",
     "Шкафы над инсталляцией, подвесные тумбы и открытые ниши точно по размерам санузла, с доступом к счётчикам и кранам.",
     f'''<h2>Что делаем для ванной и санузла</h2>
<ul><li><b>Шкаф над инсталляцией</b> до потолка, с открытой нишей или подсветкой</li><li><b>Подвесная тумба</b> под раковину с ящиками на доводчиках</li><li><b>Открытые полки-ниши</b> для полотенец и косметики</li><li><b>Шкаф для стиральной машины</b> и бытовой химии</li></ul>
<h2>Сколько стоит</h2>
<p>Мебель для санузла считаем по проекту: на цену влияют размер ниши, фасады (рифлёные, цветные, под дуб) и наполнение. Самый быстрый способ узнать ориентир: прислать в WhatsApp размеры и фото санузла. Точную цену назовём на замере и запишем в договор.</p>
<h2>На что обратить внимание</h2>
<p>В санузле важно заранее предусмотреть доступ к счётчикам, кранам и кнопке инсталляции. Мы закладываем это в 3D-проект: напротив коммуникаций ставим дверцы или съёмную панель, чтобы сантехник мог всё открыть без разбора шкафа.</p>
<h2>Почему Khan Mebel</h2>
{USP_SHORT}''',
     FAQ_S,
     answer="Khan Mebel делает мебель для санузла на заказ в Астане: шкафы над инсталляцией, подвесные тумбы под раковину и открытые ниши. Цена зависит от размеров и фасадов, поэтому её считаем после замера; ориентир можно узнать, прислав размеры в WhatsApp. Доступ к счётчикам и кранам закладываем в проект.")

# Угловые кухни
FAQ_U = [
    ("Сколько стоит угловая кухня на заказ в Астане?", "Угловая кухня по стенам 2,4 + 1,8 м с фасадами ЛДСП и столешницей ЛДСП выходит примерно в 920 000 ₸, с фасадами МДФ в плёнке около 1 210 000 ₸. Длина считается по стенам, угол добавляет около 45 000 ₸ за угловой модуль."),
    ("Как считается длина угловой кухни?", "Складываем длину кухни по обеим стенам. Например, 2,4 м по одной стене и 1,8 м по другой дают 4,2 погонных метра."),
    ("Что поставить в угловой шкаф?", "В нижний угловой модуль чаще всего ставят мойку или выдвижные механизмы, чтобы не было «мёртвой зоны». Решение подбираем на замере под вашу технику и привычки."),
    ("Делаете П-образные кухни и кухни с островом?", "Да. Кухни на заказ делаем прямые, угловые, П-образные и с островом."),
]
page("uglovye-kuhni-na-zakaz-astana.html",
     "Угловая кухня на заказ в Астане: цены 2026 | Khan Mebel",
     "Угловые кухни на заказ в Астане: ЛДСП от 180 000 ₸/п.м., МДФ от 250 000 ₸/п.м. Угловая кухня 4,2 м из ЛДСП ≈ 920 000 ₸. Замер и 3D-проект за один выезд, изготовление 10-15 дней.",
     "Угловые кухни на заказ в Астане",
     "Угловые кухни",
     "Угловая кухня использует две стены и угол, поэтому в ней больше рабочей поверхности и места для хранения, чем в прямой.",
     f'''<h2>Сколько стоит угловая кухня</h2>
<p>Пример для кухни по стенам 2,4 + 1,8 м (4,2 погонных метра), верхние шкафы 720 мм, столешница ЛДСП:</p>
{table(["Фасады", "Цена за п.м.", "Угловая кухня 4,2 м"], [
    ["ЛДСП", "от 180 000 ₸", "≈ 920 000 ₸"],
    ["МДФ в плёнке", "от 250 000 ₸", "≈ 1 210 000 ₸"],
    ["МДФ в краске", "от 300 000 ₸", "≈ 1 420 000 ₸"]])}
<p>В расчёт входят модули, столешница ЛДСП (≈ 28 000 ₸ за п.м.) и угловой модуль (≈ 45 000 ₸). Верхние шкафы до потолка добавляют около 30% к стоимости модулей. Свои размеры можно посчитать <a href="kalkulyator.html">в калькуляторе</a>.</p>
<h2>Плюсы угловой кухни</h2>
<ul><li>Рабочий треугольник «мойка – плита – холодильник» получается компактным</li><li>Больше столешницы, чем у прямой кухни той же ширины</li><li>Угол можно занять мойкой или выдвижными механизмами</li><li>Подходит и для небольших кухонь, и для кухонь-гостиных</li></ul>
<h2>Угловая кухня до потолка</h2>
<p>В наших проектах угловые кухни часто идут до потолка: с рифлёными антресолями, витриной с подсветкой и колонной под духовку и микроволновку. Так помещается вся посуда, а над шкафами не собирается пыль. Фото таких кухонь есть в разделе <a href="proekty.html">«Проекты»</a>.</p>
<h2>Почему Khan Mebel</h2>
{USP_SHORT}''',
     FAQ_U, (offer("Угловая кухня на заказ", "180000", "погонный метр"),),
     answer="Угловая кухня на заказ в Астане в Khan Mebel стоит от 180 000 ₸ за погонный метр с фасадами ЛДСП. Кухня по стенам 2,4 + 1,8 м со столешницей ЛДСП выходит примерно в 920 000 ₸, с фасадами МДФ в плёнке около 1 210 000 ₸. Замер и 3D-проект за один выезд, изготовление 10-15 рабочих дней.")

# Недорого
FAQ_N = [
    ("Где заказать мебель недорого в Астане?", "Дешевле всего заказывать напрямую у производителя: без наценки салона. В Khan Mebel самый доступный вариант: корпус и фасады из ЛДСП с фурнитурой с доводчиками. Шкаф от 60 000 ₸ за м², кухня от 180 000 ₸ за погонный метр."),
    ("На чём можно сэкономить?", "На фасадах (ЛДСП вместо МДФ в краске), на столешнице (ЛДСП вместо искусственного камня), на высоте верхних шкафов и на форме кухни (прямая дешевле угловой)."),
    ("На чём экономить нельзя?", "На петлях, направляющих и ящиках. На них приходится вся ежедневная нагрузка, и дешёвая фурнитура первой выходит из строя. Мы ставим фурнитуру GTV (Польша) с доводчиками даже в бюджетных проектах."),
]
page("mebel-na-zakaz-nedorogo-astana.html",
     "Мебель на заказ в Астане недорого: как сэкономить | Khan Mebel",
     "Недорогая мебель на заказ в Астане от производителя: кухня из ЛДСП от 180 000 ₸/п.м., шкаф от 60 000 ₸/м². Где можно сэкономить, а где нельзя. Примеры бюджетов.",
     "Мебель на заказ в Астане недорого",
     "Недорого",
     "Мебель на заказ не обязательно дорогая. Объясняем, из чего складывается цена, где экономия разумна, а где обернётся переделкой.",
     f'''<h2>Сколько стоит недорогая мебель на заказ</h2>
<p>Бюджетные варианты на корпусе и фасадах из ЛДСП с фурнитурой GTV с доводчиками:</p>
{table(["Изделие", "Размер", "Ориентир"], [
    ["Прямая кухня, столешница ЛДСП", "2,6 м", "≈ 540 000 ₸"],
    ["Шкаф распашной", "1,8 × 2,6 м", "≈ 281 000 ₸"],
    ["Открытая прихожая", "1,2 м", "≈ 102 000 ₸"],
    ["Мебель под ключ", "1-комнатная квартира", "от 980 000 ₸"]])}
<p>Все цены есть на странице <a href="ceny.html">«Цены»</a>, свой вариант можно собрать <a href="kalkulyator.html">в калькуляторе</a>.</p>
<h2>Где экономия разумна</h2>
<ul><li><b>Фасады ЛДСП вместо МДФ в краске.</b> Кухня из ЛДСП стоит от 180 000 ₸ за п.м., из МДФ в краске от 300 000 ₸: разница около 40%.</li><li><b>Столешница ЛДСП вместо камня.</b> Около 28 000 ₸ за п.м. против 170 000 ₸ за искусственный камень.</li><li><b>Верхние шкафы стандартной высоты.</b> Шкафы до потолка удобнее, но добавляют около 30% к стоимости модулей.</li><li><b>Прямая кухня вместо угловой</b>, если позволяет планировка.</li><li><b>Открытая прихожая</b> вместо прихожей со шкафом: 85 000 против 110 000 ₸ за п.м.</li></ul>
<h2>Где экономить не стоит</h2>
<p>Петли, направляющие и ящики работают каждый день. Дешёвая фурнитура разбалтывается за год-два, и мебель приходится ремонтировать. Поэтому даже в самых бюджетных проектах ставим фурнитуру GTV (Польша) с доводчиками. Ещё одна ложная экономия: заказ без замера. Ошибка в несколько сантиметров стоит дороже, чем выезд мастера.</p>
<h2>Почему у производителя дешевле</h2>
<p>Вы не платите наценку салона и посредника. Замер, проект, производство и сборку делает одна команда, а цена фиксируется в договоре и не меняется после подписания.</p>''',
     FAQ_N, (offer("Мебель на заказ недорого", "60000", "м²"),),
     answer="Недорогая мебель на заказ в Астане: корпус и фасады из ЛДСП с фурнитурой с доводчиками. В Khan Mebel шкаф стоит от 60 000 ₸ за м², кухня от 180 000 ₸ за погонный метр, прямая кухня 2,6 м со столешницей ЛДСП около 540 000 ₸. Экономить разумно на фасадах и столешнице, но не на фурнитуре.")

# Где заказать: рынок, OLX, Instagram, производство
FAQ_W = [
    ("Где лучше заказать мебель в Астане: на рынке, на OLX или на производстве?", "Готовая мебель с рынка или OLX подходит, если стандартный размер совпал с вашим. Если нужна мебель точно в нишу, с договором и сборкой, надёжнее заказывать на производстве после замера."),
    ("Как проверить мебельщика из Instagram?", "Посмотрите отзывы в 2ГИС, а не только в комментариях, попросите фото и видео реальных работ, узнайте адрес цеха или шоурума и требуйте договор с ценой, сроком и материалами."),
    ("Что должно быть в договоре на мебель?", "Итоговая цена, срок изготовления и установки, материалы корпуса и фасадов, бренд фурнитуры, размер предоплаты и что происходит при срыве срока."),
    ("Где посмотреть работы Khan Mebel?", "На странице «Проекты», в Instagram @khan_mebel.kz и в 2ГИС, где у нас рейтинг 5,0 по 38 оценкам. Шоурум: Астана, ул. Ыкылас Дукенулы, 31/2."),
]
page("gde-zakazat-mebel-astana.html",
     "Где заказать мебель в Астане: рынок, OLX, Instagram или производство",
     "Где заказать мебель на заказ в Астане: центральный рынок, OLX, мастера из Instagram или производство. Сравнение по цене, срокам и сборке и чек-лист, как проверить мебельщика.",
     "Где заказать мебель в Астане: рынок, OLX, Instagram или производство",
     "Где заказать мебель",
     "Честное сравнение четырёх способов купить мебель в Астане и чек-лист, который поможет не ошибиться с мастером.",
     f'''<h2>Сравнение</h2>
{table(["", "Рынок", "OLX", "Мастер из Instagram", "Производство с шоурумом"], [
    ["Размеры", "Стандартные", "Стандартные или б/у", "Под заказ", "Под заказ после замера"],
    ["3D-проект", "Нет", "Нет", "По-разному", "Да"],
    ["Договор", "Чек", "Обычно нет", "По-разному", "Да, с ценой и сроком"],
    ["Сборка", "Отдельно", "Сами", "По-разному", "Входит"],
    ["Где проверить", "Осмотреть на месте", "Фото в объявлении", "Instagram, 2ГИС", "2ГИС, шоурум, работы"]])}
<h2>Центральный рынок</h2>
<p>Плюс рынка: мебель можно потрогать и увезти в тот же день. Минус: размеры стандартные. Если ниша 2,15 м, а шкаф 2 м, останется щель, а под потолком пустое место. Рынок хорош для отдельных предметов: стола, комода, тумбы.</p>
<h2>OLX</h2>
<p>На OLX дешевле всего, особенно б/у. Но мебель уже сделана под чужую квартиру, а разборка и перевозка часто расшатывают корпус. Объявления «мебель на заказ» на OLX тоже бывают хорошими, но проверяйте мастера по чек-листу ниже.</p>
<h2>Мастера из Instagram</h2>
<p>В Instagram много хороших мастеров, и это удобный способ посмотреть стиль работ. Но красивые фото ещё ничего не говорят о сроках и качестве сборки. Перед заказом найдите мастера в 2ГИС, почитайте отзывы и попросите договор.</p>
<h2>Производство с шоурумом</h2>
<p>Производство делает мебель под ваши размеры: замер, 3D-проект, договор, изготовление и сборка у одной команды. Это дороже готовой мебели с рынка, но вещь встаёт точно в размер и служит дольше.</p>
<h2>Чек-лист: как проверить мебельщика</h2>
<ul><li>Есть отзывы в 2ГИС или Google, а не только комментарии в Instagram</li><li>Есть фото и видео реальных квартир, а не картинки из интернета</li><li>Есть адрес цеха или шоурума, куда можно приехать</li><li>Замер делает мастер, а не вы сами рулеткой</li><li>В договоре указаны цена, срок, материалы и бренд фурнитуры</li><li>Понятно, какая предоплата и что будет при срыве срока</li></ul>
<h2>Как это устроено в Khan Mebel</h2>
<p>Шоурум и производство в Астане, ул. Ыкылас Дукенулы, 31/2. Рейтинг 5,0 по 38 оценкам в <a href="{GIS}" target="_blank" rel="noopener">2ГИС</a>, работы в разделе <a href="proekty.html">«Проекты»</a> и в <a href="{IG}" target="_blank" rel="noopener">Instagram @khan_mebel.kz</a>. Замер, 3D-проект и договор за один выезд, срок 10-15 рабочих дней записываем в договор.</p>''',
     FAQ_W,
     answer="Готовая мебель с центрального рынка или OLX дешевле и доступна сразу, но сделана в стандартных размерах. Мастера из Instagram и производства делают мебель под заказ; перед заказом проверьте отзывы в 2ГИС, реальные работы, адрес цеха и договор с ценой, сроком и материалами.")


# Недорогие кухни
FAQ_KN = [
    ("Сколько стоит недорогая кухня в Астане?", "Самая доступная кухня на заказ в Khan Mebel: корпус и фасады из ЛДСП, от 180 000 ₸ за погонный метр. Прямая кухня 2,6 м со столешницей ЛДСП выходит примерно в 540 000 ₸, 3 м около 624 000 ₸."),
    ("Почему кухня на заказ может быть не дороже готовой?", "Готовую кухню часто приходится докупать модулями и подгонять, а лишние сантиметры остаются пустыми. Кухня на заказ делается ровно под стену, и вы не платите за модули, которые не нужны."),
    ("Будет ли дешёвая кухня служить долго?", "Да, если не экономить на фурнитуре. Мы ставим фурнитуру GTV (Польша) с доводчиками и ящики скрытого монтажа на 25-30 кг даже в самых бюджетных кухнях."),
    ("Входит ли техника в цену кухни?", "Нет. Бытовая техника, мойка и смеситель в цену не входят. Установку встроенной техники можем сделать при сборке."),
]
page("kuhni-nedorogo-astana.html",
     "Кухни Астана недорого: кухня из ЛДСП от 180 000 ₸/п.м. | Khan Mebel",
     "Недорогие кухни на заказ в Астане от производителя: ЛДСП от 180 000 ₸ за погонный метр, прямая кухня 2,6 м ≈ 540 000 ₸. Где сэкономить без потери качества, примеры цен.",
     "Кухни в Астане недорого",
     "Кухни недорого",
     "Бюджетная кухня на заказ точно по размеру стены. Показываем реальные цены и объясняем, на чём можно сэкономить.",
     f'''<h2>Цены на недорогие кухни</h2>
<p>Прямые кухни с фасадами ЛДСП, верхними шкафами 720 мм и столешницей ЛДСП (≈ 28 000 ₸ за п.м.):</p>
{table(["Длина", "Модули", "Столешница", "Итого"], [
    ["2 м", "360 000 ₸", "56 000 ₸", "≈ 416 000 ₸"],
    ["2,6 м", "468 000 ₸", "72 800 ₸", "≈ 540 000 ₸"],
    ["3 м", "540 000 ₸", "84 000 ₸", "≈ 624 000 ₸"]])}
<p>Свои размеры можно посчитать <a href="kalkulyator.html">в калькуляторе кухни онлайн</a>. Доставка и сборка включены в смету калькулятора.</p>
<h2>Как сделать кухню дешевле</h2>
<ul><li><b>Фасады ЛДСП</b> вместо МДФ: 180 000 против 250 000-300 000 ₸ за п.м.</li><li><b>Столешница ЛДСП</b> вместо искусственного камня: около 28 000 против 170 000 ₸ за п.м.</li><li><b>Верхние шкафы 720 мм</b> вместо шкафов до потолка: до потолка дороже примерно на 30%.</li><li><b>Прямая кухня</b> вместо угловой, если позволяет планировка.</li></ul>
<h2>Что мы не урезаем даже в бюджетной кухне</h2>
<p>Фурнитура GTV (Польша) с доводчиками, ящики скрытого монтажа на 25-30 кг, гигиенический поддон под мойкой и термопланки возле плиты. Это то, что ломается первым в дешёвых кухнях, поэтому здесь не экономим.</p>
<h2>Почему Khan Mebel</h2>
{USP_SHORT}''',
     FAQ_KN, (offer("Недорогая кухня на заказ", "180000", "погонный метр"),),
     answer="Недорогая кухня на заказ в Астане в Khan Mebel: корпус и фасады из ЛДСП от 180 000 ₸ за погонный метр. Прямая кухня 2,6 м со столешницей ЛДСП стоит около 540 000 ₸, 3 м около 624 000 ₸. Фурнитура GTV с доводчиками входит даже в бюджетный вариант.")

# Готовые и модульные кухни
FAQ_GK = [
    ("Что лучше: готовая модульная кухня или кухня на заказ?", "Модульная кухня дешевле и быстрее, если стандартные модули (обычно шагом 10-20 см) ложатся на вашу стену. Если нет, остаются щели, пустой угол и место под потолком. Кухня на заказ делается ровно под стену, трубы и технику."),
    ("Продаёте готовые кухни?", "Нет, мы делаем кухни на заказ по размерам. Зато срок изготовления всего 10-15 рабочих дней, а замер, 3D-проект и договор делаем за один выезд."),
    ("Насколько кухня на заказ дороже модульной?", "Зависит от материалов. Кухня на заказ из ЛДСП стоит от 180 000 ₸ за погонный метр. Сравнивайте одинаковую комплектацию: фасады, фурнитуру, столешницу, доставку и сборку."),
    ("Можно ли купить кухню онлайн?", "Посчитать кухню онлайн можно в нашем калькуляторе и отправить смету в WhatsApp. Но перед изготовлением всё равно нужен замер, иначе кухня может не встать по месту."),
]
page("gotovye-kuhni-astana.html",
     "Готовые и модульные кухни Астана или кухня на заказ: что выбрать",
     "Готовые и модульные кухни в Астане или кухня на заказ: сравнение по цене, срокам и размерам. Когда модульная кухня выгоднее, а когда лучше заказать по размеру. Расчёт онлайн.",
     "Готовая модульная кухня или кухня на заказ",
     "Готовые кухни",
     "Сравниваем готовые модульные кухни и кухни на заказ: когда модули выгоднее, а когда переплата за готовую кухню получается больше.",
     f'''<h2>Сравнение</h2>
{table(["", "Готовая модульная кухня", "Кухня на заказ"], [
    ["Размеры", "Модули стандартной ширины", "Точно по стене"],
    ["Срок", "Сразу или под заказ со склада", "10-15 рабочих дней"],
    ["Замер и проект", "Обычно сами", "Мастер и 3D-проект"],
    ["Угол, трубы, короб", "Обходить заглушками", "Учитываем в проекте"],
    ["До потолка", "Редко", "Да, с антресолями"],
    ["Цена", "Ниже на старте", "От 180 000 ₸ за п.м. (ЛДСП)"]])}
<h2>Когда модульная кухня выгоднее</h2>
<p>Если стена ровная, длина совпадает с суммой стандартных модулей, а кухня нужна на время, например в съёмную квартиру. Тогда модули дешевле и их можно увезти сразу.</p>
<h2>Когда лучше заказать по размеру</h2>
<ul><li>Стена не кратна модулям, и остаётся 15-30 см пустоты</li><li>Есть короб, газовая труба, счётчик или неровный угол</li><li>Нужна встроенная техника и колонна под духовку</li><li>Хочется шкафы до потолка, без пыли наверху</li><li>Кухня ставится надолго, в свою квартиру</li></ul>
<h2>Как посчитать кухню онлайн</h2>
<p>В <a href="kalkulyator.html">калькуляторе</a> выберите форму, длину по стенам, фасады и столешницу: цена появится сразу. Отправьте смету в WhatsApp, и мы приедем на замер на следующий день. Варианты подешевле собрали на странице <a href="kuhni-nedorogo-astana.html">«Кухни недорого»</a>.</p>''',
     FAQ_GK,
     answer="Готовая модульная кухня дешевле на старте и доступна сразу, но состоит из модулей стандартной ширины. Кухня на заказ делается точно по стене, с учётом труб, короба и техники. В Khan Mebel кухня на заказ стоит от 180 000 ₸ за погонный метр (ЛДСП) и делается за 10-15 рабочих дней.")

# Кухни: фото работ
FAQ_KF = [
    ("Где посмотреть фото кухонь Khan Mebel?", "На этой странице собраны фото кухонь, которые мы сделали для квартир в Астане. Остальные работы есть в разделе «Проекты» и в Instagram @khan_mebel.kz, видео-обзоры на главной странице."),
    ("Можно сделать такую же кухню?", "Да. Пришлите в WhatsApp фото понравившейся кухни и размеры стены: назовём ориентир по цене, а на замере подгоним проект под вашу кухню."),
    ("Сколько стоит кухня как на фото?", "Зависит от длины и фасадов. Кухня из ЛДСП от 180 000 ₸ за погонный метр, МДФ в плёнке от 250 000 ₸, МДФ в краске от 300 000 ₸. Свой вариант можно посчитать в калькуляторе."),
]
doc("kuhni-foto.html", "Кухни на заказ в Астане: фото работ | Khan Mebel",
    "Фото кухонь на заказ в Астане от Khan Mebel: угловые и прямые кухни до потолка, витрины с подсветкой, колонны под технику, фасады шейкер и рифлёные. Реальные квартиры.",
    page_head("Кухни на заказ: фото наших работ", "Реальные кухни, которые мы сделали для квартир в Астане. Нажмите на фото, чтобы рассмотреть детали.", "Фото кухонь")
    + answer_box("На странице собраны фото кухонь на заказ, которые Khan Mebel сделала в Астане: угловые и прямые кухни до потолка, витрины с подсветкой, колонны под духовку и микроволновку, фасады шейкер и рифлёные. Цены на такие кухни начинаются от 180 000 ₸ за погонный метр.")
    + f'''<section style="padding-top:40px"><div class="wrap">{gallery_only("kitchen")}
<div class="center" style="margin-top:32px;text-align:center"><a class="btn btn-ink" href="kuhni-na-zakaz-astana.html">Цены на кухни</a> <a class="btn btn-paper" href="proekty.html">Все проекты</a></div></div></section>'''
    + f'''<section class="band-light"><div class="wrap prose"><h2 style="margin-top:0">Частые вопросы</h2>{faq_html(FAQ_KF)}</div></section>''' + sec_lead(),
    (faq_schema(FAQ_KF), crumbs_schema("Фото кухонь", "kuhni-foto.html")))

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
- Шкаф с фасадами МДФ в краске: от 100 000 ₸ за м²
- Прихожая со шкафом: от 110 000 ₸ за погонный метр
- Мебель для санузла (шкаф над инсталляцией, тумба): цена индивидуальная, по проекту после замера
- Шкафы только распашные, шкафы-купе не делаем
- Мебель под ключ: 1-комнатная квартира от ~980 000 ₸

## Страницы
- [Главная и калькулятор]({DOMAIN}/)
"""
llms += "".join(f"- [{t}]({DOMAIN}/{h})\n" for h, t in SEE_ALSO if h not in ("kalkulyator.html", "proekty.html", "ceny.html", "otzyvy.html"))
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
