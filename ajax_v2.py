import requests
import json
from bs4 import BeautifulSoup as bs4


def get_content(html):
    items = html.split( 'nn<div "="" class="stm_lms_courses__single no-sale="" stm_lms_courses__single_animation=""' ) # seporator into parts
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
        print( item[title_beg:title_end].replace( '&amp;', '&' ) )
        print( item[category_beg:category_end].replace( '&amp;', '&' ) )
        print( item[link_cours_beg:link_cours_end] )
        print( item[link_pic_beg:link_pic_end] )
        if len( item[title_beg:title_end] ) > 0:
            udemy.append( {
                'title': item[title_beg:title_end].replace( '&amp;', '&' ),
                'category': item[category_beg:category_end].replace( '&amp;', '&' ),
                'link_coursevania': item[link_cours_beg:link_cours_end],
                'link_pictures': item[link_pic_beg:link_pic_end],
                #            'link': HOST + item.find('span', class_='link').get('href'),
                #            'usd_price': item.find('strong', class_='green').get_text(),
                #            'uah_price': uah_price,
                #            'city': item.find('svg', class_='svg_i16_pin').find_next('span').get_text(),
            } )
        else:
            print( 'Пустая строка' )
    #        print(item)
    print( udemy )
    return udemy


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
           'Accept': 'application/json, text/javascript, */*; q=0.01'}

url = 'https://coursevania.com/wp-admin/admin-ajax.php?offset=1&template=courses/grid&args=' \
      '{"posts_per_page":"10"}' \
      '&action=stm_lms_load_content&nonce=e08ead6046&sort=date_high'

# https://coursevania.com/courses/gann-box-trading-ninja-advance-diy-technical-analysis-tool/
# https://www.udemy.com/course/gann-box/?couponCode=1JAN21

res = requests.get( url, headers=headers )
soup = bs4( res.content, 'html.parser' )
data = str( soup ).replace( '\\', '' ).replace( "'", "" )
# {"content":"n
data = data.replace( '{"content":"n    ', '' )
# n this="">n        <div>n            <div class="stm_lms_lazy_image"><img ="" "="" alt="98dab8124423244675bd47e810e90182" class="lazyload
data = data.replace(
    'n this="">n        <div>n            <div class="stm_lms_lazy_image"><img ="" "="" alt="98dab8124423244675bd47e810e90182" class="lazyload',
    '' ).replace( "'", "" )
# nn<div "="" class="stm_lms_courses__single no-sale="" stm_lms_courses__single_animation=""
get_content( data )

# separator = data.split('nn<div "="" class="stm_lms_courses__single no-sale="" stm_lms_courses__single_animation=""')
# i =0
# for stroka in separator:
#    print(stroka)
#    i += 1
# print('i=', i-1)
# data = str(soup).replace('\\n', '').replace('\\', '').replace("'", "").replace('&gt','').replace('&lt','')
beg = data.find( 'href' ) + 6
# end = data.find('"', beg)
link = data[beg:data.find( '"', beg )]
total = data[data.find( '"total"' ) + 8:data.find( '"pages"' ) - 1]
pages = data[data.find( '"pages"' ) + 8:data.rfind( '}' )]
print( link )
print( total )
print( pages )
print( data.find( '"pages"' ) + 8 )
print( data.rfind( '}' ) )
# print(end)
# divs = soup.find_all('div', attrs={'class': 'stm_lms_courses__single--title'})
# print(divs)
# i = 0
# for div in divs:
#    title = div.find('h5').text
#    href = div.find('a')['href']
#    print("{} - {}".format(title, href))
#    i += 1
# print(div)
# Convert data to dict
# print(res.content)
# data = json.load(res.text)
# data = data = json.dumps(data)
# print(data)
# soup = bs4(res.content, 'lxml')

# print(soup)
# soup = bs4(json_.content, 'html.parser')
# print(json_.json())
file = open( 'ajax3.html', 'w' )
# file.write(str(soup))
file.write( data )

# print(json_.json())
file.close()
# print(soup)
