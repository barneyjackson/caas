#!/usr/bin/env python

from flask import Flask, request
import cgi
import json
import random
import urllib           

application = Flask(__name__, static_folder='static', static_url_path='')

retorts = {
    0: 'Nah, it\'s shit.',
    1: 'This bit\'s great! Not.',
    2: 'And this is your best work?',
    3: 'WTF is that??',
    4: 'This was clearly written by a drunkard.',
    5: 'This just doesn\'t make sense.',
    6: 'A goldfish could do better than that.',
    7: 'I don\'t think this meets anyones standards...',
    8: 'Just, wrong.',
    9: 'Sick and wrong.',
    10: 'This needs redoing.',
    11: 'Redo this bit please.',
    12: 'I think you should try again here.',
    13: 'Just bin it.',
    14: 'Start again, seriously.',
    15: 'It\'s like you suddenly started writing with your eyes closed?',
    16: 'This was clearly an off day for you...',
    17: 'What happened here?!',
    18: 'You couldn\'t be more wrong',
    19: 'Are you retarded?',
    20: 'You can do better than this.',
    21: 'It just gets worse and worse.'
}

@application.route("/")
def index():
    return application.send_static_file('index.html')

@application.route("/criticise/<path:victim>")
def criticise(victim):
    sock = urllib.urlopen(victim)
    html = sock.read()           
    sock.close()
    lines = html.rstrip().split('\n')
    looking = True
    while looking:
        line_id = random.choice(range(len(lines)))
        if (not lines[line_id].isspace()) and lines[line_id]:
            looking = False
    line = cgi.escape(lines[line_id], quote=True)
    prev_line_id = line_id - 1
    prev_line = '...'
    if prev_line_id >= 0:
        prev_line = cgi.escape(lines[prev_line_id], quote=True)
    next_line_id = line_id + 1
    next_line = '...'
    if next_line_id < len(lines):
        next_line = cgi.escape(lines[next_line_id], quote=True)
    lines = {
        '0': {
            'lineno': prev_line_id + 1,
            'text': prev_line
        },
        '1': {
            'lineno': line_id + 1,
            'text': line
        },
        '2': {
            'lineno': next_line_id + 1,
            'text': next_line
        }
    }

    used = [ int(x) for x in request.args.get('u').split(',') if x != '']
    thinking = len(used) != len(retorts) 
    retort = 'You\'ve had enough. I\'m bored.'
    while thinking:
        options = range(len(retorts))
        retort_id = random.choice(options)
        thinking = retort_id in used
        if thinking == False:
            retort = retorts[retort_id]
            used.append(retort_id)
    print victim + ' -> ' + retort + ' Remaining: ' + str([ x for x in retorts.keys() if x not in used ] or str(None))
    return json.dumps({'lines': lines, 'retort': retort, 'used': used})

if __name__ == "__main__":
    application.run(debug=True)
