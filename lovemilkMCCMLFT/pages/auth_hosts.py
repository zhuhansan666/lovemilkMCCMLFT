import flet as ft
from aioping import ping
import asyncio
from typing import Any

from . import UI
from ..database.manager import Manager
from ..types import IPDict


class AuthHostsUI(UI):
    def __init__(
            self,
            page: ft.Page,
            # view: ft.View,
            # version: str,
            mgr: Manager,
            auth_data: IPDict,
            appbar_actions: list[ft.Control] | None = None,
            fonts: dict[str, str] | None = None,
            fonst_family: str | None = None
    ) -> None:
        super().__init__(page)
        # self.view = view
        # self.page.title = f'Lovemilk Minecraft China Mainland Login Fix Tools V{version}'
        self.mgr = mgr
        self.login_data = auth_data

        self.delay_test_button = ft.ElevatedButton(
            '延时测试',
            icon=ft.icons.REFRESH,
            on_click=self.delay_test,
        )
        self.open_hosts_button = ft.ElevatedButton(
            '打开 Hosts 文件',
            icon='FILE_OPEN',
            on_click=lambda event: self.mgr.open_hosts()
        )
        self.delete_hosts_button = ft.ElevatedButton(
            '删除当前页面已改 Hosts',
            icon=ft.icons.DELETE_SWEEP_OUTLINED,
            on_click=self.delete_hosts,
        )
        # self.about_button  # TODO: about page

        self.login_listview = ft.ListView(expand=True, spacing=5)
        self.page.add(
            ft.Row([
                ft.Container(
                    ft.Text('IP'),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.Container(
                    ft.Text('国家 / 地区 / 服务提供商'),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
                ft.Container(
                    ft.Text('延时'),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )
        self.page.add(self.login_listview)
        self.init_login_listview()

        actions = (appbar_actions if appbar_actions is not None else []) + [
                self.delay_test_button,
                self.open_hosts_button,
                self.delete_hosts_button
            ]
        page.appbar = ft.AppBar(
            title=ft.Text('验证服务器 Hosts 修改'),
            actions=actions,
        )

        page.fonts = fonts if fonts is not None else {}
        page.theme = ft.Theme(font_family=fonst_family)

        page.update()
        # self.delay_test(None)

    def init_login_listview(self, delays: dict[str, float] | None = None):
        delays = delays if delays is not None else {}

        for location, ips in self.login_data['ips'].items():
            for ip in ips:
                self.login_listview.controls.append(
                    ft.Row([
                        ft.Container(
                            ft.ElevatedButton(
                                ip,
                                on_click=lambda event: self.set_hosts(
                                    event.control.text),
                                icon='CLOUD'
                            ),
                            alignment=ft.alignment.center,
                            expand=True,
                        ),
                        ft.Container(
                            ft.Text(location),
                            alignment=ft.alignment.center,
                            expand=True,
                        ),
                        ft.Container(
                            ft.Text(f'{delays.get(ip)} ms' if delays.get(ip) is not None else '未经测试'),
                            alignment=ft.alignment.center,
                            expand=True,
                        ),
                    ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                )
        self.login_listview.update()

    def sort_login_listview(self):
        controls: Any = self.login_listview.controls
        self.login_listview.controls = sorted(
            controls,
            key=lambda item:
                float(
                    item.controls[2].content.value[:-2]
                    if item.controls[2].content.value.endswith('ms') else
                    'INF'
                )
        )
        self.login_listview.update()

    async def ping(self, ip: str, controls, timeout: int = 3):
        control = next(filter(
            lambda row: row.controls[0].content.text == ip,
            controls
        ))

        control.controls[2].content.value = '正在请求...'
        control.controls[2].content.color = 'secondary'
        control.controls[0].content.disabled = True
        self.page.update()

        try:
            result = (await ping(ip, timeout=timeout))
        except TimeoutError:
            result = None

        if result is None:
            control.controls[2].content.value = '请求超时'
            control.controls[2].content.color = 'error'
            self.page.update()
            return

        result *= 1000

        control.controls[0].content.disabled = False
        control.controls[2].content.value = f'{round(result, 3)} ms'
        control.controls[2].content.color = 'teal'

        self.page.update()

        return result

    def delay_test(self, event):
        if not self.page.appbar:
            return

        self.page.appbar.title = ft.Text('正在测试延时, 请等待请求完成自动排序...', color='teal')
        self.delay_test_button.disabled = True
        self.page.update()

        tasks = []

        controls: Any = self.login_listview.controls

        for ips in self.login_data['ips'].values():
            for ip in ips:
                tasks.append(self.ping(ip, controls))

        async def gather():
            return await asyncio.gather(*tasks)

        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        asyncio.run(gather())

        self.sort_login_listview()

        self.page.appbar.title = ft.Text('验证服务器 Hosts 修改')
        self.delay_test_button.disabled = False
        self.page.update()

    def set_hosts(self, ip, confirm: bool = False):
        if not confirm:
            self.add_dialog(
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text('请确认是否替换'),
                    content=ft.Text(f'你真的想要替换 Hosts 吗?\n当前选中: {ip}'),
                    actions=[
                        ft.TextButton(
                            '是', on_click=lambda event: self.set_hosts(ip, True)),
                        ft.TextButton('否'),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            )
            return

        try:
            self.mgr.delete('auth')

            result = ''
            for domain in self.login_data['domains']:
                result += f'{ip} {domain}\n'

            self.mgr.write('auth', result)

            self.add_dialog(
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text('替换成功!'),
                    content=ft.Text('替换 Hosts 成功'),
                    actions=[
                        ft.TextButton('我了解'),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            )
        except Exception as e:
            self.add_dialog(
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text('替换失败', color='error'),
                    content=ft.Text(repr(e)),
                    actions=[
                        ft.TextButton('好的吧'),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            )

    def delete_hosts(self, event, confirm: bool = False):
        if not confirm:
            self.add_dialog(
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text('请确认是否删除'),
                    content=ft.Text('你真的想要删除 Hosts 吗?'),
                    actions=[
                        ft.TextButton(
                            '是', on_click=lambda event: self.delete_hosts(event, True)),
                        ft.TextButton('否'),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            )
            return

        try:
            self.mgr.delete('auth')

            self.add_dialog(
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text('删除成功!'),
                    content=ft.Text('删除 Hosts 成功'),
                    actions=[
                        ft.TextButton('我了解'),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            )
        except Exception as e:
            self.add_dialog(
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text('删除失败', color='error'),
                    content=ft.Text(repr(e)),
                    actions=[
                        ft.TextButton('好的吧'),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
            )
