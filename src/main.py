from src.view.www import app, runApp
import os


def fileRead(fileName):
    with open(fileName) as file:
        configInfo = file.readlines()
    for i in range(len(configInfo)):
        configInfo[i] = configInfo[i].removesuffix("\n")
    return configInfo


def main():
    fileToRead = os.path.abspath('config.txt')
    config = fileRead(fileToRead)

    if config is not None and len(config) == 8:
        public, debug, host, user, password, database, givenSessionTime, secretKey = config
        public = bool(int(public))
        debug = bool(int(debug))
        givenSessionTime = int(givenSessionTime)

        runApp(host, user, password, database, givenSessionTime, secretKey, public, debug)
    else:
        print("Brak odpowiedniego pliku konfiguracyjnego lub nie zawiera on wszystkich parametrów!")
        exit()


if __name__ == '__main__':
    main()
