import time
from app import app
from system_config import Config


def main():
    app.run(host=Config.host, port=Config.port, debug=True, use_reloader=False)

    while True:
        print("test")
        time.sleep(5)


main()
