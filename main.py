from settings import token, chat_id, url
import requests
from bs4 import BeautifulSoup
import time

TOKEN = token

send_link = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text="

def get_car_links():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
    html_response = requests.get(url=url, headers = headers)
    soup = BeautifulSoup(html_response.text, 'lxml')
    quotes = soup.find_all('div', class_='ListingItem')
    links = []
    for quot in quotes:
        temp = quot.find('a', class_='Link ListingItemTitle__link').get('href')
        links.append(temp)
    return links

all_links = get_car_links()
past_link = all_links[0]
while True:
    all_links = get_car_links()
    print(f"top link = {all_links[3]}")
    print(f"prev link = {past_link}")
    if past_link != all_links[3]:
        print(past_link)
        i = 0
        temp = []
        while past_link != all_links[i]:
            temp.append(all_links[i])
            i += 1
            print(i)
        answer = "Появились новые машины:\n"
        for car in temp:
            answer += f"{car}\n"
        past_link = all_links[0]
        requests.post(send_link+answer)
    time.sleep(60)
