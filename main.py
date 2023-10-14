# Minecraft Chinese Mainland Login Fix Tools
from lovemilkMCCMLFT.pages.login_hosts import LoginHostsUI
from lovemilkMCCMLFT.pages.auth_hosts import AuthHostsUI
from lovemilkMCCMLFT.database.manager import Manager
from lovemilkMCCMLFT.database.ip import LOGIN, AUTHSERVER
import asyncio
import version
import flet as ft


def main(page: ft.Page):
    page.title = f'Lovemilk Minecraft Chinese Mainland Login Fix Tools V{version.VERSION_STRING}'
    page.window_min_width = 1024
    page.window_min_height = 512
    fonsts = {
        'main': 'resources/opposans-cufonfonts/OPPOSansMedium.ttf',
        'MiSansMedium': 'resources/MiSans/MiSans-Medium.ttf'
    }

    mgr = Manager()

    page_name = 'login'

    def switch_page(event):
        nonlocal ui
        nonlocal page_name

        if ui.delay_test_button.disabled:
            ui.add_dialog(
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text('警告', color='error'),
                    content=ft.Text('请等待异步请求完成!'),
                    actions=[
                        ft.TextButton('好的吧, 我再等等...'),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            )
            return

        page.clean()
        if page_name == 'login':
            page_name = 'auth'
            switch_page_button.text = f'切换到 启动器登录/皮肤下载 Hosts 页面'
            ui = AuthHostsUI(page, mgr, AUTHSERVER, [switch_page_button, ], fonsts, 'main')
        elif page_name == 'auth':
            page_name = 'login'
            switch_page_button.text = f'切换到 验证服务器 Hosts 页面'
            ui = LoginHostsUI(page, mgr, LOGIN, [switch_page_button, ], fonsts, 'main')
            page.update()
    
    switch_page_button = ft.ElevatedButton(
        f'切换到 验证服务器 Hosts 页面',
        on_click=switch_page
    )

    ui = LoginHostsUI(page, mgr, LOGIN, [switch_page_button, ], fonsts, 'main')


ft.app(target=main)
