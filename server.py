import tornado.ioloop
import tornado.web
import StringIO
import sys
import statsd
import logging

from sink_inspector import get_dirtiness
from PIL import Image

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
statsd_client = statsd.StatsClient('localhost', 8125)


class DirtySinkHandler(tornado.web.RequestHandler):
    def post(self):
        file_body = self.request.files['sink'][0]['body']
        img = Image.open(StringIO.StringIO(file_body))
        dest = "/var/www/html/edisdead.com/sink.jpg"
        img.save(dest)
        dirtiness = get_dirtiness(dest)
        logging.info('dirtiness: %d' ,dirtiness)
        statsd_client.gauge('sink', dirtiness)


if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/your_dirty_sink", DirtySinkHandler),
    ], debug=True)

    application.listen(34433)
    tornado.ioloop.IOLoop.current().start()