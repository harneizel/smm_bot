import datetime
import os


class Logger:
    def __init__(self):
        self.folder = 'configs/logs/'
        os.makedirs(self.folder, exist_ok=True)
        self.path = self._get_actual_path()

    def write_log(self, text: str):
        date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        text = f"[{date}] {text}"
        file_content = self._read_file()
        if file_content and file_content[-1] != '\n':
            print(file_content[-1])
            text = '\n' + text

        self._write_file(text)

    # additional functions below

    def _get_actual_path(self, ):
        today = datetime.date.today()
        start_of_week = today - datetime.timedelta(days=today.weekday())
        end_of_week = start_of_week + datetime.timedelta(days=6)
        filename = f"{start_of_week.strftime('%d.%m.%Y')}-{end_of_week.strftime('%d.%m.%Y')}.txt"
        return self.path + filename

    def _read_file(self):
        self.__check_exists()
        with open(self.path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text

    def _write_file(self, text: str):
        self.__check_exists()
        with open(self.path, "a", encoding='utf-8') as f:
            f.write(text)

    def __check_exists(self):
        if not os.path.exists(self.path):
            with open(self.path, 'w', encoding='utf-8') as f:
                f.write("")


if __name__ == '__main__':
    logger = Logger()

    logger.write_log('sigma')
