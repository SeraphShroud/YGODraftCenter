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
from service.api_requests import APIRequest
from service.ygo_card_db_service import YGOCardDBService
from enums.strings import MongoDB


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

    card_db_service = YGOCardDBService(MongoDB.DB_NAME, MongoDB.CARD_COLLECTION_NAME, MongoDB.DB_URL)
    if len(card_db_service.get_collection()) < 20:
        APIRequest.populate_card_info_db(card_db_service)

    urls = [
<<<<<<< HEAD
        # (r"/$", IndexHandler),
        # (r"/ygoserver$"),
        (r"/upload/deck$", UploadHandler, dict(game_manager=draft_game_manager)),
        (r"/upload/params$", UploadDraftParams, dict(game_manager=draft_game_manager)),
        (r"/ygoserver/ws$", DraftSocketHandler, dict(game_manager=draft_game_manager))
=======
        (r"/$", IndexHandler),
        #(r"/tic-tac-toe$", DraftHandler),
        (r"/upload$", UploadHandler),
        (r"/ygoserver/ws$", DraftSocketHandler,
         dict(game_manager=draft_game_manager))
>>>>>>> 517d6a6969b76ee3b2d96460ee92d0856dd68354
    ]

    # Create Tornado application
    application = tornado.web.Application(
        urls,
        debug=options.debug,
        autoreload=options.debug)

    # Start Server
    logger.info(f"Starting App on Port: {options.port} with Debug Mode: {options.debug}")
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
