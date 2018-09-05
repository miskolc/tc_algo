import quickfix
from client import Application

filename = "client.cfg"

if __name__ == '__main__':
    try:
        settings = quickfix.SessionSettings(filename)
        application = quickfix.Application
        storeFactory = quickfix.FileStoreFactory(settings)
        logFactory = quickfix.FileLogFactory(settings)
        acceptor = quickfix.SocketAcceptor(application, storeFactory, settings, logFactory)
        acceptor.start()
        # while condition == true: do something
        acceptor.stop()
    except quickfix.ConfigError as e:
        print(e)
