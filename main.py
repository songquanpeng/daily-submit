import asyncio
import json
import os

import requests
from playwright.async_api import async_playwright

target_url = 'https://enroll.scut.edu.cn/door/health/h5/health.html'


def send_msg(msg, push_url):
    if not push_url:
        print(msg)
    else:
        if push_url.endswith("/"):
            push_url = push_url.rstrip("/")
        requests.get("{}/?title=每日健康填报&description={}".format(push_url, msg))


async def report_health(username, password, debug=False):
    async with async_playwright() as p:
        if debug:
            browser = await p.chromium.launch(headless=False, slow_mo=50)
        else:
            browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(target_url)
        await page.fill("#un", username)
        await page.fill("#pd", password)
        await page.click("#index_login_btn > input")
        await page.click("#container > div.main > form > div.btn_add")
        await page.click(
            "body > div.custom-classname > div.weui-dialog.weui-animate-fade-in > div.weui-dialog__ft > a.weui-dialog__btn.weui-dialog__btn_primary")
        message = await page.text_content("#weuiDialogSuc > div.weui-dialog > div.weui-dialog__bd")
        await browser.close()
        return message


def generate_cfg(cfg_path):
    username = input("Please input your student id: ")
    password = input("Please input your password: ")
    message_push_url = input("Please input your message push url (optional): ")
    cfg = {
        "username": username,
        "password": password,
        "message_push_url": message_push_url
    }
    with open(os.path.join(cfg_path), 'w') as f:
        print(json.dumps(cfg, sort_keys=True, indent=4, ensure_ascii=False), file=f)
    print("Your configuration is saved at ", cfg_path)
    return cfg


def load_cfg(cfg_path="config.json"):
    if os.path.exists(cfg_path):
        with open(cfg_path, 'r') as f:
            cfg = json.load(f)
    else:
        cfg = generate_cfg(cfg_path)
    return cfg


async def main(debug=False):
    cfg = load_cfg()
    msg = await report_health(cfg["username"], cfg["password"], debug)
    send_msg(msg, push_url=cfg["message_push_url"])


if __name__ == '__main__':
    asyncio.run(main())
