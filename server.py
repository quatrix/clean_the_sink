import tornado.ioloop
import tornado.web
import StringIO
import sys
from PIL import Image

class DirtySinkHandler(tornado.web.RequestHandler):
    def post(self):
        file_body = self.request.files['sink'][0]['body']
        img = Image.open(StringIO.StringIO(file_body))
        img.save("/var/www/html/edisdead.com/sink.jpg")




if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/your_dirty_sink", DirtySinkHandler),
    ], debug=True)

    application.listen(34433)
    tornado.ioloop.IOLoop.current().start()
