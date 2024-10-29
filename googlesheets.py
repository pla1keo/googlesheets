import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import pytz

msk_timezone = pytz.timezone('Europe/Moscow')

SERVICE_ACCOUNT_FILE = 'python-sheets.json'

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

gc = gspread.authorize(credentials)
spreadsheet = gc.open("test")
worksheet = spreadsheet.sheet1

def get_info_by_id(id): # Получение информации о акции через номер
    all_ids = worksheet.col_values(1)
    if len(all_ids) <= 1:
        return False
    try:
        index = all_ids.index(str(id)) + 1
    except ValueError:
        return False
    info = worksheet.row_values(index)
    response_data = {"id": info[0]} if len(info) == 1 else {
        "id": info[0],
        "fio": info[1] if len(info) > 1 else "",
        "number": info[2] if len(info) > 2 else "",
        "date": info[3] if len(info) > 3 else ""
    }
    return response_data

def add_action(number_action): # Добавление акции
    all_ids = worksheet.col_values(1)
    if str(number_action) in all_ids:
        return False
    
    next_index = len(all_ids) + 1
    return worksheet.update_acell(f'A{next_index}', number_action)

def delete_action(number_action): # Удаление акции
    all_ids = worksheet.col_values(1)
    if str(number_action) not in all_ids:
        return False
    
    index = all_ids.index(str(number_action)) + 1
    cell_list = worksheet.range(f'A{index}:F{index}')
    for cell in cell_list:
        cell.value = ''
    temp_ = worksheet.update_cells(cell_list)
    worksheet.format(f'A{index}:F{index}', {"backgroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}})
    return temp_

def unregister(number_action): # Удаление информации о владельце акции
    all_ids = worksheet.col_values(1)
    if str(number_action) not in all_ids:
        return False
    
    index = all_ids.index(str(number_action)) + 1
    cell_list = worksheet.range(f'B{index}:F{index}')
    for cell in cell_list:
        cell.value = ''
    temp_ = worksheet.update_cells(cell_list)
    worksheet.format(f'A{index}:F{index}', {"backgroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}})
    return temp_

def register_action(number_action, fio, number, tz): # Регистрация акции
    all_ids = worksheet.col_values(1)
    if str(number_action) not in all_ids:
        return False
    
    try:
        index = all_ids.index(str(number_action)) + 1
    except ValueError:
        return False
    
    msk_time = datetime.now(msk_timezone)
    formatted_msk_time = msk_time.strftime("%d.%m.%Y")
    local_time = msk_time + timedelta(hours=tz)
    formatted_local_time = local_time.strftime("%d.%m.%Y %H:%M:%S")

    cell_list = worksheet.range(f'A{index}:F{index}')
    cell_list[1].value = fio
    cell_list[2].value = number
    cell_list[3].value = formatted_msk_time
    cell_list[4].value = tz
    cell_list[5].value = formatted_local_time
    temp_ = worksheet.update_cells(cell_list)
    worksheet.format(f'A{index}:F{index}', {"backgroundColor": {"red": 0.0, "green": 1.0, "blue": 0.0}})
    return temp_
    
    
if __name__ == '__main__': # Небольшой тестовый код, дабы проверить как работает
    while True:
        d = input("Действие (add, delete, unregister, register, get): ")
        number_action = input("Введите номер акции:")
        match d:
            case "add":
                add_action(number_action)
            case "delete":
                delete_action(number_action)
            case "register":
                register_action(number_action, input("ФИО: "), input("Номер телефона: "), -1)
            case _:
                pass
