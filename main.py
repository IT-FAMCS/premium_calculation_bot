import telebot
import gspread
import httplib2
from oauth2client.service_account import ServiceAccountCredentials


TOKEN = ''

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)


spreadsheet_id = ''
sheet_name = 'Лист1'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    username = message.from_user.username
    sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
    data = sheet.get_all_records(expected_headers=['Ф. И. О.', '%, Общий', '%, Тропа (отдел)', '%, Тропа (меро)', '%, Капуста (отдел)', '%, Капуста (меро)', 'Телеграм тэги'])
    prem = []

    for row in data:
        if len(row['Телеграм тэги']) != 0:
            row['Телеграм тэги'] = row['Телеграм тэги'][1:]
        else:
            continue
        if username.lower() == row['Телеграм тэги'].lower():
            prem.append((row['Ф. И. О.'], row['%, Тропа (отдел)'], row['%, Тропа (меро)'], row['%, Капуста (отдел)'], row['%, Капуста (меро)'], row['%, Общий']))
            text = f'''Твое имя: {prem[len(prem) - 1][0]}\nТвой процент премии за отдел на тропе: {prem[len(prem) - 1][1]}\nТвой процент премии за работу на мероприятии "Тропа": {prem[len(prem) - 1][2]}\nТвой процент премии за отдел на капусте: {prem[len(prem) - 1][3]}\nТвой процент премии за работу на мероприятии "Капустник": {prem[len(prem) - 1][4]}\nВ итоге ты получаешь {prem[len(prem) - 1][5]}% премии'''
            bot.send_message(message.chat.id, text)
            break
        else:
            continue

    if len(prem) == 0:
        bot.send_message(message.chat.id, 'На данный момент у тебя нет премии. Для выяснения причины напиши Артему: @swanovich')


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
