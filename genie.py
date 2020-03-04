import requests
from bs4 import BeautifulSoup as BS
import pandas as pd
import matplotlib.pyplot as plt

titles=[]
artists=[]
genres=[]
results1=[]



headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36(KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

for i in range(0,12):

    if i<10:
            day="0"+str(i+1)
    else:
            day=str(i+1)

    ballad=0
    rap_hiphop=0
    dance=0
    pop=0
    RB=0
    indi_music=0
    electronica=0
    OST=0
    rock=0
    el_se=0
    for page in [1,2]:
        req= requests.get('https://www.genie.co.kr/chart/top200?ditc=M&ymd=2018' + day + '01&hh=07&rtm=N&pg='+str(page), headers = headers)
        html = BS(req.text, 'html.parser')

        tr_list = html.select('#body-content > div.newest-list > div > table > tbody > tr')

        for tr in tr_list:
            rank = tr.find('td',{'class':'number'}).text
            song = tr.get('songid')
            title = tr.find('td',{'class':'info'}).find('a',{'class':'title ellipsis'}).text
            artist = tr.find('td',{'class':'info'}).find('a',{'class':'artist ellipsis'}).text


            req2 = requests.get('https://www.genie.co.kr/detail/songInfo?xgnm=' + song , headers = headers)

            html2 = BS(req2.text, 'html.parser')

            genre = html2.find('div',{'class':'song-main-infos'}).find('div',{'class':'info-zone'}).find('ul',{'class':'info-data'}).find_all('span',{'class':'value'})[2].text

            if genre[:3] == '가요 ':
                if genre[5:] == '발라드':
                    ballad += 1
                elif genre[5:] == 'R&B/소울':
                    RB += 1
                elif genre[5:] == '인디':
                    indi_music += 1
                elif genre[5:] == '댄스':
                    dance += 1
                elif genre[5:] == '랩/힙합':
                    rap_hiphop += 1
                elif genre[5:] == '일렉트로니카':
                    electronica += 1
                elif genre[5:] == '락':
                    rock += 1
                else:
                    el_se +=1

            elif genre[:3] == 'OST':
                OST += 1

            elif genre[:3] == 'POP':
                if genre[6:] == '팝':
                    pop += 1
                elif genre[6:] == '일렉트로니카':
                    electronica += 1
                elif genre[6:] == '락':
                    rock += 1
                else:
                    el_se +=1
            else:
                el_se +=1
    sum_all=[ballad, rap_hiphop, dance, rock, pop, RB, indi_music, electronica, OST, el_se]
    results1.append([ballad, rap_hiphop, dance, rock, pop, RB, indi_music, electronica, OST, el_se, sum(sum_all)])       

        
    
data1=pd.DataFrame(results1)
data1.columns = ['발라드', '랩/힙합', '댄스', '락', '팝', 'R&B', '인디', '일렉트로니카', 'OST','그 외 장르', '합계']
data1.index = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
data1