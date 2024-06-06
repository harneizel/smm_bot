import os
import os.path as path

def history_file(tg_id):
    if not path.exists(f"../database/histories/{tg_id}.txt"):
        os.mknod(f'../database/histories/{tg_id}.txt')
        print("файл созадан")


history_file(1234)