import requests, json, sys
from flask import Flask
from flask_cors import CORS

def d2j(d): return json.dumps(d)

def get_from_youtube_chat(vid, limit=30):
    try:
        url = 'https://studio.youtube.com/live_chat?is_popout=1&v=' + vid
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        html = str(response.text)
        head = html.find('{"responseContext"')
        tail = html.find('};', head) + 1
        json_str = html[head:tail]
        json_obj = json.loads(json_str)
        actions = json_obj['contents']['liveChatRenderer']['actions']
        lines = []
        for action in actions:
            try:
                author = action['addChatItemAction']['item']['liveChatTextMessageRenderer']['authorName']['simpleText']
                author = f'<span class="author">{author}</span>'
                runs = action['addChatItemAction']['item']['liveChatTextMessageRenderer']['message']['runs']
                content = ''
                for run in runs:
                    if 'text' in run.keys(): 
                        text = run['text']
                        content += f'<span class="content">{text}</span>'
                    if 'emoji' in run.keys(): 
                        url = run['emoji']['image']['thumbnails'][0]['url']
                        content += f'<img src={url} style="width:16px">'
                line = f'{author} {content} <br/>'
                lines += [line]
            except Exception as e:
                pass
        if len(lines) > limit:
            lines = lines[-limit:]
        return '\n'.join(lines)
    except Exception as e:
        return 'Error'

if len(sys.argv) != 2:
    print('python3 server.py <PORT>')
    exit()

HOST = '0.0.0.0'
PORT = int(sys.argv[1])
app = Flask(__name__, template_folder='.')
CORS(app)

@app.route("/api/data/<vid>/<limit>")
def api_data(vid, limit):
    data = get_from_youtube_chat(vid, int(limit))
    return data

print(f'HOST={HOST} PORT={PORT}')
app.run(host=HOST, port=PORT)



'''
# vid = 'PTUafmTYrsA'
# data = get_from_youtube_chat(vid)
# print('\n'.join(data))
def remove_emoji(string):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

# head = html.find('"actions":') + 10
# tail = html.find('"actionPanel"', head) - 1
# print(json_str[:1000])
# print(json_str[-1000:])
# print(json_str[:1000])
# json_str = remove_emoji(json_str)
# json_str.encode(encoding='UTF-8')
# print(json_str[185:205])
# print(json_str[195])
'''