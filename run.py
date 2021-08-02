from concurrent.futures.thread import ThreadPoolExecutor
import time
from datetime import datetime
import threading
import concurrent.futures
from app import app
from system_config import Config
from app.mod_data_extraction import finviz, yahoo_finance, investingdotcom


executor = ThreadPoolExecutor(2)

def main():
    while True:
        print(datetime.now().strftime("%H:%M:%S"))
        time.sleep(5)



def startFlaskApp():
    app.run(host=Config.host, port=Config.port, debug=True, use_reloader=False)


def startMain():
    mainThread = threading.Thread(target=main)
    mainThread.setName("main")
    mainThread.start()



def runProgram():
    executor.submit(startMain())


runProgram()
startFlaskApp()
