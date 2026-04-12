import json
import time
import hashlib
import random
import threading
import statistics
from datetime import datetime, timedelta, timezone

import ntplib
import pytz
import urllib3


class HTTP11Session:
    def __init__(self):
        self.http = urllib3.PoolManager(
            maxsize=10,
            retries=True,
            timeout=urllib3.Timeout(connect=2.0, read=15.0),
            headers={}
        )

    def make_request(self, method, url, headers=None, body=None):
        try:
            request_headers = {}
            if headers:
                request_headers.update(headers)

            request_headers['Content-Type'] = 'application/json; charset=utf-8'

            if method == 'POST':
                if body is None:
                    body = '{"is_retry":true}'.encode('utf-8')
                request_headers['Content-Length'] = str(len(body))

            request_headers['Accept-Encoding'] = 'gzip, deflate, br'
            request_headers['User-Agent'] = 'okhttp/4.12.0'
            request_headers['Connection'] = 'keep-alive'

            response = self.http.request(
                method,
                url,
                headers=request_headers,
                body=body,
                preload_content=False
            )
            return response
        except Exception:
            return None


class RequestHandler:
    def __init__(self, app):
        self.app = app
        self.session = HTTP11Session()
        self.ntp_servers = [
            "time1.google.com", "time2.google.com", "time3.google.com", "time4.google.com", "time.android.com",
            "time.aws.com", "time.google.com", "time.cloudflare.com",
            "ntp.time.in.ua", "stratum1.net", "ntp5.stratum2.ru"
        ]
        self.mi_servers = ['sgp-api.buy.mi.com']
        self.last_success_dialog_shown = False

    def generate_device_id(self):
        random_data = f"{random.random()}-{time.time()}-{random.randint(0, 1000000)}"
        device_id = hashlib.sha1(random_data.encode('utf-8')).hexdigest().upper()
        return device_id

    def debug_ping(self, host):
        try:
            from icmplib import ping
            result = ping(host, count=1, interval=0.5, timeout=2)
            return result.avg_rtt if result.is_alive else None
        except Exception as e:
            self.app.log_message(self.app.translation.tr('ping_error').format(host, e))
            return None

    def get_average_ping(self):
        all_pings = []
        self.app.log_message(self.app.translation.tr('ping_start'))

        def ping_server(server):
            pings = []
            for attempt in range(3):
                result = self.debug_ping(server)
                if result is not None:
                    pings.append(result)
                time.sleep(0.2)
            return statistics.mean(pings) if pings else None

        for server in self.mi_servers:
            try:
                ping_time = ping_server(server)
                if ping_time is not None:
                    all_pings.append(ping_time)
                    self.app.log_message(self.app.translation.tr('ping_server').format(server, ping_time))
                else:
                    self.app.log_message(self.app.translation.tr('ping_failed').format(server))
            except Exception as e:
                self.app.log_message(self.app.translation.tr('ping_error').format(server, str(e)))

        if not all_pings:
            default_ping = self.app.settings['default_ping']
            self.app.log_message(self.app.translation.tr('ping_default').format(default_ping))
            self.app.ping_var.set(
                f"{self.app.translation.tr('ping')}: {default_ping} {self.app.translation.tr('ms')} ({self.app.translation.tr('default')})")
            return default_ping

        avg_ping = statistics.mean(all_pings)
        self.app.log_message(self.app.translation.tr('ping_avg').format(avg_ping))
        self.app.ping_var.set(f"{self.app.translation.tr('ping')}: {avg_ping:.2f} ms")
        return avg_ping

    def get_initial_beijing_time(self):
        client = ntplib.NTPClient()
        beijing_tz = pytz.timezone("Asia/Shanghai")
        for server in self.ntp_servers:
            try:
                self.app.log_message(self.app.translation.tr('ntp_connect').format(server))
                response = client.request(server, version=3)
                ntp_time = datetime.fromtimestamp(response.tx_time, timezone.utc)
                beijing_time = ntp_time.astimezone(beijing_tz)
                self.app.log_message(self.app.translation.tr('ntp_time').format(
                    server, beijing_time.strftime('%Y-%m-%d %H:%M:%S.%f')))
                self.app.time_var.set(
                    f"{self.app.translation.tr('time_synchronized')}: {beijing_time.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)")
                return beijing_time
            except Exception as e:
                self.app.log_message(f"Error connecting to {server}: {e}")
        self.app.log_message(self.app.translation.tr('ntp_failed'))
        return None

    def get_synchronized_beijing_time(self, start_beijing_time, start_timestamp):
        elapsed = time.time() - start_timestamp
        current_time = start_beijing_time + timedelta(seconds=elapsed)
        return current_time

    def calculate_script_time(self, ping_ms):
        ping_seconds = ping_ms / 1000.0
        send_time = 60.0 - ping_seconds
        if send_time < 58.0:
            send_time = 58.0
        if send_time > 59.9:
            send_time = 59.9
        return send_time

    def check_unlock_status(self, cookie_value, device_id):
        if self.app.settings['skip_cookie_check']:
            self.app.log_message(self.app.translation.tr('cookie_skipped'))
            return True

        try:
            url = "https://sgp-api.buy.mi.com/bbs/api/global/user/bl-switch/state"
            headers = {
                "Cookie": f"new_bbs_serviceToken={cookie_value};versionCode=500411;versionName=5.4.11;deviceId={device_id};"
            }

            response = self.session.make_request('GET', url, headers=headers)
            if response is None:
                self.app.log_message("[Error] Failed to get unlock status.")
                return False

            response_data = json.loads(response.data.decode('utf-8'))
            response.release_conn()

            if response_data.get("code") == 100004:
                self.app.log_message(self.app.translation.tr('cookie_expired'))
                from tkinter import messagebox
                messagebox.showerror("Error", self.app.translation.tr('cookie_expired'))
                return False

            data = response_data.get("data", {})
            is_pass = data.get("is_pass")
            button_state = data.get("button_state")
            deadline_format = data.get("deadline_format", "")

            if is_pass == 4:
                if button_state == 1:
                    self.app.log_message(self.app.translation.tr('account_ready'))
                    return True
                elif button_state == 2:
                    self.app.log_message(self.app.translation.tr('account_blocked').format(deadline_format))
                    from tkinter import messagebox
                    messagebox.showinfo(
                        self.app.translation.tr('account_blocked_title'),
                        self.app.translation.tr('account_blocked').format(deadline_format)
                    )
                    return False
                elif button_state == 3:
                    self.app.log_message(self.app.translation.tr('account_new'))
                    from tkinter import messagebox
                    messagebox.showinfo(
                        self.app.translation.tr('account_new_title'),
                        self.app.translation.tr('account_new')
                    )
                    return False
            elif is_pass == 1:
                self.app.log_message(self.app.translation.tr('account_approved').format(deadline_format))
                from tkinter import messagebox
                messagebox.showinfo(
                    self.app.translation.tr('account_approved_title'),
                    self.app.translation.tr('account_approved').format(deadline_format)
                )
                return False
            else:
                self.app.log_message(self.app.translation.tr('account_unknown'))
                from tkinter import messagebox
                messagebox.showerror(
                    self.app.translation.tr('unknown_status_title'),
                    self.app.translation.tr('account_unknown')
                )
                return False
        except Exception as e:
            self.app.log_message(self.app.translation.tr('status_error').format(e))
            return False

    def single_request(self):
        cookie = self.app.cookie_value.get().strip()
        device_id = self.generate_device_id()

        url = "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth"
        headers = {
            "Cookie": f"new_bbs_serviceToken={cookie};versionCode=500411;versionName=5.4.11;deviceId={device_id};"
        }

        try:
            request_time = self.get_synchronized_beijing_time(self.app.start_beijing_time, self.app.start_timestamp)
            self.app.log_message(
                self.app.translation.tr('request_sent').format(request_time.strftime('%Y-%m-%d %H:%M:%S.%f')))

            response = self.session.make_request('POST', url, headers=headers)
            if response is None:
                self.app.log_message(self.app.translation.tr('request_failed'))
                from tkinter import messagebox
                messagebox.showerror("Error", self.app.translation.tr('request_failed'))
                return

            response_time = self.get_synchronized_beijing_time(self.app.start_beijing_time, self.app.start_timestamp)
            self.app.log_message(
                self.app.translation.tr('response_received').format(response_time.strftime('%Y-%m-%d %H:%M:%S.%f')))

            try:
                response_data = response.data
                response.release_conn()
                json_response = json.loads(response_data.decode('utf-8'))
                code = json_response.get("code")
                data = json_response.get("data", {})

                if code == 0:
                    apply_result = data.get("apply_result")
                    if apply_result == 1:
                        self.app.log_message("[Status] Application approved, checking status...")
                        self.check_unlock_status(cookie, device_id)
                        self.show_success_dialog()
                    elif apply_result == 3:
                        deadline_format = data.get("deadline_format", "Not specified")
                        self.app.log_message(
                            self.app.translation.tr('application_not_submitted').format(deadline_format))
                        from tkinter import messagebox
                        messagebox.showinfo(
                            "Information",
                            f"{self.app.translation.tr('application_not_submitted').format(deadline_format)}\n\n{self.app.translation.tr('device_binding_hint')}"
                        )
                elif code == 100001:
                    self.app.log_message("[Status] Application rejected, request error (code 100003).")
                elif code == 100003:
                    self.app.log_message("[Status] Application possibly approved, checking status...")
                    self.check_unlock_status(cookie, device_id)
                    self.show_success_dialog()
                elif code == 100004 or code == 10004:
                    error_msg = self.app.translation.tr('cookie_expired')
                    self.app.log_message(f"[Error] {error_msg}", color="red")
                    from tkinter import messagebox
                    messagebox.showerror(
                        self.app.translation.tr('cookie_error_title'),
                        error_msg
                    )
                else:
                    msg = json_response.get("message", "Unknown error")
                    self.app.log_message(f"[Error] Code: {code}, Message: {msg}", color="red")

            except Exception as e:
                self.app.log_message(self.app.translation.tr('response_error').format(e))
                from tkinter import messagebox
                messagebox.showerror("Error", self.app.translation.tr('response_error').format(e))

        except Exception as e:
            self.app.log_message(self.app.translation.tr('request_error').format(e))
            from tkinter import messagebox
            messagebox.showerror("Error", self.app.translation.tr('request_error').format(e))

    def show_success_dialog(self):
        if not hasattr(self, '_success_dialog_shown') or not self._success_dialog_shown:
            self._success_dialog_shown = True
            from tkinter import messagebox

            if self.app.translation.language == 'ru':
                title = "Успех!"
                message = "Успешно! Попробуйте привязать аккаунт."
            elif self.app.translation.language == 'id':
                title = "Sukses!"
                message = "Berhasil! Coba tautkan akun Anda."
            elif self.app.translation.language == 'es':
                title = "¡Éxito!"
                message = "¡Éxito! Intente vincular su cuenta."
            elif self.app.translation.language == 'pt':
                title = "Sucesso!"
                message = "Sucesso! Tente vincular sua conta."
            elif self.app.translation.language == 'zh':
                title = "成功！"
                message = "成功！尝试绑定您的帐户。"
            else:
                title = "Success!"
                message = "Success! Try to bind your account."

            messagebox.showinfo(title, message)

            def reset_flag():
                self._success_dialog_shown = False

            threading.Timer(5.0, reset_flag).start()

    def make_single_request_with_new_device_id(self, seq_num, offset_val, device_id):
        try:
            cookie = self.app.cookie_value.get().strip()

            self.app.log_message(self.app.translation.tr('log_spam_new_device_id').format(seq_num, device_id),
                                 color="blue")

            url = "https://sgp-api.buy.mi.com/bbs/api/global/apply/bl-auth"
            headers = {
                "Cookie": f"new_bbs_serviceToken={cookie};versionCode=500411;versionName=5.4.11;deviceId={device_id};"
            }

            response = self.session.make_request('POST', url, headers=headers)

            if response:
                try:
                    resp_data = response.data.decode('utf-8')
                    json_resp = json.loads(resp_data)
                    code = json_resp.get("code")
                    msg = json_resp.get("message", "")

                    prefix = self.app.translation.tr('log_spam_response_prefix').format(seq_num, f"{offset_val:.3f}")
                    log_str = self.app.translation.tr('log_spam_response_format').format(prefix, code, msg)

                    if code == 0 or code == 100003:
                        self.app.log_message(f"{self.app.translation.tr('log_spam_success_prefix')} {log_str}",
                                             color="green")
                        if code == 0 or code == 100003:
                            self.show_success_dialog()
                    elif code == 100004 or code == 10004:
                        self.app.log_message(f"[Error] {self.app.translation.tr('cookie_expired')}", color="red")
                        from tkinter import messagebox
                        messagebox.showerror(
                            self.app.translation.tr('cookie_error_title'),
                            self.app.translation.tr('cookie_expired')
                        )
                    else:
                        self.app.log_message(log_str, color="orange")

                except Exception as e:
                    self.app.log_message(self.app.translation.tr('log_spam_parse_error').format(seq_num, e),
                                         color="red")
            else:
                self.app.log_message(self.app.translation.tr('log_spam_no_response').format(seq_num), color="red")

        except Exception as e:
            self.app.log_message(self.app.translation.tr('log_spam_send_error').format(seq_num, e), color="red")