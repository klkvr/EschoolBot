from telebot import types

start_message = "<b>Список команд:</b> \n /help - помощь \n /set_account - подключить/заменить аккаунт\n/notify_settings - настроить уведомления об оценках\n/get_marks - получить текущие оценки\n/calculate - калькулятор для прогнозирования среднего балла при получении оценок\n/get_homework - получить домашнее задание на выбранный день"
enter_login = "Пришли свой логин"
enter_password = "Пришли свой пароль"
success_login_format = "Успешная авторизация как <b>{user.real_name}</b>"
sorry_for_teachers = "Извините, но на данный момент бота могут использовать только родители и ученики"
unknown_error = "Ошибка! Попробуй ввести пароль еще раз"
log_in_first = "Сначала войди в аккаунт\n/set_account - подключить аккаунт"
error_logging_in = "Ошибка входа в аккаунт"
no_marks = "У тебя пока нет оценок"
getting_marks = "Получаю оценки..."
logging_in = "Вхожу в аккаунт..."
choose_day_to_get_homework = 'Выбери день, на который ты хочешь получить домашние задания'
no_homeworks = 'На этот день нет домашних заданий'
calculate_choose_unit = 'Выбери предмет'
calculate_choose_mark_format = 'Текущий балл по предмету <b>{unit_name}:</b> {average}\n\nВыбери оценку, чтобы узнать изменение среднего балла (используйте отрицательные оценки для проверки балла при удалении оценок)'
marks_kb = types.InlineKeyboardMarkup(row_width=5)
marks_kb.add(*[types.InlineKeyboardButton(text=mark, callback_data=f'calc_chosen_mark:{mark}') for mark in [-1, -2, -3, -4, -5, 1, 2, 3, 4, 5]])
calculate_choose_weight_format = 'Текущий балл по предмету <b>{unit_name}:</b> {average}\n\nВыбери коэффициент полученной оценки'
weights_kb = types.InlineKeyboardMarkup(row_width=5)
weights_kb.add(*[types.InlineKeyboardButton(text=weight, callback_data=f'calc_chosen_weight:{weight}') for weight in ['0.3', '0.5', '0.75',  '1.0', '1.25', '1.3', '1.35', '1.5', '1.75', '2.0', '2.5', '2.75', '3.0']])
calculate_result_format = 'При получении оценки <b>{chosen_mark}</b> с коэффициентом <b>{chosen_weight}</b> средний балл по предмету <b>{unit_name}</b> изменится с <b>{prev_average}</b> на <b>{new_average}</b>'
calculate_more = 'Добавить еще оценку'
choose_notify_type = 'О каких оценках вы хотите получать уведомления?'