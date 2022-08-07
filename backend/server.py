import requests, json, sys, datetime
from flask import Flask, request
from flask_cors import CORS

if len(sys.argv) != 2:
    print('python3 server.py <PORT>')
    exit()

jm_comments = []

def d2j(d): return json.dumps(d)
def e2t(e): return datetime.datetime.fromtimestamp(e)
def now(): return datetime.datetime.now()
def t2s(t, format="%Y-%m-%d %H:%M:%S"): return t.strftime(format)
def s2t(s, format="%Y-%m-%d %H:%M:%S"): return datetime.datetime.strptime(s,format)

def to_html(comment):
    html = f'<span class="author">{comment["author"]}</span> '
    for e in comment['content']:
        if e['type'] == 'text':
            html += f'<span class="text">{e["data"]}</span>'
        if e['type'] == 'emoji':
            html += f'<img class="emoji" src={e["url"]}>'
    html += ' <br>'
    return html

def get_yt_comments(vid, limit=30):
    try:
        url = 'https://studio.youtube.com/live_chat?is_popout=1&v=' + vid
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        html = str(response.text)
        head = html.find('{"responseContext"')
        tail = html.find('};', head) + 1
        json_str = html[head:tail]
        json_obj = json.loads(json_str)
        actions = json_obj['contents']['liveChatRenderer']['actions']
        comments = []
        for action in actions:
            try:
                author = action['addChatItemAction']['item']['liveChatTextMessageRenderer']['authorName']['simpleText']
                runs = action['addChatItemAction']['item']['liveChatTextMessageRenderer']['message']['runs']
                timestamp = action['addChatItemAction']['item']['liveChatTextMessageRenderer']['timestampUsec']
                timestamp = e2t(int(timestamp[:-6]))
                content = []
                for run in runs:
                    if 'text' in run.keys(): 
                        data = run['text']
                        content += [{'type':'text','data':data}]
                    if 'emoji' in run.keys(): 
                        url = run['emoji']['image']['thumbnails'][0]['url']
                        content += [{'type':'emoji','url':url}]
                comment = {'timestamp': timestamp, 'author': author, 'content': content}
                comments += [comment]
            except Exception as e:
                pass
        if len(comments) > limit:
            comments = comments[-limit:]
        return comments
    except Exception as e:
        return [] #'Error'

def add_jm_comments(author, content):
    comment = {'timestamp': now(), 'author': author, 'content': [{'type':'text','data':content}]}
    jm_comments.append(comment)
    return True

HOST = '0.0.0.0'
PORT = int(sys.argv[1])
app = Flask(__name__, template_folder='.')
CORS(app)

@app.route("/api/data/<vid>/<int:limit>")
def api_data(vid, limit):
    yt_comments = get_yt_comments(vid, limit)
    comments = (yt_comments + jm_comments)
    comments = sorted(comments, key=lambda c: c['timestamp'])
    comments = comments[-limit:]
    htmls = [to_html(c) for c in comments]
    return '\n'.join(htmls)

@app.route("/api/add")
def api_add():
    author = request.args.get('author')
    content = request.args.get('content')
    return str(add_jm_comments(author, content))

@app.route("/api/reset")
def api_reset():
    global jm_comments
    jm_comments = []
    return str(True)

print(f'HOST={HOST} PORT={PORT}')
app.run(host=HOST, port=PORT)



'''
# vid = 'PTUafmTYrsA'
# data = get_yt_comments(vid)
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