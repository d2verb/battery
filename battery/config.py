class Basic(object):
    SECRET_KEY = "********"
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INSTANCE_PATH = None

class Development(Basic):
    pass

class Testing(Basic):
    INSTANCE_PATH = "/tmp/battery/instance"

class Production(Basic):
    pass
