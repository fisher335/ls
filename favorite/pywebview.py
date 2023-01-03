import time

import webview


def evaluate_js(window):
    result = window.evaluate_js(
        r"""
        var username = document.getElementById('webUserName')
        username.value = "17643"
        var pd = document.getElementById('webUserPassword')
        pd.value  = "@!"
        """
    )


def now():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def check() -> bool:
    s = '2023-10-26 00:00:00'
    now()
    if now() > s:
        return False
    else:
        return True


if __name__ == '__main__':
    if check():
        window = webview.create_window('Run custom JavaScript', url='https://sjz.cetcsc.com/')
        webview.start(evaluate_js, window)
    else:
        window = webview.create_window('软件已过期', url='https://www.baidu.com/')
        webview.start(evaluate_js, window)
