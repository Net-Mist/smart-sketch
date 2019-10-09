import base64
import logging
import os
import socket
import subprocess
import sys
import uuid
from test import run

import tornado.ioloop
import tornado.options
import tornado.web
import signal

from color_grey_conversion import color_to_grey

IMG_FOLDER = os.path.join(os.path.dirname(__file__), "dataset/val_img")
INST_FOLDER = os.path.join(os.path.dirname(__file__), "dataset/val_inst")
LABEL_FOLDER = os.path.join(os.path.dirname(__file__), "dataset/val_label")

verbose = ((sys.argv[1] if 1 < len(sys.argv) else "") == "verbose")

APP_FOLDER = os.path.join(os.path.dirname(__file__), 'app', 'dist')
STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
EXPORT_LOCATION = "/tmp"
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "output")


def check_for_dataset_folder():
    if not os.path.isdir("dataset/"):
        os.mkdir("dataset/")
    if not os.path.isdir("dataset/val_img"):
        os.mkdir("dataset/val_img")
    if not os.path.isdir("dataset/val_inst"):
        os.mkdir("dataset/val_inst")
    if not os.path.isdir("dataset/val_label"):
        os.mkdir("dataset/val_label")


def parse_static_filepath(filepath):
    split_filepath = filepath.split('/')
    while len(split_filepath) > 2:
        split_filepath.pop(0)

    return '/'.join(split_filepath)


def run_model(filename):
    """Runs the pretrained COCO model"""
    # TODO check to see if this goes any faster with GPUS enabled...
    # TODO make is it so that concurrent users won't mess with eachother :P aka have hashed or something dataset routes...
    # that will also take a lot of cleaning up...
    # TODO figure out how to not do this from the command line...
    return run(OUTPUT_FOLDER, verbose)


def copy_file(old="avon.png", new="avon.png"):
    command_string = "cp " + old + " " + new
    subprocess.check_output(command_string.split(" "))


def make_processable(greyscale_fname, output_color_file):
    # Inst folder
    ouptut_greyscale_file = INST_FOLDER + "/" + greyscale_fname

    # Converts the file to greyscale and saves it to the inst folder?
    if verbose:
        print(output_color_file, ouptut_greyscale_file)

    color_to_grey.convert_rgb_image_to_greyscale(
        output_color_file,
        ouptut_greyscale_file
    )

    output_greyscale_file_labels = LABEL_FOLDER + "/" + greyscale_fname

    copy_file(ouptut_greyscale_file, output_greyscale_file_labels)
    copy_file(ouptut_greyscale_file, os.path.join(OUTPUT_FOLDER, greyscale_fname))


class UploadHandler(tornado.web.RequestHandler):
    def post(self, name=None):
        self.application.logger.info("Recieved a file")
        pic = str(self.request.body)
        # data URL
        base64_string = pic.split(",")[1]
        img_data = base64.b64decode(base64_string)
        color_file = "color.png"
        output_color_file = os.path.join(OUTPUT_FOLDER, color_file)

        # Writes the color image
        with open(output_color_file, "wb+") as out_f:
            out_f.write(img_data)

        greyscale_file = "greyscale.png"

        make_processable(greyscale_file, output_color_file)

        # We shouldnt need to pass it a string anymore
        export_image_location = run_model(greyscale_file)
        if verbose:
            print(export_image_location)

        static_image_location = parse_static_filepath(export_image_location)
        if verbose:
            print(static_image_location)

        self.write({
            "result": "success",
            "location": os.path.join(OUTPUT_FOLDER, os.path.basename(static_image_location))
        })


class MainApplication(tornado.web.Application):
    is_closing = False

    def signal_handler(self, signum, frame):
        logging.info('exiting...')
        self.is_closing = True

    def try_exit(self):
        if self.is_closing:
            tornado.ioloop.IOLoop.instance().stop()
            logging.info('exit success')

    def __init__(self, **settings):
        tornado.web.Application.__init__(self, **settings)
        self.port = settings.get('port', 80)
        self.address = settings.get('address', "0.0.0.0")
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.logger = logging.getLogger()

        # Tie the handlers to the routes here
        self.add_handlers(".*", [
            (r"/upload", UploadHandler),
            (r"/output/(.*)", tornado.web.StaticFileHandler, {"path": OUTPUT_FOLDER}),
            (r".*/static/(.*)", tornado.web.StaticFileHandler, {"path": STATIC_FOLDER}),
            (r"/img/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(APP_FOLDER, "img")}),
            (r"/css/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(APP_FOLDER, "css")}),
            (r"/js/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(APP_FOLDER, "js")}),
            (r"/^$", tornado.web.RedirectHandler, {"url": "/index.html"}),
            (r"/^#(.*)", tornado.web.RedirectHandler, {"url": "/index.html#{0}"}),
            (r"/(.*)", tornado.web.StaticFileHandler, {"path": APP_FOLDER}),
        ])

    def run(self):
        try:
            signal.signal(signal.SIGINT, self.signal_handler)
            self.listen(self.port, self.address)
            tornado.ioloop.PeriodicCallback(self.try_exit, 100).start()

        except socket.error as e:
            self.logger.fatal("Unable to listen on {}:{} = {}".format(
                self.address, self.port, e))
            sys.exit(1)
        self.ioloop.start()


if __name__ == "__main__":

    check_for_dataset_folder()
    tornado.options.define(
        "debug",
        default=False,
        help="Enable debugging mode."
    )
    tornado.options.define('port', default=9000, help='Port to listen on.')
    host = "0.0.0.0"
    if sys.platform == "win32":
        host = "127.0.0.1"
    tornado.options.define('address', default=host, help='Url')

    tornado.options.define('template_path', default=os.path.join(
        os.path.dirname(__file__), "templates"), help='Path to templates')
    tornado.options.parse_command_line()
    options = tornado.options.options.as_dict()
    if verbose:
        print(options)
    app = MainApplication(**options)
    app.run()
