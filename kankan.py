from urllib import parse

import execjs
import requests

user = '18811112222'
password = '11111111'
def get_first():
    s = requests.session()
    url = 'https://ilogin.kankan.com/check/?u={}&v=100'.format(user)
    headers ={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Connection': 'keep-alive', 'Cookie': 'KANKANWEBUID=e209d3934c8cfce7a57395b9c4babcfd', 'Host': 'ilogin.kankan.com', 'Referer': 'http://www.kankan.com/', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    res = s.get(url,headers=headers)
    cookies = res.cookies.get_dict()
    print(res.status_code)
    print(res.cookies.get_dict())
    if 'check_result' in cookies.keys() and 'check_n' in cookies.keys():
        verifycode = cookies.get('check_result').split(':')[1].split(';')[0]
        check_n = cookies.get('check_n')

        print(verifycode,check_n)

        return verifycode,check_n,s
def get_p(check_n,verifycode,password):
    with open('kankan.js', 'r', encoding='UTF-8') as f:
        js2 = f.read()
        ctx2 = execjs.compile(js2)
        p = ctx2.call("getpwd",check_n,verifycode,password)
        print(p)
    return p
def get():
    url = 'https://ilogin.kankan.com/sec2login/'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Content-Length': '447',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ilogin.kankan.com', 'Origin': 'http://www.kankan.com', 'Referer': 'http://www.kankan.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    verifycode, check_n,s = get_first()
    check_n = parse.unquote(check_n)
    print(check_n)
    p = get_p(check_n,verifycode,password)
    print('p',p)

    data = {
        'p': p,
        'u': '18811112222',
        'n': check_n,
        'e': 'AQAB',
        'v': '100',
        'verifycode': verifycode,
        'login_enable': '0',
        'business_type': '107',
    }
    print('data',data)
    res = s.post(url, headers=headers, data=data)
    print(res.status_code)
    print(res.cookies.get_dict())


if __name__ == '__main__':
    get()
