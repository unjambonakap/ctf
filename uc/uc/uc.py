
import requests
from http.cookiejar import MozillaCookieJar
from urllib.parse import *
from chdrft.sys.opa_keyring import Keyring
from chdrft.utils.cache import Cachable
import chdrft.utils.misc as misc
import re
import logging
import os
import time
import copy
from enum import Enum

def get_level_dumpname(level):
    return re.sub('\s', '_', level.lower())


class uc(Cachable):

    class Levels(Enum):
        TUTORIAL = 'Tutorial'
        NEW_ORLEANDS = 'New Orleans'
        SYDNEY = 'Sydney'
        HANOI = 'Hanoi'
        REYKJAVIK = 'Reykjavik'
        CUSCO = 'Cusco'
        JOHANNESBURG = 'Johannesburg'
        WHITEHORSE = 'Whitehorse'
        SANTA_CRUZ = 'Santa Cruz'
        JAKARTA = 'Jakarta'
        ADDIS_ABABA = 'Addis Ababa'
        NOVOSIBIRSK = 'Novosibirsk'
        MONTEVIDEO = 'Montevideo'
        ALGIERS = 'Algiers'
        VLADIVOSTOK = 'Vladivostok'
        LAGOS = 'Lagos'
        BANGALORE = 'Bangalore'
        CHERNOBYL = 'Chernobyl'
        HOLLYWOOD = 'Hollywood'

    login_key = 'uc_keyring_key'
    base_url = 'https://microcorruption.com'

    re_not_logged = re.escape(
        "<button class='button orange' type='SUBMIT'>Log in</button>")

    path_login = 'login'
    path_get_levels = 'get_levels'
    path_set_level = 'cpu/set_level'
    path_alive = 'cpu/is_alive'
    path_debug = 'cpu/reset/debug'
    path_nodebug = 'cpu/reset/nodebug'
    path_snapshot = 'cpu/snapshot'
    path_load = 'cpu/load'
    path_root = '/'
    path_kill = 'cpu/dbg/kill'

    def build_url(self, path):
        return urljoin(self.base_url, path)

    def __init__(self, login, cookiejar, **kwargs):
        super().__init__(**kwargs)

        self.keyring = Keyring()
        self.json = misc.JsonUtils()

        self._login = login
        self.kr_key = '{}#{}'.format(self.login_key, self._login)
        self._pwd = self.keyring.get_or_set(
            self.kr_key,
            help='uc login password:')

        for x in uc.__dict__:
            m = re.match('^path_(.*)', x)
            if not m:
                continue
            val = m.group(1)
            url_attr = '{}_url'.format(val)
            url = self.build_url(getattr(uc, x))
            setattr(self, url_attr, url)

        self.session = requests.Session()
        self.jar = MozillaCookieJar(cookiejar)
        if os.path.isfile(cookiejar):
            self.jar.load(ignore_discard=True)
        self.session.cookies = self.jar
        self.last_token = None

    def is_logged(self, req):
        ans = re.search(self.re_not_logged, req.text)
        return ans is None

    def do_req(self, mode, url, **kwargs):
        login_req = False
        if 'login_req' in kwargs:
            login_req = kwargs['login_req']
            kwargs.__delitem__('login_req')

        cp = copy.deepcopy(kwargs)
        req = requests.Request(mode, url, **cp)
        preq = self.session.prepare_request(req)
        data = '''============= Request =============
Url: {}
Headers: {}
Body: {}
EOF'''.format(req.url, preq.headers, preq.body)
        res = self.session.send(preq)
        logging.info(data)
        # logging.info(res.headers)
        # logging.info(res.text)

        token = re.search(
            '<meta content="([^"]*)" name="csrf-token" />',
            res.text)
        if token:
            self.last_token = token.group(1)
            logging.info('last token >> {}'.format(self.last_token))

        logging.info(self.jar)
        self.jar.save(ignore_discard=True)
        if not login_req and not self.is_logged(res):
            self.login()
            kwargs['login_req'] = True
            res = self.do_req(mode, url, **kwargs)
            assert self.is_logged(res)

        return res

    def do_post(self, url, **kwargs):
        return self.do_req('POST', url, **kwargs)

    def do_get(self, url, **kwargs):
        return self.do_req('GET', url, **kwargs)

    def login(self):
        r = self.do_post(self.login_url, login_req=True)
        data = r.text

        post = dict(
            name=self._login,
            password=self._pwd,
            authenticity_token=self.last_token)

        self.do_post(self.login_url, data=post, login_req=True)

    def json_req(self, url, get=False, data={}, **kwargs):
        data = dict(body=data)
        if not self.last_token:
            self.login()
        headers = {}
        headers['x-requested-with'] = 'XMLHttpRequest'
        headers['x-csrf-token'] = self.last_token
        if get:
            r = self.do_get(url, headers=headers, login_req=True, **kwargs)
        else:
            r = self.do_post(url, json=data,
                             headers=headers, login_req=True, **kwargs)
        logging.info(r.text)
        return self.json.decode(r.text)

    def alive(self):
        r = self.json_req(self.alive_url, {})
        assert r

    def set_level(self, level):
        r = self.json_req(self.set_level_url, data=dict(level=level))
        assert r

    def reset(self, debug=True):
        if debug:
            r = self.json_req(self.debug_url)
        else:
            r = self.json_req(self.nodebug_url)
        assert r

    def load(self):
        self.json_req(self.load_url)

    def kill(self):
        self.json_req(self.kill_url)

    def root(self):
        self.do_get(self.root_url)

    def get_levels(self):
        r = self.json_req(self.get_levels_url, get=True)
        return r['levels']

    def get_snapshot(self):
        now = int(time.time())
        params = dict(x=now)
        r = self.json_req(self.snapshot_url, get=True, params=params)
        return r
