import logging
import websocket

from codebattleclient.internals.Board import Board
from codebattleclient.internals.TurnAction import TurnAction

logger = logging.getLogger(__name__)


def sample(ws):
    pass


class GameClient:
    def __init__(self, url):
        path = url.replace("http", "ws")
        path = path.replace("board/player/", "ws?user=")
        path = path.replace("?code=", "&code=")

        logger.info("connecting... {}".format(path))
        self.socket = websocket.WebSocketApp(path,
                                             on_message=lambda ws, msg: self.on_message(ws, msg),
                                             on_error=lambda ws, err: self.on_error(ws, err),
                                             on_close=lambda ws: self.on_close(ws),
                                             on_open=lambda ws: self.on_open(ws))

    def run(self, on_turn=lambda a: TurnAction.STOP):
        self.on_turn = on_turn
        self.socket.run_forever()

    def on_message(self, ws, message):
        board = Board(message.lstrip("board="))
        action = self.on_turn(board)
        try:
            self.__send(action.value)
        except Exception:
            action = TurnAction.STOP
            self.__send(action.value)
        return board


    def __send(self, msg):
        logger.info('Sending: {}'.format(msg))
        self.socket.send(msg)

    def on_open(self, ws):
        logger.info('Connection established: {}'.format(ws))

    def on_error(self, ws, error):
        logger.error(error)

    def on_close(self, ws):
        logger.info("### disconnected ###")
