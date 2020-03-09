# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import logging.config

import tornado.ioloop
import tornado.web
from tornado.options import options

from config import settings
from app.handlers import IndexHandler, UploadHandler, UploadDraftParams
from app.handlers import DraftHandler, DraftSocketHandler
from app.game_managers import DraftGameManager

def main():
    """Creates Tornado Application and starts the IO Loop
    """

    # Get the Port and Debug mode from command line options
    options.parse_command_line()

    # create logger for app
    logger = logging.getLogger()

    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT)

    draft_game_manager = DraftGameManager()

    urls = [
        # (r"/$", IndexHandler),
        # (r"/ygoserver$"),
        (r"/upload/deck$", UploadHandler, dict(game_manager=draft_game_manager)),
        (r"/upload/params$", UploadDraftParams, dict(game_manager=draft_game_manager)),
        (r"/ygoserver/ws$", DraftSocketHandler, dict(game_manager=draft_game_manager))
    ]

    # Create Tornado application
    application = tornado.web.Application(
        urls,
        debug=options.debug,
        autoreload=options.debug)

    # Start Server
    logger.info("Starting App on Port: {} with Debug Mode: {}".format(options.port, options.debug))
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()