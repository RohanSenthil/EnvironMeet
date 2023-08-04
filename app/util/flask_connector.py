from .werkzeug_connector import InputWerkzeug, Output, Connector
from flask import abort


class InputFlask(InputWerkzeug):
    pass

class OutputFlask(Output):
    def error(self):
        abort(500)