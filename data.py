class data:
    def __init__(self):
        self.login_url = "https://www.elibrary.ru/start_session.asp"
        self.headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'uk,en-US;q=0.9,en;q=0.8,ru;q=0.7',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }
        
        with open('auth.txt', 'r', encoding='utf-8') as f:
            try:
                text = f.read()
                self.auth = {'login' : text.split('\n')[0], 'password' : text.split('\n')[1]}
            except:
                self.auth = {}
