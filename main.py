import requests
from time import sleep

import urllib.parse as urlparse
from urllib.parse import urlencode

from bs4 import BeautifulSoup


# classe qui contient les className CSS pour identifier les éléments HTML de la page AVITO
class ClassNames:
    item_element = 'oan6tk-0 gFtuUo'
    item_url = 'oan6tk-1 jkKPKg'
    pagination_buttons = 'sc-2y0ggl-0 cslvkF'


# class pour stocker les constantes: url de base de la page avito
# + les class names des elements qu'on souhaite recuperer
class Constants:
    cars_base_url = 'https://www.avito.ma/fr/maroc/voitures/{search_text}--%C3%A0_vendre'
    class_names = ClassNames()

# variable qui contient les urls des annonces, utilisé comme cache dans la RAM
memory = set()

# fonction qui retourne l'html de la page à partir de son url
def load_page_source(page_url):
    return requests.get(page_url).content


# fonction qui genere l'url en prenant le text de recherche + les filtres à appliquer
def generate_url(base_url, search_text, filter_=None, page=1):
    if filter_ is None:
        filter_ = {}
    filter_['o'] = page

    # traitement pour ajouter les elements du filtre à l'url sous format de query parameters
    url_parts = list(urlparse.urlparse(base_url.format(search_text=search_text)))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(filter_)
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


# retourne le nombre de pages
def get_number_of_pages(url):
    s = load_page_source(url)
    soup = BeautifulSoup(s)
    pagination_element = soup.findAll('div', {'class': Constants.class_names.pagination_buttons})
    if pagination_element:
        pagination_element = pagination_element[1]
    else:
        return 1
    pages_buttons_text = []
    for element in pagination_element.children:
        pages_buttons_text.append(element.text)
    return int(pages_buttons_text[-2])


# fonction qui génère les filtres avito
def generate_car_filter(brand=None,
                        model=None,
                        max_price=None,
                        min_price=None,
                        max_cv=None,
                        min_cv=None,
                        doors=None,
                        first_own=None,
                        fuel=None,
                        origin=None,
                        max_year=None,
                        min_year=None,
                        max_km=None,
                        min_km=None):
    # dictionnaire pour faire le mapping entre le nom de la marque et son numéro avito
    car_brands = {
        'audi': 3,
        'bmw': 5,
        'dacia': 13,
        'ford': 18,
        'citroen': 12,
        'fiat': 17,
        'honda': 22,
        'seat': 50
    }

    # declaration du dictionnaire filter_ vide, la réponse de la fonction
    filter_ = {}

    if brand is not None:
        filter_['cb'] = car_brands[brand.lower()]

    if model is not None:
        filter_['mo'] = model.lower()

    if max_price is not None:
        filter_['mpr'] = max_price

    if min_price is not None:
        filter_['spr'] = min_price

    if min_cv is not None:
        if min_cv > 7:
            filter_['spf'] = min(9, min_cv - 6)
    if max_cv is not None:
        if max_cv > 7:
            filter_['mpf'] = min(9, max_cv - 6)

    if doors is not None:
        if doors == 3:
            filter_['drs'] = 0
        if doors == 5:
            filter_['drs'] = 1

    if first_own is not None:
        if first_own:
            filter_['f_own'] = 0
        else:
            filter_['f_own'] = 1

    if fuel is not None:
        fuel_options = ['diesel', 'essence', 'electrique', 'lpg', 'hybride']
        filter_['fl'] = fuel_options.index(fuel.lower()) + 1 # id diesel = 1

    if origin is not None:
        origine_options = ['dédouanée', 'pas encore dédouannée', 'ww au maroc', 'importée neuve']
        filter_['v_orig'] = origine_options.index(origin.lower()) # id dédouané = 0

    if max_year is not None:
        filter_['re'] = max_year - 1980

    if min_year is not None:
        filter_['rs'] = min_year - 1980

    if max_km is not None:
        filter_['me'] = max(max_km - 200000, 0) / 50000 + min(max(max_km - 100000, 0), 100000) / 10000 + min(max_km, 100000) / 5000

    if min_km is not None:
        filter_['ms'] = max(min_km - 200000, 0) / 50000 + min(max(min_km - 100000, 0), 100000) / 10000 + min(min_km, 100000) / 5000

    return filter_


def get_ads_urls(page_html):
    urls = []
    soup = BeautifulSoup(page_html)
    articles = soup.findAll('div', {'class': Constants.class_names.item_element})

    for article in articles:
        urls.append(article.find('a', {'class': Constants.class_names.item_url}).attrs['href'])
    return urls


def check_search(found_urls):
    global memory
    return list(memory - set(found_urls))


def save_search(found_urls):
    global memory
    memory = set(found_urls)


def send_mail(new_urls):
    # l'implémentation denvoie de mail necessite un serveur SMTP
    # c payant
    # si on a l'addresse d'un serveur SMTP, lenvoie de mail est faisable facilement avec python
    # avec 2 lignes de code ...
    # là, la fonction va juste faire un print des nouveaux urls detectés au lieu d'envoyer un mail.
    print('mail sent:')
    print('\n'.join(new_urls))


if __name__ == '__main__':
    # intervalle de check du script en secondes, là chaque 10 minutes le script vérifie s'il y a des nouvelles annocnes
    interval = 600
    
    #les critères de recherche qu'on souhaite
    filter_ = generate_car_filter(brand='seat',
                                  model='leon',
                                  min_year=2017,
                                  fuel='diesel')
    search_text = 'leon fr'
    
    # generer l'url de la premiere page des annonces
    search_url = generate_url(Constants.cars_base_url, search_text, filter_)
    
    #boucle infinie, pour que le script tourne infiniement
    while True:
        # detecter le nombre de pages de recherche
        number_of_pages = get_number_of_pages(search_url)
        print('number of pages', number_of_pages)
        found_urls = []
        # une boucle pour extraire la data de chaque page
        for i in range(number_of_pages):
            # generer l'url de la page ( en ajoutant le numero de la page)
            url = generate_url(Constants.cars_base_url, search_text, filter_, i+1)
            # charger l'html de la page
            page_html = load_page_source(url)
            # extraire les urls des annocnes
            found_urls += get_ads_urls(page_html)
        print('annonces trouvés:', len(found_urls))
        # detecter s'il y a une nouvelle annonce en comparant avec le dernier resultat trouvé
        new_urls = check_search(found_urls)
        print('nouvelles annonces trouvées', len(new_urls))
        # sauvegarder le nouveau resultat dans la variable de cache "memory" pour etre utilisé dans la prochaine comparaison
        save_search(found_urls)
        
        #s'il y a des nouveaux urls, on notifie l'utilisateur avec un mail qui contient les urls
        if new_urls:
            send_mail(new_urls)
            
        # mettre le script en veille pour X secondes (defini dans la variable interval) avant de déclencher le traitement à zero
        sleep(interval)
