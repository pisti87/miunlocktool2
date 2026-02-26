# ПЕРЕВОДЫ
import os
import locale


def get_system_language():
    try:
        lang = locale.getlocale()[0]
        if lang:
            lang_lower = lang.lower()
            if lang_lower.startswith("ru"):
                return "ru"
            elif lang_lower.startswith("id") or lang_lower.startswith("in") or "indonesian" in lang_lower:
                return "id"
            elif lang_lower.startswith("es") or "spanish" in lang_lower:
                return "es"
            elif lang_lower.startswith("zh") or "chinese" in lang_lower:
                return "zh"
    except Exception:
        pass

    env_lang = (os.environ.get("LANG", "") + os.environ.get("LANGUAGE", "")).lower()
    if "ru" in env_lang:
        return "ru"
    elif "id" in env_lang or "in" in env_lang or "indonesian" in env_lang:
        return "id"
    elif "es" in env_lang or "spanish" in env_lang:
        return "es"
    elif "zh" in env_lang or "chinese" in env_lang:
        return "zh"

    return "en"


class Translation:
    def __init__(self, language=None):
        if language is None:
            self.language = get_system_language()
        else:
            self.language = language
        self.translations = {
            'ru': self.get_russian(),
            'en': self.get_english(),
            'id': self.get_indonesian(),
            'es': self.get_spanish(),
            'zh': self.get_chinese()
        }

    def get_russian(self):
        return {
            'title': "Xiaomi Unlock Tool",
            'main_title': f"Xiaomi Unlock Tool",
            'desc': (
                f"Инструмент для автоматической отправки заявки на Unlock\n"
                f"By: Vozduhan\n"
                f"Version: {self._get_version()}"
            ),
            'desc_manual': (
                f"Ручной режим - выберите время отправки заявки вручную\n"
                f"By: Vozduhan\n"
                f"Version: {self._get_version()}"
            ),
            'params': "Параметры",
            'log_success_prefix': "УСПЕХ!",
            'log_code_message': "Код: {code} | Сообщение: {msg}",
            'log_request_parse_error': "[Ошибка обработки ответа] Не удалось распарсить JSON: {data}",
            'log_request_failed_no_response': "[Ошибка] Не удалось отправить запрос (нет ответа)",
            'log_request_exception': "[Ошибка запроса] {error}",
            'cookie_label': "New_bbs_ServiceToken:",
            'confirm': "Я подтверждаю риск возможного бана аккаунта",
            'info': "Информация",
            'status_ready': "Готов к работе",
            'ping': "Пинг: не измерен",
            'time': "Время: не синхронизировано",
            'start_btn': "Начать подачу заявки",
            'instructions_btn': "Инструкция и настройки скрипта",
            'exit_btn': "Выход",
            'log': "Лог выполнения",
            'clear_log_btn': "Очистить",
            'unlock_start': "Начало процесса разблокировки...",
            'device_id_gen': "Сгенерирован deviceId: {}",
            'ping_start': "Начинаем вычисление пинга...",
            'ping_server': "Пинг до {}: {:.2f} мс",
            'ping_failed': "Не удалось получить пинг до сервера {}",
            'ping_error': "Ошибка при пинге {}: {}",
            'open_miflash': "MiFlash Unlock",
            'ping_default': "Не удалось получить пинг ни до одного сервера!\nИспользуем значение по умолчанию: {} мс",
            'ping_avg': "Средний пинг: {:.2f} мс",
            'ntp_connect': "Попытка подключения к NTP серверу: {}",
            'ntp_time': "Пекинское время, полученное с сервера {}: {}",
            'ntp_failed': "Не удалось подключиться ни к одному из NTP серверов.",
            'time_wait': "Ожидание времени для пинга (23:59:48 по Пекину)...",
            'target_time': "Ожидание до {} (скорректировано по пингу {} мс)",
            'target_time_manual': "Ожидание до {} (ручной режим)",
            'time_reached': "Время достигнуто: {}. Начинаем отправку запроса...",
            'cookie_skipped': "Проверка cookie пропущена согласно настройкам",
            'cookie_expired': "Cookie устарел, обновите его.",
            'account_ready': "[Статус] Аккаунт может подать заявку на разблокировку.",
            'account_blocked': "[Статус] На аккаунте блокировка на подачу заявки до {} (Месяц/День).",
            'account_new': "[Статус] Аккаунт создан менее 30 дней назад.",
            'account_approved': "[Статус] Заявка одобрена, разблокировка возможна до {}.",
            'account_unknown': "[Ошибка] Неизвестный статус.",
            'status_error': "[Ошибка проверки статуса] {}",
            'request_sent': "\nОтправка запроса в {} (UTC+8)",
            'response_received': "Ответ получен в {} (UTC+8)",
            'request_failed': "[Ошибка] Не удалось отправить запрос",
            'response_error': "[Ошибка обработки ответа] {}",
            'request_error': "[Ошибка запроса] {}",
            'confirm_warning': "Пожалуйста, подтвердите, что понимаете все риски!",
            'cookie_error': "Введите значение cookie!",
            'time_error': "Не удалось синхронизировать время!",
            'settings_saved': "\nНастройки сохранены:",
            'cookie_check': "Проверка Token Cookie: {}",
            'default_ping': "Пинг по умолчанию: {} мс",
            'ping_note': "Это значение будет использовано, если не удастся измерить пинг до серверов.",
            'saved': "Настройки успешно сохранены!",
            'instructions_title': "Инструкция и настройки скрипта",
            'about_title': "О скрипте",
            'about_content': (
                f"Инструмент для автоматической отправки\n"
                f"заявки на разблокировку загрузчика\n"
                f"устройств Xiaomi на Global HyperOS\n\n"
                f"Версия скрипта: {self._get_version()}"
            ),
            'general_title': "Требования",
            'general_content': (
                "1. Mi аккаунт старше 30 дней\n \n"
                "2. Mi Community аккаунт должен быть с\n \n"
                "регионом Global\n \n"
                "3. Разблокировка устройств со всеми\n"
                "индексами кроме Китайских (CNXM)\n \n"
                "4. Устройство должно быть на HyperOS 1-3"
            ),
            'firefox_title': "FireFox | Edge",
            'firefox_content': (
                "1. Скачайте расширение Cookie Editor\n\n"
                "2. Авторизуйтесь в аккаунт, предварительно\n"
                "выйдя из него, на сайте Xiaomi Mi Community\n"
                "http://new.c.mi.com/global\n"
                "или на сайте\n"
                "http://mi.com\n\n"
                "3. В окне Cookie Editor извлеките\n"
                "new_bbs_token и скопируйте его\n\n"
                "Особенности работы:\n"
                "1. Все время в скрипте является Пекинским"
            ),
            'chrome_title': "Chrome",
            'chrome_content': (
                "1. Авторизуйтесь в аккаунте, предварительно\n"
                "выйдя из него, на сайте Mi Community\n"
                "https://new.c.mi.com/global\n"
                "или на сайте\n"
                "https://mi.com\n\n"
                "2. В строку браузера вводим команду:\n\n"
                "javascript :(function(){var token=document.cookie.match(/popRunToken=([^;]+)/);"
                "if(token){prompt(\"Copy the token:\", token[1]);}"
                "else{alert(\"Token not found\");}})()\n\n"
                "*не забудьте убрать пробел после javascript когда вставите команду в строку браузера*\n\n"
                "3. Скопируйте значение token из всплывающего окна\n\n"
                "Особенности работы:\n \n"
                "1. Все время в скрипте является Пекинским"
            ),
            'trouble_title': "Решение проблем",
            'trouble_content': """Проблема: Cookie Editor не выдает new_bbs_serviceToken

Решение:

1. Переустановите расширение Cookie Editor

2. Выйдите и зайдите в аккаунт заново

Проблема: Куки просрочен или не работает

Возможные причины:

• Регион аккаунта не Global (переключите)

• Куки действительно просрочены

Проблема: Лимит заявок исчерпан

Решение:

Проверьте статус в Mi Unlock в настройках телефона

Проблема: Ошибки 10001 и другие

Решение:

Скрипт не смог отправить заявку

Обратитесь к разработчику:

• В чат ТГК:

https://t.me/miunlocktoolrevamp""",
            'authors_title': "Авторы",
            'authors_content': """Разработчики:

• Vozduhan | Tg: @hyeplet231

Ссылки:

Telegram: https://t.me/miunlocktoolrevamp

GitHub: https://github.com/AsInsideOut/miunlocktool

Reddit: https://www.reddit.com/r/miunlocktool

Cкрипт построен на базе скрипта от:

• Vierta

Версия скрипта: """ + self._get_version(),
            'cookie_checkbox': "Отключить проверку Token Cookie перед отправкой",
            'ping_label': "Пинг по умолчанию (мс):",
            'color_theme_label': "Цветовая тема интерфейса:",
            'color_theme_xiaomi_orange': "Xiaomi Orange",
            'color_theme_red_sun': "Red Sun",
            'color_theme_blue_world': "Blue World",
            'save_btn': "Сохранить",
            'close_btn': "Закрыть",
            'ping_error_title': "Ошибка",
            'ping_error_msg': "Пинг должен быть положительным числом!",
            'cookie_error_title': "Ошибка",
            'account_blocked_title': "Информация",
            'account_new_title': "Информация",
            'account_approved_title': "Успех",
            'unknown_status_title': "Ошибка",
            'install_error': "Ошибка установки",
            'import_error': "Ошибка импорта",
            'settings': "Настройки",
            'cookie_check_state': "Отключена" if False else "Включена",
            'ban_risk': "Я подтверждаю риск возможного бана аккаунта",
            'submit_application': "Начать подачу заявки",
            'script_info': "Инструкция и настройки скрипта",
            'exit': "Выход",
            'execution_log': "Лог выполнения",
            'clear_log_btn': "Очистить",
            'unlock_process': "Начало процесса разблокировки...",
            'auto_mode': "Авто режим",
            'manual_mode': "Ручной режим",
            'manual_time_label': "Время отправки (секунды):",
            'manual_time_hint': "58.5 - 59.8 (например: 59.1)",
            'manual_mode_start': "Ручной режим: отправка в 23:59:{}",
            'manual_time_error': "Некорректное время. Используйте формат 58.5 - 59.8",
            'application_not_submitted': "[Статус] Заявка не подана, лимит превышен, попробуйте снова {} (Месяц/День).",
            'device_binding_hint': "Попробуйте привязать устройства в Настройках Раздел Статус Mi Unlock",
            'theme_label': "Тема интерфейса:",
            'theme_system': "Как в системе",
            'theme_light': "Светлая",
            'theme_dark': "Тёмная",
            'mode_label': "Режим работы:",
            'cookies_title': "Получение Cookies",
            'expand_cookies': "▶ Получение Cookies",
            'collapse_cookies': "▼ Получение Cookies",
            'check_updates': "Проверить обновления",
            'update_available': "Доступно новое обновление",
            'update_not_available': "Обновлений не найдено",
            'update_checking': "Проверка обновлений...",
            'update_error': "Ошибка при проверке обновлений",
            'current_version': "Текущая версия: {}",
            'latest_version': "Последняя версия: {}",
            'update_btn_ok': "Окей",
            'update_btn_update': "Обновить",
            'update_message': "Доступна новая версия {}! Хотите перейти на страницу загрузки?",
            'time_synchronized': "Время синхронизировано",
            'ms': "мс",
            'default': "по умолчанию",
            'welcome_title': "Xiaomi Unlock Tool",
            'welcome_text': (
                "Добро пожаловать в Xiaomi Unlock Tool!\n\n"
                "Благодаря нашей программе вы сможете разблокировать загрузчик на устройствах с HyperOS.\n\n"
                "ПЕРЕД ИСПОЛЬЗОВАНИЕМ ВНИМАТЕЛЬНО ПРОЧИТАЙТЕ ИНСТРУКЦИЮ!\n\n"
                "1. Использование данного инструмента может привести к блокировке отправки запросов на разблокировку загрузчика.\n\n"
                "2. Инструмент работает на всех глобальных прошивках (MIXM, EUXM, INXM, TRXM...)\n"
                "   и НЕ работает с китайскими (CNXM) прошивками.\n\n"
                "3. Обязательные требования:\n"
                "   • Mi аккаунт старше 30 дней\n"
                "   • Регин в Mi Community стоит Global\n"
                "   • Устройство на HyperOS 1-3\n\n"
                "4. Вся ответственность на вас и разработчики НЕ несут ответственность за ваше устройство.\n\n"
                "Нажмите 'Продолжить', чтобы начать работу."
            ),
            'welcome_btn': "Продолжить",
            'ping_hint': "Это значение будет использовано, если не удастся измерить пинг до серверов.",
            'color_theme_xiaomi': "Xiaomi Orange",
            'color_theme_blue': "Blue Word",
            'color_theme_red': "Red Sun",
            'language_label': "Язык",
            'log_to_txt_checkbox': "Логирование в TXT файле",
            'spam_mode_checkbox': "Спам-отправка (в Авто-режиме)",
            'spam_mode_desc': "Отправляет запросы в 23:59 на 58.6, 58.8, 59.1, 59.3, 59.5 секундах.\nЕсли отключено, отправляется один запрос в оптимальное время.",
            'ping_not_measured_manual': "Пинг: не измеряется (ручной режим)",
            'log_auto_mode_spam_selected': "Выбран автоматический режим (Спам-отправка)",
            'log_auto_mode_single_selected': "Выбран автоматический режим (Обычная отправка)",
            'log_manual_mode_selected': "Выбран ручной режим",
            'log_time_gt_2355': "Время > 23:58. Выполняем синхронизацию времени перед стартом...",
            'log_time_sync_success': "Время успешно синхронизировано!",
            'log_presync_wait': "Ожидание предварительной синхронизации в 23:58:00 (Пекин)...",
            'status_presync_wait': "Ожидание 23:58 для синхронизации...",
            'log_presync_start': "Наступило 23:58! Выполняем точную синхронизацию времени...",
            'log_time_updated': "Время обновлено: {}",
            'log_resync_error': "Ошибка повторной синхронизации, продолжаем с текущим таймером.",
            'log_normal_mode_ping': "Обычный режим: вычисляем пинг...",
            'log_calculated_send_time': "Расчетное время отправки: 23:59:{}",
            'log_spam_mode_targets': "РЕЖИМ СПАМА: Целевые времена: {}",
            'status_spam_wait': "Ожидание спам-атаки...",
            'log_spam_sending_at': "[Спам #{}] Отправка запроса в 23:59:{}s",
            'log_spam_new_device_id': "[Спам #{}] Новый deviceId: {}",
            'log_spam_response_prefix': "[Спам #{}] Время: {}s",
            'log_spam_success_prefix': "УСПЕХ!",
            'log_spam_response_format': "{} | Код: {} | {}",
            'log_spam_parse_error': "[Спам #{}] Ошибка парсинга ответа: {}",
            'log_spam_no_response': "[Спам #{}] Нет ответа от сервера",
            'log_spam_send_error': "[Спам #{}] Ошибка отправки: {}",
        }

    def get_english(self):
        return {
            'title': "Xiaomi Unlock Tool",
            'main_title': f"Xiaomi Unlock Tool",
            'desc': (
                f"Tool for automatic unlock request submission\n"
                f"By: Vozduhan\n"
                f"Version: {self._get_version()}"
            ),
            'desc_manual': (
                f"Manual mode - select the time to submit manually\n"
                f"By: Vozduhan\n"
                f"Version: {self._get_version()}"
            ),
            'params': "Parameters",
            'log_success_prefix': "SUCCESS!",
            'log_code_message': "Code: {code} | Message: {msg}",
            'log_request_parse_error': "[Response processing error] Failed to parse JSON: {data}",
            'log_request_failed_no_response': "[Error] Failed to send request (no response)",
            'log_request_exception': "[Request error] {error}",
            'cookie_label': "New_bbs_ServiceToken:",
            'confirm': "I acknowledge the risk of possible account ban",
            'info': "Information",
            'status_ready': "Ready to start",
            'ping': "Ping: not measured",
            'time': "Time: not synchronized",
            'start_btn': "Start Application",
            'instructions_btn': "Instructions and Script Settings",
            'exit_btn': "Exit",
            'log': "Execution Log",
            'clear_log_btn': "Clear",
            'unlock_start': "Starting unlock process...",
            'device_id_gen': "Generated deviceId: {}",
            'ping_start': "Starting ping calculation...",
            'ping_server': "Ping to {}: {:.2f} ms",
            'ping_failed': "Failed to get server ping {}",
            'ping_error': "Error pinging {}: {}",
            'ping_default': "Failed to get server ping!\nUsing default value: {} ms",
            'open_miflash': "MiFlash Unlock",
            'ping_avg': "Average ping: {:.2f} ms",
            'ntp_connect': "Attempting to connect to NTP server: {}",
            'ntp_time': "Beijing time received from server {}: {}",
            'ntp_failed': "Failed to connect to any NTP servers.",
            'time_wait': "Waiting for ping time (23:59:48 Beijing time)...",
            'target_time': "Waiting until {} (adjusted for ping {} ms)",
            'target_time_manual': "Waiting until {} (manual mode)",
            'time_reached': "Time reached: {}. Starting request submission...",
            'cookie_skipped': "Cookie check skipped according to settings",
            'cookie_expired': "Cookie expired, please update (see settings, Troubleshooting)",
            'account_ready': "[Status] Account can submit unlock request.",
            'account_blocked': "[Status] Account has submission ban until {} (Month/Day).",
            'account_new': "[Status] Account created less than 30 days ago.",
            'account_approved': "[Status] Application approved, unlock possible until {}.",
            'account_unknown': "[Error] Unknown status.",
            'status_error': "[Status check error] {}",
            'request_sent': "\nSending request at {} (UTC+8)",
            'response_received': "Response received at {} (UTC+8)",
            'request_failed': "[Error] Failed to send request",
            'response_error': "[Response processing error] {}",
            'request_error': "[Request error] {}",
            'confirm_warning': "Please confirm that you understand all risks!",
            'cookie_error': "Enter cookie value!",
            'time_error': "Failed to synchronize time!",
            'settings_saved': "\nSettings saved:",
            'cookie_check': "Token Cookie check: {}",
            'default_ping': "Default ping: {} ms",
            'ping_note': "This value will be used if measuring ping to servers fails.",
            'saved': "Settings saved successfully!",
            'instructions_title': "Settings and instructions",
            'about_title': "About",
            'about_content': (
                f"Tool for automatic request send\n"
                f"for bootloader unlocking on\n"
                f"Xiaomi devices that runs HyperOS\n\n"
                f"Script version: {self._get_version()}"
            ),
            'general_title': "Requirements",
            'general_content': (
                "1. Mi account must be older than 30 days\n \n"
                "2. Mi Community account must have\n \n"
                "Global region set\n \n"
                "3. Unlocking available for all devices\n"
                "except Chinese ROM (CNXM)\n \n"
                "4. Device is running HyperOS"
            ),
            'firefox_title': "FireFox | Edge",
            'firefox_content': (
                "1. Download Cookie Editor extension\n\n"
                "2. Log in to your account (after logging out)\n"
                "on Xiaomi Mi Community site:\n\n"
                "http://new.c.mi.com/global\n"
                "or \n"
                "http://mi.com\n\n"
                "3. In Cookie Editor window extract\n"
                "new_bbs_token and copy it\n\n"
                "Important notes:\n \n"
                "1. All times in script are Beijing time"
            ),
            'chrome_title': "Chrome",
            'chrome_content': (
                "1. Log in to your account (after logging out)\n"
                "on Xiaomi Mi Community site:\n"
                "https://new.c.mi.com/global\n"
                "or \n"
                "https://mi.com\n\n"
                "2. In browser address bar enter command:\n\n"
                "javascript :(function(){var token=document.cookie.match(/popRunToken=([^;]+)/);"
                "if(token){prompt(\"Copy the token:\", token[1]);}"
                "else{alert(\"Token not found\");}})()\n\n"
                "*remember to remove the space after javascript when pasting the command into the browser address bar*\n\n"
                "3. Copy the token value from the popup window\n\n"
                "Important notes:\n \n"
                "1. All times in script are Beijing time"
            ),
            'trouble_title': "Troubleshooting",
            'trouble_content': """Issue: CookieEditor doesn't show new_bbs_serviceToken

Solution:

1. Refresh page

2. Log out and sign in again

Issue: Cookie expired or not working

Possible reasons:

• Account region is not Global (switch it)

• Cookie is actually expired

Issue: Request limit reached

Solution:

Check status in Mi Unlock in phone settings

Issue: Errors 10001 and others

Solution:

Script failed to submit request

Contact developers:

• Via Telegram group:

https://t.me/miunlocktoolrevamp""",
            'authors_title': "Authors",
            'authors_content': """Developers:

• Vozduhan | Tg: @hyeplet231

Links:

Telegram group: https://t.me/miunlocktoolrevamp

GitHub: https://github.com/AsInsideOut/miunlocktool

Reddit: https://www.reddit.com/r/miunlocktool

Script is based on:

• Vierta

Script version: """ + self._get_version(),
            'cookie_checkbox': "Disable Token Cookie check before submission",
            'ping_label': "Default ping (ms):",
            'color_theme_label': "Color theme:",
            'color_theme_xiaomi_orange': "Xiaomi Orange",
            'color_theme_red_sun': "Red Sun",
            'color_theme_blue_world': "Blue World",
            'save_btn': "Save",
            'close_btn': "Close",
            'ping_error_title': "Error",
            'ping_error_msg': "Ping must be a positive number.",
            'cookie_error_title': "Error",
            'account_blocked_title': "Information",
            'account_new_title': "Information",
            'account_approved_title': "Success",
            'unknown_status_title': "Error",
            'install_error': "Installation Error",
            'import_error': "Import Error",
            'settings': "Settings",
            'cookie_check_state': "Disabled" if False else "Enabled",
            'ban_risk': "I acknowledge the risk of possible account ban",
            'submit_application': "Start Application",
            'script_info': "Instructions and Script Settings",
            'exit': "Exit",
            'execution_log': "Execution Log",
            'clear_log_btn': "Clear",
            'unlock_process': "Starting unlock process...",
            'auto_mode': "Auto Mode",
            'manual_mode': "Manual Mode",
            'manual_time_label': "Submission time (seconds):",
            'manual_time_hint': "58.5 - 59.8 (e.g.: 59.1)",
            'manual_mode_start': "Manual mode: sending at 23:59:{}",
            'manual_time_error': "Invalid time. Use format 58.5 - 59.8",
            'application_not_submitted': "[Status] Application not submitted, limit exceeded, try again on {} (Month/Day).",
            'device_binding_hint': "Try to bind devices in Settings, Mi Unlock Status section",
            'theme_label': "Interface theme:",
            'theme_system': "System",
            'theme_light': "Light",
            'theme_dark': "Dark",
            'mode_label': "Operation mode:",
            'cookies_title': "Getting Cookies",
            'expand_cookies': "▶ Getting Cookies",
            'collapse_cookies': "▼ Getting Cookies",
            'check_updates': "Check for Updates",
            'update_available': "Update is available",
            'update_not_available': "No updates found",
            'update_checking': "Checking for updates...",
            'update_error': "Error checking for updates",
            'current_version': "Current version: {}",
            'latest_version': "Latest version: {}",
            'update_btn_ok': "Alright",
            'update_btn_update': "Update",
            'update_message': "New version {} is available! Would you like to go to the download page?",
            'time_synchronized': "Time synchronized",
            'ms': "ms",
            'default': "default",
            'welcome_title': "Xiaomi Unlock Tool",
            'welcome_text': (
                "Welcome to Xiaomi Unlock Tool!\n\n"
                "IMPORTANT WARNING:\n\n"
                "BEFORE USING, CAREFULLY READ THE INSTRUCTIONS!\n\n"
                "1. Using this tool may lead to submission ban.\n\n"
                "2. The tool is ONLY for devices on Global HyperOS\n"
                "   and does NOT work with Chinese (CN) models.\n\n"
                "3. Requirements:\n"
                "   • Mi account older than 30 days\n"
                "   • Mi Community account with Global region\n\n"
                "4. By using this tool, you agree that developers dont take responsibility for your devices.\n\n"
                "Click 'Continue' to start."
            ),
            'welcome_btn': "Continue",
            'color_theme_xiaomi': "Xiaomi Orange",
            'color_theme_blue': "Blue Word",
            'color_theme_red': "Red Sun",
            'language_label': "Language",
            'log_to_txt_checkbox': "Log to TXT file",
            'spam_mode_checkbox': "Spam Sending (in Auto-Mode)",
            'spam_mode_desc': "Sends requests at 23:59:58.6, 58.8, 59.1, 59.3, 59.5.\nIf disabled, sends a single request at the optimal time.",
            'ping_not_measured_manual': "Ping: not measured (manual mode)",
            'log_auto_mode_spam_selected': "Auto mode selected (Spam)",
            'log_auto_mode_single_selected': "Auto mode selected (Single request)",
            'log_manual_mode_selected': "Manual mode selected",
            'log_time_gt_2355': "Time > 23:58. Synchronizing time before start...",
            'log_time_sync_success': "Time synchronized successfully!",
            'log_presync_wait': "Waiting for pre-synchronization at 23:58:00 (Beijing)...",
            'status_presync_wait': "Waiting for 23:58 to synchronize...",
            'log_presync_start': "It's 23:58! Performing precise time synchronization...",
            'log_time_updated': "Time updated: {}",
            'log_resync_error': "Re-synchronization error, continuing with the current timer.",
            'log_normal_mode_ping': "Normal mode: calculating ping...",
            'log_calculated_send_time': "Calculated send time: 23:59:{}",
            'log_spam_mode_targets': "SPAM MODE: Target times: {}",
            'status_spam_wait': "Waiting for spam attack...",
            'log_spam_sending_at': "[Spam #{}] Sending request at 23:59:{}s",
            'log_spam_new_device_id': "[Spam #{}] New deviceId: {}",
            'log_spam_response_prefix': "[Spam #{}] Time: {}s",
            'log_spam_success_prefix': "SUCCESS!",
            'log_spam_response_format': "{} | Code: {} | {}",
            'log_spam_parse_error': "[Spam #{}] Error parsing response: {}",
            'log_spam_no_response': "[Spam #{}] No response from server",
            'log_spam_send_error': "[Spam #{}] Error sending request: {}",
        }

    def get_indonesian(self):
        return {
            'title': "Xiaomi Unlock Tool",
            'main_title': f"Xiaomi Unlock Tool",
            'desc': (
                f"Alat untuk pengajuan permintaan buka kunci otomatis\n"
                f"Oleh: Vozduhan\n"
                f"Versi: {self._get_version()}"
            ),
            'desc_manual': (
                f"Mode manual - pilih waktu pengiriman secara manual\n"
                f"Oleh: Vozduhan\n"
                f"Versi: {self._get_version()}"
            ),
            'params': "Parameter",
            'log_success_prefix': "SUKSES!",
            'log_code_message': "Kode: {code} | Pesan: {msg}",
            'log_request_parse_error': "[Kesalahan pemrosesan respons] Gagal mengurai JSON: {data}",
            'log_request_failed_no_response': "[Kesalahan] Gagal mengirim permintaan (tidak ada respons)",
            'log_request_exception': "[Kesalahan permintaan] {error}",
            'cookie_label': "New_bbs_ServiceToken:",
            'confirm': "Saya menyadari risiko kemungkinan pemblokiran akun",
            'info': "Informasi",
            'status_ready': "Siap memulai",
            'ping': "Ping: tidak diukur",
            'time': "Waktu: tidak disinkronkan",
            'start_btn': "Mulai Aplikasi",
            'instructions_btn': "Instruksi dan Pengaturan Skrip",
            'exit_btn': "Keluar",
            'log': "Log Eksekusi",
            'clear_log_btn': "Bersihkan",
            'unlock_start': "Memulai proses buka kunci...",
            'device_id_gen': "DeviceId yang dihasilkan: {}",
            'ping_start': "Memulai perhitungan ping...",
            'ping_server': "Ping ke {}: {:.2f} ms",
            'ping_failed': "Gagal mendapatkan ping server {}",
            'ping_error': "Kesalahan ping {}: {}",
            'open_miflash': "MiFlash Unlock",
            'ping_default': "Gagal mendapatkan ping server!\nMenggunakan nilai default: {} ms",
            'ping_avg': "Rata-rata ping: {:.2f} ms",
            'ntp_connect': "Mencoba terhubung ke server NTP: {}",
            'ntp_time': "Waktu Beijing diterima dari server {}: {}",
            'ntp_failed': "Gagal terhubung ke server NTP mana pun.",
            'time_wait': "Menunggu waktu ping (23:59:48 waktu Beijing)...",
            'target_time': "Menunggu hingga {} (disesuaikan dengan ping {} ms)",
            'target_time_manual': "Menunggu hingga {} (mode manual)",
            'time_reached': "Waktu tercapai: {}. Memulai pengiriman permintaan...",
            'cookie_skipped': "Pemeriksaan cookie dilewati sesuai pengaturan",
            'cookie_expired': "Cookie kedaluwarsa, harap perbarui",
            'account_ready': "[Status] Akun dapat mengirim permintaan buka kunci.",
            'account_blocked': "[Status] Akun diblokir hingga {} (Bulan/Hari).",
            'account_new': "[Status] Akun dibuat kurang dari 30 hari yang lalu.",
            'account_approved': "[Status] Aplikasi disetujui, buka kunci hingga {}.",
            'account_unknown': "[Kesalahan] Status tidak dikenal.",
            'status_error': "[Kesalahan pemeriksaan status] {}",
            'request_sent': "\nMengirim permintaan pada {} (UTC+8)",
            'response_received': "Respons diterima pada {} (UTC+8)",
            'request_failed': "[Kesalahan] Gagal mengirim permintaan",
            'response_error': "[Kesalahan pemrosesan respons] {}",
            'request_error': "[Kesalahan permintaan] {}",
            'confirm_warning': "Harap konfirmasi bahwa Anda memahami semua risiko!",
            'cookie_error': "Masukkan nilai cookie!",
            'time_error': "Gagal menyinkronkan waktu!",
            'settings_saved': "\nPengaturan disimpan:",
            'cookie_check': "Pemeriksaan Token Cookie: {}",
            'default_ping': "Ping default: {} ms",
            'ping_note': "Nilai ini akan digunakan jika pengukuran ping ke server gagal.",
            'saved': "Pengaturan berhasil disimpan!",
            'instructions_title': "Instruksi dan Pengaturan Skrip",
            'about_title': "Tentang",
            'about_content': (
                f"Alat untuk pengiriman permintaan otomatis\n"
                f"untuk membuka kunci bootloader pada\n"
                f"perangkat Xiaomi yang menjalankan HyperOS\n\n"
                f"Versi skrip: {self._get_version()}"
            ),
            'general_title': "Persyaratan",
            'general_content': (
                "1. Akun Mi harus lebih dari 30 hari\n \n"
                "2. Akun Mi Community harus memiliki\n \n"
                "region Global\n \n"
                "3. Buka kunci tersedia untuk semua perangkat\n"
                "kecuali ROM China (CNXM)\n \n"
                "4. Perangkat menjalankan HyperOS"
            ),
            'firefox_title': "FireFox | Edge",
            'firefox_content': (
                "1. Unduh ekstensi Cookie Editor\n\n"
                "2. Masuk ke akun Anda (setelah keluar)\n"
                "di situs Xiaomi Mi Community:\n\n"
                "http://new.c.mi.com/global\n"
                "atau \n"
                "http://mi.com\n\n"
                "3. Di jendela Cookie Editor, ekstrak\n"
                "new_bbs_token dan salin\n\n"
                "Catatan penting:\n \n"
                "1. Semua waktu dalam skrip adalah waktu Beijing"
            ),
            'chrome_title': "Chrome",
            'chrome_content': (
                "1. Masuk ke akun Anda (setelah keluar)\n"
                "di situs Xiaomi Mi Community:\n"
                "https://new.c.mi.com/global\n"
                "atau \n"
                "https://mi.com\n\n"
                "2. Di bilah alamat browser, masukkan perintah:\n\n"
                "javascript :(function(){var token=document.cookie.match(/popRunToken=([^;]+)/);"
                "if(token){prompt(\"Salin token:\", token[1]);}"
                "else{alert(\"Token tidak ditemukan\");}})()\n\n"
                "*ingat untuk menghapus spasi setelah javascript saat menempelkan perintah ke bilah alamat browser*\n\n"
                "3. Salin nilai token dari jendela popup\n\n"
                "Catatan penting:\n \n"
                "1. Semua waktu dalam skrip adalah waktu Beijing"
            ),
            'trouble_title': "Pemecahan Masalah",
            'trouble_content': """Masalah: CookieEditor tidak menampilkan new_bbs_serviceToken

Solusi:

1. Segarkan halaman

2. Keluar dari akun Anda dan masuk kembali.

Masalah: Cookie kedaluwarsa atau tidak berfungsi

Kemungkinan penyebab:

• Region akun bukan Global (ganti)

• Cookie benar-benar kedaluwarsa

Masalah: Batas permintaan tercapai

Solusi:

Periksa status di Mi Unlock di pengaturan ponsel

Masalah: Kesalahan 10001 dan lainnya

Solusi:

Skrip gagal mengirim permintaan

Hubungi pengembang:

• Melalui grup Telegram:

https://t.me/miunlocktoolrevamp""",
            'authors_title': "Pengembang",
            'authors_content': """Pengembang:

• Space | Tg: @hyeplet231

Tautan:

Grup Telegram: https://t.me/miunlocktoolrevamp

GitHub: https://github.com/AsInsideOut/miunlocktool

Reddit: https://www.reddit.com/r/miunlocktool

Skrip ini didasarkan pada:

• Vierta

Versi skrip: """ + self._get_version(),
            'cookie_checkbox': "Nonaktifkan pemeriksaan Token Cookie sebelum pengiriman",
            'ping_label': "Ping default (ms):",
            'color_theme_label': "Tema warna:",
            'color_theme_xiaomi_orange': "Xiaomi Orange",
            'color_theme_red_sun': "Red Sun",
            'color_theme_blue_world': "Blue World",
            'save_btn': "Simpan",
            'close_btn': "Tutup",
            'ping_error_title': "Kesalahan",
            'ping_error_msg': "Ping harus berupa angka positif.",
            'cookie_error_title': "Kesalahan",
            'account_blocked_title': "Informasi",
            'account_new_title': "Informasi",
            'account_approved_title': "Sukses",
            'unknown_status_title': "Kesalahan",
            'install_error': "Kesalahan Instalasi",
            'import_error': "Kesalahan Impor",
            'settings': "Pengaturan",
            'cookie_check_state': "Dinonaktifkan" if False else "Diaktifkan",
            'ban_risk': "Saya menyadari risiko kemungkinan pemblokiran akun",
            'submit_application': "Mulai Aplikasi",
            'script_info': "Instruksi dan Pengaturan Skrip",
            'exit': "Keluar",
            'execution_log': "Log Eksekusi",
            'clear_log_btn': "Bersihkan",
            'unlock_process': "Memulai proses buka kunci...",
            'auto_mode': "Mode Otomatis",
            'manual_mode': "Mode Manual",
            'manual_time_label': "Waktu pengiriman (detik):",
            'manual_time_hint': "58.5 - 59.8 (contoh: 59.1)",
            'manual_mode_start': "Mode manual: mengirim pada 23:59:{}",
            'manual_time_error': "Waktu tidak valid. Gunakan format 58.5 - 59.8",
            'application_not_submitted': "[Status] Aplikasi tidak terkirim, batas terlampaui, coba lagi pada {} (Bulan/Hari).",
            'device_binding_hint': "Coba ikat perangkat di Pengaturan, Bagian Status Mi Unlock",
            'theme_label': "Tema antarmuka:",
            'theme_system': "Sistem",
            'theme_light': "Terang",
            'theme_dark': "Gelap",
            'mode_label': "Mode operasi:",
            'cookies_title': "Mendapatkan Cookies",
            'expand_cookies': "▶ Mendapatkan Cookies",
            'collapse_cookies': "▼ Mendapatkan Cookies",
            'check_updates': "Periksa Pembaruan",
            'update_available': "Pembaruan tersedia",
            'update_not_available': "Tidak ada pembaruan",
            'update_checking': "Memeriksa pembaruan...",
            'update_error': "Kesalahan saat memeriksa pembaruan",
            'current_version': "Versi saat ini: {}",
            'latest_version': "Versi terbaru: {}",
            'update_btn_ok': "Baik",
            'update_btn_update': "Perbarui",
            'update_message': "Versi baru {} tersedia! Apakah Anda ingin membuka halaman unduhan?",
            'time_synchronized': "Waktu disinkronkan",
            'ms': "ms",
            'default': "default",
            'welcome_title': "Xiaomi Unlock Tool",
            'welcome_text': (
                "Selamat datang di Xiaomi Unlock Tool!\n\n"
                "PERINGATAN PENTING:\n\n"
                "SEBELUM MENGGUNAKAN, BACA INSTRUKSI DENGAN SEKSAMA!\n\n"
                "1. Menggunakan alat ini dapat menyebabkan pemblokiran pengiriman.\n\n"
                "2. Alat ini HANYA untuk perangkat dengan HyperOS Global\n"
                "   dan TIDAK bekerja dengan model China.\n\n"
                "3. Persyaratan:\n"
                "   • Akun Mi lebih dari 30 hari\n"
                "   • Akun Mi Community dengan region Global\n\n"
                "4. Dengan menggunakan alat ini, Anda setuju bahwa pengembang tidak bertanggung jawab atas perangkat Anda.\n\n"
                "Klik 'Lanjutkan' untuk memulai."
            ),
            'welcome_btn': "Lanjutkan",
            'color_theme_xiaomi': "Xiaomi Orange",
            'color_theme_blue': "Blue Word",
            'color_theme_red': "Red Sun",
            'language_label': "Bahasa",
            'log_to_txt_checkbox': "Log ke file TXT",
            'spam_mode_checkbox': "Pengiriman Spam (dalam Mode Otomatis)",
            'spam_mode_desc': "Mengirim permintaan pada 23:59:58.6, 58.8, 59.1, 59.3, 59.5.\nJika dinonaktifkan, mengirim satu permintaan pada waktu optimal.",
            'ping_not_measured_manual': "Ping: tidak diukur (mode manual)",
            'log_auto_mode_spam_selected': "Mode otomatis dipilih (Spam)",
            'log_auto_mode_single_selected': "Mode otomatis dipilih (Permintaan tunggal)",
            'log_manual_mode_selected': "Mode manual dipilih",
            'log_time_gt_2355': "Waktu > 23:58. Menyinkronkan waktu sebelum memulai...",
            'log_time_sync_success': "Waktu berhasil disinkronkan!",
            'log_presync_wait': "Menunggu pra-sinkronisasi pada 23:58:00 (Beijing)...",
            'status_presync_wait': "Menunggu 23:58 untuk sinkronisasi...",
            'log_presync_start': "Sekarang 23:58! Melakukan sinkronisasi waktu presisi...",
            'log_time_updated': "Waktu diperbarui: {}",
            'log_resync_error': "Kesalahan sinkronisasi ulang, melanjutkan dengan pengatur waktu saat ini.",
            'log_normal_mode_ping': "Mode normal: menghitung ping...",
            'log_calculated_send_time': "Perkiraan waktu pengiriman: 23:59:{}",
            'log_spam_mode_targets': "MODE SPAM: Waktu target: {}",
            'status_spam_wait': "Menunggu serangan spam...",
            'log_spam_sending_at': "[Spam #{}] Mengirim permintaan pada 23:59:{}s",
            'log_spam_new_device_id': "[Spam #{}] DeviceId baru: {}",
            'log_spam_response_prefix': "[Spam #{}] Waktu: {}s",
            'log_spam_success_prefix': "SUKSES!",
            'log_spam_response_format': "{} | Kode: {} | {}",
            'log_spam_parse_error': "[Spam #{}] Kesalahan mengurai respons: {}",
            'log_spam_no_response': "[Spam #{}] Tidak ada respons dari server",
            'log_spam_send_error': "[Spam #{}] Kesalahan mengirim permintaan: {}",
        }

    def get_spanish(self):
        return {
            'title': "Xiaomi Unlock Tool",
            'main_title': f"Xiaomi Unlock Tool",
            'desc': (
                f"Herramienta para el envío automático de solicitudes de desbloqueo\n"
                f"Por: Vozduhan\n"
                f"Versión: {self._get_version()}"
            ),
            'desc_manual': (
                f"Modo manual - seleccione la hora de envío manualmente\n"
                f"Por: Vozduhan\n"
                f"Versión: {self._get_version()}"
            ),
            'params': "Parámetros",
            'log_success_prefix': "¡ÉXITO!",
            'log_code_message': "Código: {code} | Mensaje: {msg}",
            'log_request_parse_error': "[Error al procesar respuesta] No se pudo analizar JSON: {data}",
            'log_request_failed_no_response': "[Error] No se pudo enviar la solicitud (sin respuesta)",
            'log_request_exception': "[Error de solicitud] {error}",
            'cookie_label': "New_bbs_ServiceToken:",
            'confirm': "Reconozco el riesgo de posible bloqueo de cuenta",
            'info': "Información",
            'status_ready': "Listo para comenzar",
            'ping': "Ping: no medido",
            'time': "Hora: no sincronizada",
            'start_btn': "Iniciar Solicitud",
            'instructions_btn': "Instrucciones y Configuración",
            'exit_btn': "Salir",
            'log': "Registro de Ejecución",
            'clear_log_btn': "Limpiar",
            'unlock_start': "Iniciando proceso de desbloqueo...",
            'device_id_gen': "DeviceId generado: {}",
            'ping_start': "Calculando ping...",
            'ping_server': "Ping a {}: {:.2f} ms",
            'ping_failed': "No se pudo obtener ping del servidor {}",
            'ping_error': "Error al hacer ping a {}: {}",
            'open_miflash': "MiFlash Unlock",
            'ping_default': "¡No se pudo obtener ping de ningún servidor!\nUsando valor predeterminado: {} ms",
            'ping_avg': "Ping promedio: {:.2f} ms",
            'ntp_connect': "Intentando conectar al servidor NTP: {}",
            'ntp_time': "Hora de Pekín recibida del servidor {}: {}",
            'ntp_failed': "No se pudo conectar a ningún servidor NTP.",
            'time_wait': "Esperando hora para ping (23:59:48 hora de Pekín)...",
            'target_time': "Esperando hasta {} (ajustado por ping {} ms)",
            'target_time_manual': "Esperando hasta {} (modo manual)",
            'time_reached': "Hora alcanzada: {}. Iniciando envío de solicitud...",
            'cookie_skipped': "Verificación de cookie omitida según configuración",
            'cookie_expired': "Cookie caducada, por favor actualícela",
            'account_ready': "[Estado] La cuenta puede enviar solicitud de desbloqueo.",
            'account_blocked': "[Estado] La cuenta tiene bloqueo de envío hasta {} (Mes/Día).",
            'account_new': "[Estado] La cuenta fue creada hace menos de 30 días.",
            'account_approved': "[Estado] Solicitud aprobada, desbloqueo posible hasta {}.",
            'account_unknown': "[Error] Estado desconocido.",
            'status_error': "[Error al verificar estado] {}",
            'request_sent': "\nEnviando solicitud a las {} (UTC+8)",
            'response_received': "Respuesta recibida a las {} (UTC+8)",
            'request_failed': "[Error] No se pudo enviar la solicitud",
            'response_error': "[Error al procesar respuesta] {}",
            'request_error': "[Error de solicitud] {}",
            'confirm_warning': "¡Por favor confirme que comprende todos los riesgos!",
            'cookie_error': "¡Ingrese el valor de la cookie!",
            'time_error': "¡No se pudo sincronizar la hora!",
            'settings_saved': "\nConfiguración guardada:",
            'cookie_check': "Verificación de Token Cookie: {}",
            'default_ping': "Ping predeterminado: {} ms",
            'ping_note': "Este valor se usará si falla la medición de ping a los servidores.",
            'saved': "¡Configuración guardada exitosamente!",
            'instructions_title': "Instrucciones y Configuración",
            'about_title': "Acerca de",
            'about_content': (
                f"Herramienta para envío automático de solicitudes\n"
                f"de desbloqueo de gestor de arranque en\n"
                f"dispositivos Xiaomi con HyperOS\n\n"
                f"Versión del script: {self._get_version()}"
            ),
            'general_title': "Requisitos",
            'general_content': (
                "1. La cuenta Mi debe tener más de 30 días\n \n"
                "2. La cuenta de Mi Community debe tener\n \n"
                "región Global configurada\n \n"
                "3. Desbloqueo disponible para todos los dispositivos\n"
                "excepto ROM China (CNXM)\n \n"
                "4. El dispositivo debe tener HyperOS"
            ),
            'firefox_title': "FireFox | Edge",
            'firefox_content': (
                "1. Descargue la extensión Cookie Editor\n\n"
                "2. Inicie sesión en su cuenta (después de cerrar sesión)\n"
                "en el sitio de Xiaomi Mi Community:\n\n"
                "http://new.c.mi.com/global\n"
                "o \n"
                "http://mi.com\n\n"
                "3. En la ventana de Cookie Editor, extraiga\n"
                "new_bbs_token y cópielo\n\n"
                "Notas importantes:\n \n"
                "1. Todas las horas en el script son hora de Pekín"
            ),
            'chrome_title': "Chrome",
            'chrome_content': (
                "1. Inicie sesión en su cuenta (después de cerrar sesión)\n"
                "en el sitio de Xiaomi Mi Community:\n"
                "https://new.c.mi.com/global\n"
                "o \n"
                "https://mi.com\n\n"
                "2. En la barra de direcciones del navegador, ingrese el comando:\n\n"
                "javascript :(function(){var token=document.cookie.match(/popRunToken=([^;]+)/);"
                "if(token){prompt(\"Copiar token:\", token[1]);}"
                "else{alert(\"Token no encontrado\");}})()\n\n"
                "*recuerde quitar el espacio después de javascript al pegar el comando en la barra de direcciones del navegador*\n\n"
                "3. Copie el valor del token de la ventana emergente\n\n"
                "Notas importantes:\n \n"
                "1. Todas las horas en el script son hora de Pekín"
            ),
            'trouble_title': "Solución de Problemas",
            'trouble_content': """Problema: CookieEditor no muestra new_bbs_serviceToken

Solución:

1. Actualice la página

2. Cierre sesión y vuelva a iniciarla

Problema: Cookie caducada o no funciona

Posibles causas:

• La región de la cuenta no es Global (cámbiela)

• La cookie realmente ha caducado

Problema: Límite de solicitudes alcanzado

Solución:

Verifique el estado en Mi Unlock en la configuración del teléfono

Problema: Errores 10001 y otros

Solución:

El script no pudo enviar la solicitud

Contacte a los desarrolladores:

• A través del grupo de Telegram:

https://t.me/miunlocktoolrevamp""",
            'authors_title': "Autores",
            'authors_content': """Desarrolladores:

• Vozduhan | Tg: @hyeplet231

Enlaces:

Grupo de Telegram: https://t.me/miunlocktoolrevamp

GitHub: https://github.com/AsInsideOut/miunlocktool

Reddit: https://www.reddit.com/r/miunlocktool

El script está basado en:

• Vierta

Versión del script: """ + self._get_version(),
            'cookie_checkbox': "Desactivar verificación de Token Cookie antes del envío",
            'ping_label': "Ping predeterminado (ms):",
            'color_theme_label': "Tema de color:",
            'color_theme_xiaomi_orange': "Xiaomi Orange",
            'color_theme_red_sun': "Red Sun",
            'color_theme_blue_world': "Blue World",
            'save_btn': "Guardar",
            'close_btn': "Cerrar",
            'ping_error_title': "Error",
            'ping_error_msg': "¡El ping debe ser un número positivo!",
            'cookie_error_title': "Error",
            'account_blocked_title': "Información",
            'account_new_title': "Información",
            'account_approved_title': "Éxito",
            'unknown_status_title': "Error",
            'install_error': "Error de Instalación",
            'import_error': "Error de Importación",
            'settings': "Configuración",
            'cookie_check_state': "Desactivada" if False else "Activada",
            'ban_risk': "Reconozco el riesgo de posible bloqueo de cuenta",
            'submit_application': "Iniciar Solicitud",
            'script_info': "Instrucciones y Configuración",
            'exit': "Salir",
            'execution_log': "Registro de Ejecución",
            'clear_log_btn': "Limpiar",
            'unlock_process': "Iniciando proceso de desbloqueo...",
            'auto_mode': "Modo Automático",
            'manual_mode': "Modo Manual",
            'manual_time_label': "Hora de envío (segundos):",
            'manual_time_hint': "58.5 - 59.8 (ejemplo: 59.1)",
            'manual_mode_start': "Modo manual: enviando a las 23:59:{}",
            'manual_time_error': "Hora inválida. Use formato 58.5 - 59.8",
            'application_not_submitted': "[Estado] Solicitud no enviada, límite excedido, intente de nuevo el {} (Mes/Día).",
            'device_binding_hint': "Intente vincular dispositivos en Configuración, Sección Estado Mi Unlock",
            'theme_label': "Tema de interfaz:",
            'theme_system': "Sistema",
            'theme_light': "Claro",
            'theme_dark': "Oscuro",
            'mode_label': "Modo de operación:",
            'cookies_title': "Obtener Cookies",
            'expand_cookies': "▶ Obtener Cookies",
            'collapse_cookies': "▼ Obtener Cookies",
            'check_updates': "Buscar Actualizaciones",
            'update_available': "Actualización disponible",
            'update_not_available': "No se encontraron actualizaciones",
            'update_checking': "Buscando actualizaciones...",
            'update_error': "Error al buscar actualizaciones",
            'current_version': "Versión actual: {}",
            'latest_version': "Última versión: {}",
            'update_btn_ok': "Bien",
            'update_btn_update': "Actualizar",
            'update_message': "¡Nueva versión {} disponible! ¿Desea ir a la página de descarga?",
            'time_synchronized': "Hora sincronizada",
            'ms': "ms",
            'default': "predeterminado",
            'welcome_title': "Xiaomi Unlock Tool",
            'welcome_text': (
                "¡Bienvenido a Xiaomi Unlock Tool!\n\n"
                "ADVERTENCIA IMPORTANTE:\n\n"
                "¡ANTES DE USAR, LEA CUIDADOSAMENTE LAS INSTRUCCIONES!\n\n"
                "1. El uso de esta herramienta puede provocar bloqueo de envío.\n\n"
                "2. La herramienta es SOLO para dispositivos con HyperOS Global\n"
                "   y NO funciona con modelos chinos.\n\n"
                "3. Requisitos:\n"
                "   • Cuenta Mi con más de 30 días\n"
                "   • Cuenta Mi Community con región Global\n\n"
                "4. Al usar esta herramienta, acepta que los desarrolladores no asumen responsabilidad por sus dispositivos.\n\n"
                "Haga clic en 'Continuar' para comenzar."
            ),
            'welcome_btn': "Continuar",
            'color_theme_xiaomi': "Xiaomi Orange",
            'color_theme_blue': "Blue Word",
            'color_theme_red': "Red Sun",
            'language_label': "Idioma",
            'log_to_txt_checkbox': "Registrar en archivo TXT",
            'spam_mode_checkbox': "Envío Spam (en Modo Automático)",
            'spam_mode_desc': "Envía solicitudes a las 23:59:58.6, 58.8, 59.1, 59.3, 59.5.\nSi está desactivado, envía una sola solicitud en el tiempo óptimo.",
            'ping_not_measured_manual': "Ping: no medido (modo manual)",
            'log_auto_mode_spam_selected': "Modo automático seleccionado (Spam)",
            'log_auto_mode_single_selected': "Modo automático seleccionado (Solicitud única)",
            'log_manual_mode_selected': "Modo manual seleccionado",
            'log_time_gt_2355': "Hora > 23:58. Sincronizando hora antes de comenzar...",
            'log_time_sync_success': "¡Hora sincronizada exitosamente!",
            'log_presync_wait': "Esperando pre-sincronización a las 23:58:00 (Pekín)...",
            'status_presync_wait': "Esperando 23:58 para sincronizar...",
            'log_presync_start': "¡Son las 23:58! Realizando sincronización precisa de hora...",
            'log_time_updated': "Hora actualizada: {}",
            'log_resync_error': "Error de resincronización, continuando con el temporizador actual.",
            'log_normal_mode_ping': "Modo normal: calculando ping...",
            'log_calculated_send_time': "Tiempo de envío calculado: 23:59:{}",
            'log_spam_mode_targets': "MODO SPAM: Tiempos objetivo: {}",
            'status_spam_wait': "Esperando ataque spam...",
            'log_spam_sending_at': "[Spam #{}] Enviando solicitud a las 23:59:{}s",
            'log_spam_new_device_id': "[Spam #{}] Nuevo deviceId: {}",
            'log_spam_response_prefix': "[Spam #{}] Tiempo: {}s",
            'log_spam_success_prefix': "¡ÉXITO!",
            'log_spam_response_format': "{} | Código: {} | {}",
            'log_spam_parse_error': "[Spam #{}] Error al analizar respuesta: {}",
            'log_spam_no_response': "[Spam #{}] No hay respuesta del servidor",
            'log_spam_send_error': "[Spam #{}] Error al enviar solicitud: {}",
        }

    def get_chinese(self):
        return {
            'title': "小米解锁工具",
            'main_title': f"小米解锁工具",
            'desc': (
                f"自动提交解锁申请的工具\n"
                f"作者: Vozduhan\n"
                f"版本: {self._get_version()}"
            ),
            'desc_manual': (
                f"手动模式 - 手动选择提交时间\n"
                f"作者: Vozduhan\n"
                f"版本: {self._get_version()}"
            ),
            'params': "参数",
            'log_success_prefix': "成功！",
            'log_code_message': "代码: {code} | 消息: {msg}",
            'log_request_parse_error': "[响应处理错误] 无法解析JSON: {data}",
            'log_request_failed_no_response': "[错误] 无法发送请求（无响应）",
            'log_request_exception': "[请求错误] {error}",
            'cookie_label': "New_bbs_ServiceToken:",
            'confirm': "我确认可能面临账户封禁的风险",
            'info': "信息",
            'status_ready': "准备就绪",
            'ping': "延迟: 未测量",
            'time': "时间: 未同步",
            'start_btn': "开始申请",
            'instructions_btn': "说明和脚本设置",
            'exit_btn': "退出",
            'log': "执行日志",
            'clear_log_btn': "清除",
            'unlock_start': "开始解锁过程...",
            'device_id_gen': "生成的deviceId: {}",
            'ping_start': "开始计算延迟...",
            'ping_server': "{} 的延迟: {:.2f} 毫秒",
            'ping_failed': "无法获取服务器 {} 的延迟",
            'ping_error': "ping {} 时出错: {}",
            'open_miflash': "小米解锁工具",
            'ping_default': "无法获取任何服务器的延迟！\n使用默认值: {} 毫秒",
            'ping_avg': "平均延迟: {:.2f} 毫秒",
            'ntp_connect': "尝试连接到NTP服务器: {}",
            'ntp_time': "从服务器 {} 接收到的北京时间: {}",
            'ntp_failed': "无法连接到任何NTP服务器。",
            'time_wait': "等待ping时间（北京时间23:59:48）...",
            'target_time': "等待至 {}（根据延迟 {} 毫秒调整）",
            'target_time_manual': "等待至 {}（手动模式）",
            'time_reached': "时间到达: {}。开始发送请求...",
            'cookie_skipped': "根据设置跳过cookie检查",
            'cookie_expired': "Cookie已过期，请更新",
            'account_ready': "[状态] 账户可以提交解锁申请。",
            'account_blocked': "[状态] 账户被禁止提交申请直至 {} (月/日)。",
            'account_new': "[状态] 账户创建不足30天。",
            'account_approved': "[状态] 申请已批准，可在 {} 前解锁。",
            'account_unknown': "[错误] 未知状态。",
            'status_error': "[状态检查错误] {}",
            'request_sent': "\n在 {} (UTC+8) 发送请求",
            'response_received': "在 {} (UTC+8) 收到响应",
            'request_failed': "[错误] 无法发送请求",
            'response_error': "[响应处理错误] {}",
            'request_error': "[请求错误] {}",
            'confirm_warning': "请确认您了解所有风险！",
            'cookie_error': "请输入cookie值！",
            'time_error': "无法同步时间！",
            'settings_saved': "\n设置已保存：",
            'cookie_check': "Token Cookie检查: {}",
            'default_ping': "默认延迟: {} 毫秒",
            'ping_note': "如果无法测量服务器延迟，将使用此值。",
            'saved': "设置保存成功！",
            'instructions_title': "说明和脚本设置",
            'about_title': "关于",
            'about_content': (
                f"自动发送解锁引导加载程序请求的工具\n"
                f"适用于运行HyperOS的小米设备\n\n"
                f"脚本版本: {self._get_version()}"
            ),
            'general_title': "要求",
            'general_content': (
                "1. 小米账户必须超过30天\n \n"
                "2. Mi Community账户必须设置为\n \n"
                "全球区域\n \n"
                "3. 除中国ROM (CNXM)外的所有设备\n"
                "均可解锁\n \n"
                "4. 设备运行HyperOS"
            ),
            'firefox_title': "FireFox | Edge",
            'firefox_content': (
                "1. 下载Cookie Editor扩展\n\n"
                "2. 登录您的账户（先退出）\n"
                "在小米社区网站:\n\n"
                "http://new.c.mi.com/global\n"
                "或 \n"
                "http://mi.com\n\n"
                "3. 在Cookie Editor窗口中提取\n"
                "new_bbs_token并复制\n\n"
                "重要说明:\n \n"
                "1. 脚本中的所有时间均为北京时间"
            ),
            'chrome_title': "Chrome",
            'chrome_content': (
                "1. 登录您的账户（先退出）\n"
                "在小米社区网站:\n"
                "https://new.c.mi.com/global\n"
                "或 \n"
                "https://mi.com\n\n"
                "2. 在浏览器地址栏输入命令:\n\n"
                "javascript :(function(){var token=document.cookie.match(/popRunToken=([^;]+)/);"
                "if(token){prompt(\"复制令牌:\", token[1]);}"
                "else{alert(\"未找到令牌\");}})()\n\n"
                "*将命令粘贴到浏览器地址栏时，请记得删除javascript后面的空格*\n\n"
                "3. 从弹出窗口复制令牌值\n\n"
                "重要说明:\n \n"
                "1. 脚本中的所有时间均为北京时间"
            ),
            'trouble_title': "故障排除",
            'trouble_content': """问题：CookieEditor不显示new_bbs_serviceToken

解决方案：

1. 刷新页面

2. 退出并重新登录

问题：Cookie过期或不起作用

可能的原因：

• 账户区域不是全球（切换它）

• Cookie确实已过期

问题：达到请求限制

解决方案：

在手机设置中检查Mi Unlock状态

问题：错误10001和其他

解决方案：

脚本无法提交请求

联系开发者：

• 通过Telegram群组：

https://t.me/miunlocktoolrevamp""",
            'authors_title': "作者",
            'authors_content': """开发者：

• Vozduhan | Tg: @hyeplet231

链接：

Telegram群组：https://t.me/miunlocktoolrevamp

GitHub：https://github.com/AsInsideOut/miunlocktool

Reddit：https://www.reddit.com/r/miunlocktool

脚本基于：

• Vierta

脚本版本：""" + self._get_version(),
            'cookie_checkbox': "在提交前禁用Token Cookie检查",
            'ping_label': "默认延迟（毫秒）:",
            'color_theme_label': "颜色主题:",
            'color_theme_xiaomi_orange': "小米橙色",
            'color_theme_red_sun': "红日",
            'color_theme_blue_world': "蓝色世界",
            'save_btn': "保存",
            'close_btn': "关闭",
            'ping_error_title': "错误",
            'ping_error_msg': "延迟必须为正数！",
            'cookie_error_title': "错误",
            'account_blocked_title': "信息",
            'account_new_title': "信息",
            'account_approved_title': "成功",
            'unknown_status_title': "错误",
            'install_error': "安装错误",
            'import_error': "导入错误",
            'settings': "设置",
            'cookie_check_state': "已禁用" if False else "已启用",
            'ban_risk': "我确认可能面临账户封禁的风险",
            'submit_application': "开始申请",
            'script_info': "说明和脚本设置",
            'exit': "退出",
            'execution_log': "执行日志",
            'clear_log_btn': "清除",
            'unlock_process': "开始解锁过程...",
            'auto_mode': "自动模式",
            'manual_mode': "手动模式",
            'manual_time_label': "提交时间（秒）:",
            'manual_time_hint': "58.5 - 59.8（例如：59.1）",
            'manual_mode_start': "手动模式：在23:59:{}发送",
            'manual_time_error': "时间无效。请使用格式58.5 - 59.8",
            'application_not_submitted': "[状态] 申请未提交，超出限制，请在 {} (月/日) 重试。",
            'device_binding_hint': "尝试在设置中的Mi Unlock状态部分绑定设备",
            'theme_label': "界面主题:",
            'theme_system': "系统",
            'theme_light': "浅色",
            'theme_dark': "深色",
            'mode_label': "操作模式:",
            'cookies_title': "获取Cookies",
            'expand_cookies': "▶ 获取Cookies",
            'collapse_cookies': "▼ 获取Cookies",
            'check_updates': "检查更新",
            'update_available': "有新更新可用",
            'update_not_available': "未找到更新",
            'update_checking': "正在检查更新...",
            'update_error': "检查更新时出错",
            'current_version': "当前版本: {}",
            'latest_version': "最新版本: {}",
            'update_btn_ok': "好的",
            'update_btn_update': "更新",
            'update_message': "新版本 {} 可用！是否前往下载页面？",
            'time_synchronized': "时间已同步",
            'ms': "毫秒",
            'default': "默认",
            'welcome_title': "小米解锁工具",
            'welcome_text': (
                "欢迎使用小米解锁工具！\n\n"
                "重要警告：\n\n"
                "使用前请仔细阅读说明！\n\n"
                "1. 使用此工具可能导致提交申请被禁止。\n\n"
                "2. 此工具仅适用于全球版HyperOS设备\n"
                "   不适用于中国型号。\n\n"
                "3. 要求：\n"
                "   • 小米账户超过30天\n"
                "   • Mi Community账户设置为全球区域\n\n"
                "4. 使用此工具即表示您同意开发者不对您的设备承担任何责任。\n\n"
                "点击'继续'开始。"
            ),
            'welcome_btn': "继续",
            'color_theme_xiaomi': "小米橙色",
            'color_theme_blue': "蓝色世界",
            'color_theme_red': "红日",
            'language_label': "语言",
            'log_to_txt_checkbox': "记录到TXT文件",
            'spam_mode_checkbox': "垃圾邮件发送（自动模式下）",
            'spam_mode_desc': "在23:59:58.6、58.8、59.1、59.3、59.5秒发送请求。\n如果禁用，则在最佳时间发送单个请求。",
            'ping_not_measured_manual': "延迟: 未测量（手动模式）",
            'log_auto_mode_spam_selected': "选择了自动模式（垃圾邮件）",
            'log_auto_mode_single_selected': "选择了自动模式（单个请求）",
            'log_manual_mode_selected': "选择了手动模式",
            'log_time_gt_2355': "时间 > 23:58。开始前同步时间...",
            'log_time_sync_success': "时间同步成功！",
            'log_presync_wait': "等待预同步于23:58:00（北京时间）...",
            'status_presync_wait': "等待23:58同步...",
            'log_presync_start': "已到23:58！执行精确时间同步...",
            'log_time_updated': "时间更新: {}",
            'log_resync_error': "重新同步错误，继续使用当前计时器。",
            'log_normal_mode_ping': "正常模式：计算延迟...",
            'log_calculated_send_time': "计算发送时间: 23:59:{}",
            'log_spam_mode_targets': "垃圾邮件模式：目标时间: {}",
            'status_spam_wait': "等待垃圾邮件攻击...",
            'log_spam_sending_at': "[垃圾邮件 #{}] 在23:59:{}s发送请求",
            'log_spam_new_device_id': "[垃圾邮件 #{}] 新deviceId: {}",
            'log_spam_response_prefix': "[垃圾邮件 #{}] 时间: {}s",
            'log_spam_success_prefix': "成功！",
            'log_spam_response_format': "{} | 代码: {} | {}",
            'log_spam_parse_error': "[垃圾邮件 #{}] 解析响应错误: {}",
            'log_spam_no_response': "[垃圾邮件 #{}] 服务器无响应",
            'log_spam_send_error': "[垃圾邮件 #{}] 发送请求错误: {}",
        }

    def _get_version(self):
        # Импортируем версию из главного скрипта
        try:
            from .. import CURRENT_VERSION
            return CURRENT_VERSION
        except:
            return "5.9"

    def tr(self, key):
        return self.translations[self.language].get(key, key)