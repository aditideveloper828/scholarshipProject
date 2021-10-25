from qrScanApp import application, storage
from qrScanApp.models import User, Log

@application.shell_context_processor
def make_shell_context():
    return {'db': storage, 'User': User, 'Log': Log}