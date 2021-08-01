import requests
# import json
from bs4 import BeautifulSoup as bs4
import csv

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
           'Accept': 'application/json, text/javascript, */*; q=0.01'}

URL1 = 'https://coursevania.com/wp-admin/admin-ajax.php?offset='
URL2 = '&template=courses/grid&args={"posts_per_page":"10"}' \
       '&action=stm_lms_load_content&nonce=db160aa366&sort=date_high'

FILE = 'udemy.csv'

#web scraping
#https://www.tutorialbar.com/category/development/

def get_html(url):
    r = requests.get( url, headers=HEADERS )
    return r


def get_udemy(page=0):
    url = URL1 + str( page ) + URL2
    r = get_html( url )
    soup = bs4( r.content, 'html.parser' )
    return soup


def get_pages_count():
    data = html_clean( get_udemy() )
    beg = data.find( 'href' ) + 6
    #    link = data[beg:data.find( '"', beg )]
    total = data[data.find( '"total"' ) + 8:data.find( '"pages"' ) - 1]
    pages = int( data[data.find( '"pages"' ) + 8:data.rfind( '}' )] )
    #    print( link )
    print( f'Всего найдено {total} курсов' )
    print( f'Всего {pages} старниц' )
    #    print( data.find( '"pages"' ) + 8 )
    #    print( data.rfind( '}' ) )
    return pages


def html_clean(html):
    data = str( html ).replace( '\\', '' ).replace( "'", "" )
    data = data.replace( '{"content":"n    ', '' )
    return data


def get_content(html):
    items = html.split(
        'nn<div "="" class="stm_lms_courses__single no-sale="" stm_lms_courses__single_animation=""' )  # seporator into parts
    udemy = []
    for item in items:
        title_beg = item.find( ">ntt<h5>" ) + 8
        title_end = item.find( "&lt;", title_beg + 1 )
        category_beg = item.find( 'class="stm_lms_courses__single--term"' ) + 42
        category_end = item.find( 'tt&lt;/div', category_beg + 1 )
        link_cours_beg = item.find( 'class="stm_lms_courses__single--title">nt<a href="' ) + 50
        link_cours_end = item.find( '"', link_cours_beg + 1 )
        link_pic_beg = item.find( 'data-src="' ) + 10
        link_pic_end = item.find( '"', link_pic_beg + 1 )
        #        print(item[title_beg:title_end].replace('&amp;', '&'))
        #        print(item[category_beg:category_end].replace('&amp;', '&'))
        #        print(item[link_cours_beg:link_cours_end])
        #        print(item[link_pic_beg:link_pic_end])
        if len( item[title_beg:title_end] ) > 0:
            req = get_html(item[link_cours_beg:link_cours_end])
            if req.status_code == 200:
                soup = bs4( req.content, 'html.parser' )
                divs = soup.find( 'div', attrs={'class': 'stm-lms-buy-buttons'} )  # ищем кнопку купить
                href = divs.find( 'a' )['href']
#                print( "{}".format( href ) )
            else:
                print( "Ошибка URL" )
            udemy.append( {
                'title': item[title_beg:title_end].replace( '&amp;', '&' ),
                'category': item[category_beg:category_end].replace( '&amp;', '&' ),
                'link_coursevania': item[link_cours_beg:link_cours_end],
                'link': href,
                'link_pictures': item[link_pic_beg:link_pic_end],
            } )
    #        else:
    #            print( 'Пустая строка' )
    #        print(item)
    #    print(udemy)
    return udemy


def save_file(items, path):
    with open( path, 'w', newline='' ) as file:
        writer = csv.writer( file, delimiter=';' )
        writer.writerow( ['Марка', 'Категория', 'Ссылка Coursevania', 'Ссылка Udemy'] )
        for item in items:
            writer.writerow( [item['title'], item['category'], item['link_coursevania'], item['link']] )


def parse():
    udemy = []
    pages = get_pages_count()
    for page in range( 0, pages ):
        print( f'Парсинг страницы {page} из {pages}...' )
        html = get_udemy( page )
        udemy.extend( get_content( html_clean( html ) ) )
    save_file( udemy, FILE )
    print( f'Получено {len( udemy )} курсов' )


# https://coursevania.com/courses/gann-box-trading-ninja-advance-diy-technical-analysis-tool/
# https://www.udemy.com/course/gann-box/?couponCode=1JAN21

parse()
