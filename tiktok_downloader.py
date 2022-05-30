from pyrogram import Client
from pyrogram import filters
import time
from colorama import init
init()
from colorama import Fore, Back, Style

api_id = 12345
api_hash = "0123456789abcdef0123456789abcdef"
app = Client("my_account", api_id=api_id, api_hash=api_hash)

def indent(n):
    if n < 10: return f' {n}   '
    elif n < 100: return f' {n}  '
    elif n < 1000: return f' {n} '
    else: return f' {n}'

named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%H:%M:%S", named_tuple)

# reading urls from Favorite Videos.txt file
# bot cannot download from url like "https://www.tiktokv.com" it need "https://vt.tiktok.com"
with open('Favorite Videos.txt') as f:
    lines = f.readlines()
    list_of_links = [i[12:-1].replace('www.tiktokv', 'vt.tiktok') for i in lines][1::3][::-1]
    list_of_data = lines[0::3][::-1]

# check done_list for the presence lastn
with open('tiktok_done_links.txt') as f:
    done_lines = f.readlines()[::-1]
    try:
        lastn = int(done_lines[0].split()[0])
    except IndexError:
        for i in done_lines:
            if len(i) > 13:
                lastn = int(i.strip().split()[0])
        if not 'lastn' in locals(): lastn = 1
if lastn != 1:
    yesorno = input(f'Last downloaded video\'s queue is {lastn}. Continue downloading?\ny/n:').lower()
    if yesorno == 'y': n = lastn
    else: n = 0
else: n = 0

# changing done_links text file
done_links = open('tiktok_done_links.txt', 'a')
done_links.write(f'\n\nNew session\n{time_string}\n\n')

# bots username
userbot = 'ttfullbot'

# getting start
print(f'\n  {Back.GREEN}--Started--{Style.RESET_ALL}\n   {time_string}\n')

with app:
    app.send_message(userbot, list_of_links[n])
    print(f'{indent(1)}{list_of_links[n][28:]}', end='')
    n+=1

# if we got message "Наш новый бот" that is succesfully got the video:
@app.on_message(filters.user(userbot) & (filters.regex("Наш новый бот")))
def my_handler(client, message):
    global n
    if n >= len(list_of_links):
        print(f'\n\n  {Back.GREEN}Downloading is done!\n{Style.RESET_ALL}')
        app.send_message(userbot, 'Downloading is done!')
        quit()
    time.sleep(0.2)
    i = list_of_links[n]
    n += 1

    app.send_message(userbot, i)
    done_links.write(f'\n{indent(n)}  /{i[-8:-1]}')
    print(f'\n{indent(n)}{i[28:]}', end='')

# if we got "Не удалось скачать видео" that is we couldnt download the video:
@app.on_message(filters.user(userbot) & (filters.regex("Не удалось скачать видео.")))
def my_handler(client, message):
    global n
    if n >= len(list_of_links):
        print(f'\n\n  {Back.GREEN}Downloading is done!\n{Style.RESET_ALL}')
        app.send_message(userbot, 'Downloading is done!')
        quit()
    time.sleep(1.5)
    i = list_of_links[n]
    n += 1

    app.send_message(userbot, i)
    done_links.write(f'\n{indent(n)}  /{i[-8:-1]} FAIL')
    print(f'  {Back.RED}FAIL{Style.RESET_ALL}\n{indent(n)}{i[28:]}', end='')


# forwarding every video to the "favoritesfromtt"
@app.on_message(filters.user(userbot) & (filters.video))
def my_handler(client, message):
    message.forward('favoritesfromtt')
    app.send_message('favoritesfromtt', list_of_data[n])

app.run()
