import tornado.web
import tornado.websocket
import tornado.httpserver
import os
import logging
import ast

from db import get_session
from db.models import Account, Transaction
from util.validate import validate_json
from util.ops import Operations, CODES

session = get_session()

#__name__ = 'Tornado Server'

logging.basicConfig(filename='runa.log', level=logging.INFO)
logger = logging.getLogger(__name__)

settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

sockets = []

VALID_OPS = {'deposit': Operations.deposit,
             'withdrawal': Operations.withdrawal,
             'transfer': Operations.transfer,
             'get_balances': Operations.balance}


class BankingSocketHandler(tornado.websocket.WebSocketHandler):

    

    def check_origin(self, origin):
        return True

    def open(self):
        sockets.append(self)
        print("{} sockets".format(len(sockets)))

    def on_close(self):
        global sockets
        sockets.remove(self)
        print("{} sockets".format(len(sockets)))

    def on_message(self, message_json):
        global sockets
        try:
            m = ast.literal_eval(message_json)
            logger.info(m)
            method, args = validate_json(m)
        except Exception as err:
            self.write_message('NOK:{}'.format(CODES[800]).format(err))

        code, resp = VALID_OPS[method](**args)

        if code:
            self.write_message('OK:{}'.format(resp))
        else:
            self.write_message('NOK:{}'.format(resp))

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class ApiHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self, *args):
        name = self.get_argument('name')
        acc = session.query(Account).filter(Account.name == name).one_or_none()
        if not acc:
            acc = Account(name=name)
            logger.info(session.add(acc))
            logger.info(session.commit())

        a = acc
        data = {
            "id": a.id, 'value': '{}-{}-{}-{}'.format(a.name, a.balance, a.ccy, a.limit)}
        logger.info(data)
        for c in sockets:
            c.write_message(data)
        self.finish()

    @tornado.web.asynchronous
    def post(self):
        pass


application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/ws", BankingSocketHandler),
    (r'/api', ApiHandler),
], **settings)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8880)
    tornado.ioloop.IOLoop.instance().start()
