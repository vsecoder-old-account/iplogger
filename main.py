#!/usr/bin/python

# imports
from logging import error
import mod.geo
import iptools
import os
import string
import random
import uvicorn
import mod.utils
from fastapi import FastAPI
from fastapi import Request
from starlette.templating import Jinja2Templates
from starlette.responses import Response

# create DB
try:
    import create_db
except:
    pass

# Create server
app = FastAPI()
templates = Jinja2Templates('templates')

## Get IP Range
IPRANGE = os.environ.get('IPRANGE', '52.0.0.0/30')

## Private IP Addresses
private = iptools.IpRangeList(
    '0.0.0.0/8',      '10.0.0.0/8',     '100.64.0.0/10', '127.0.0.0/8',
    '169.254.0.0/16', '172.16.0.0/12',  '192.0.0.0/24',  '192.0.2.0/24',
    '192.88.99.0/24', '192.168.0.0/16', '198.18.0.0/15', '198.51.100.0/24',
    '203.0.113.0/24', '224.0.0.0/4',    '240.0.0.0/4',   '255.255.255.255/32'
)

link = "http://0.0.0.0/"

# Server home page
@app.get('/')
def home_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

# Server create logger page
@app.get('/create')
def logger_page(request: Request, password):
    url = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
    mod.utils.create_logs(url, password)
    return templates.TemplateResponse('create.html', {'request': request, 'url': url})

# Server look logs page
@app.get('/log/{url}')
def log_page(request: Request, url, password):
    res = mod.utils.get_log(url, password)
    if res != "Forgot password!":
        return templates.TemplateResponse('log.html', {'request': request, 'link': f'{link}log/{url}', 'ipList': res["data"]})
    else:
        return "Forgot password!"

# Server logger page
@app.get('/{url}')
def logger_page(request: Request, url):
    try:
        user_agents = request.headers.get('User-Agent')
        ip = request.client.host
    except Exception as e:
        result = {'ip': '-.-.-.-', 'user_agents': '', 'error': f'{e}'}
    if ip not in private:
        result = mod.geo.lookup(ip, user_agents)
    else:
        result = {'ip': ip, 'user_agents': user_agents, 'error': 'IP is private'}
    mod.utils.append_logs(url, result)
    return templates.TemplateResponse('logger.html', {'request': request})

# Server api page
@app.get('/api/{ip}')
def api_page(request: Request, ip):
    try:
        user_agents = request.headers.get('User-Agent')
        print(ip)
    except Exception as e:
        return {'ip': '-.-.-.-', 'user_agents': user_agents, 'error': f'{e}'}
    if ip not in private:
        result = mod.geo.lookup(ip, user_agents)
        return result
    return {'ip': ip, 'user_agents': user_agents, 'error': 'IP is private'}

# Start server
if __name__ == "__main__":
    # dev
    uvicorn.run('main:app',
        host="0.0.0.0", 
        port=int(os.environ.get("PORT", 5000)),
        log_level="debug",
        http="h11",
        reload=True, 
        use_colors=True,
        workers=3
    )
    # prod
    #uvicorn.run('app:app',
    #    host="0.0.0.0", 
    #    port=80,
    #    http="h11"
    #)
