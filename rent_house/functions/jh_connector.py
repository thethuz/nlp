import requests


class JhConnector:

    def __init__(self, host):
        self.host = host
        self.is_login = False
        self.reconnect()

    def reconnect(self):
        session = requests.Session()
        session.get(self.host + '/api/authenticate')
        cookies = session.cookies.get_dict()
        # update header
        session.headers.update({
            'X-CSRF-TOKEN': cookies['CSRF-TOKEN'],
            'Cookie': 'CSRF-TOKEN=' + cookies['CSRF-TOKEN'] + '; JSESSIONID=' + cookies['JSESSIONID']
        })
        self.session = session

        if self.is_login:
            self.login(self.userName, self.password)

    def login(self, userName, password):
        session = self.session
        host = self.host
        self.is_login = True
        self.userName = userName
        self.password = password
        response = session.post(host + '/api/authentication', {
                                'j_username': userName, 'j_password': password, 'remember-me': 'false', 'submit': 'Login'})

        cookies = session.cookies.get_dict()
        # update header
        session.headers.update({
            'Cookie': 'CSRF-TOKEN=' + cookies['CSRF-TOKEN'] + '; JSESSIONID=' + cookies['JSESSIONID']
        })

        session.get(host + '/api/authenticate')

        cookies = session.cookies.get_dict()
        # update header
        session.headers.update({
            'X-CSRF-TOKEN': cookies['CSRF-TOKEN'],
            'Content-Type': 'application/json;charset=utf-8',
            'Cookie': 'CSRF-TOKEN=' + cookies['CSRF-TOKEN'] + '; JSESSIONID=' + cookies['JSESSIONID']
        })

    def get(self, api):
        session = self.session
        host = self.host
        response = session.get(host + api)
        if not response.ok:
            self.reconnect()
            response = self.session.get(host + api)
        return response

    def post(self, api, json):
        session = self.session
        host = self.host
        response = session.post(host + api, json=json)
        if not response.ok:
            self.reconnect()
            response = self.session.post(host + api, json=json)
        return response

    def put(self, api, json):
        session = self.session
        host = self.host
        response = session.put(host + api, json=json)
        if not response.ok:
            self.reconnect()
            response = self.session.put(host + api, json=json)
        return response