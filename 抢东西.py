import winsound
import requests
import time

is_huo = False
header={'User-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
while not is_huo:
    response = requests.get(url='https://www.moack.co.kr/cart.php?a=add&pid=60', headers=header)
    print(response.encoding)
    if 'Out of Stock' in str(response.content):
        print("*"*30)
        time.sleep(5)
    else:
        is_huo = True
while is_huo:
    winsound.Beep(600,1000)
    time.sleep(1)