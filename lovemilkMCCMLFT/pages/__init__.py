import flet as ft
from typing import Any, Optional
from types import FunctionType

dialogs = ft.AlertDialog | ft.Banner | ft.BottomSheet | ft.SnackBar


class UI:
    def __init__(self, page: ft.Page) -> None:
        _dialog: Any = page.dialog  # as Any to fix typing error
        self.page = page

        self.page.dialog = _dialog
        self.dialog_events: list[dialogs] = []

    @property
    def dialog(self) -> dialogs:
        _dialog: Any = self.page.dialog
        return _dialog

    @dialog.setter
    def dialog(self, value: Optional[dialogs]):
        self.page.dialog = value

    def add_dialog(self, dialog: dialogs, immediately: bool = False):
        if immediately:
            self.dialog_events.insert(0, dialog)

            if self.dialog is not None:
                if self.dialog.open:
                    self.dialog.open = False

                self.dialog = None
        else:
            self.dialog_events.append(dialog)

        self.page.add(dialog)
        self.__handle_dialog_close(dialog)  # handle dialog close events
        if self.dialog is None or self.dialog.open is False:
            self.update_dialog()

    def update_dialog(self):
        if len(self.dialog_events) <= 0:
            return

        self.dialog = self.dialog_events[0]
        self.page.dialog = self.dialog
        self.dialog_events.pop(0)
        self.open_dialog()

    def open_dialog(self):
        if self.dialog is not None:
            self.dialog.open = True
        self.dialog.update()

    def close_dialog(self):
        if self.dialog is not None:
            self.dialog.open = False
        self.dialog.update()

        self.update_dialog()

    def __handle_dialog_close(self, dialog: dialogs):
        for control in getattr(dialog, 'actions', []):
            if control.__class__.__name__.endswith('Button'):  # is flet button
                on_click_func = getattr(control, 'on_click', False)

                if on_click_func is False:  # on_click func may be None
                    continue

                # close when any button clicked
                setattr(control, 'on_click_old', on_click_func)
                setattr(control, 'on_click', lambda event: (
                    (event.control.on_click_old or (lambda event: ()))(event),
                    self.close_dialog()
                ))

        on_dismiss_func = getattr(dialog, 'on_dismiss', False)
        if on_dismiss_func is not False:
            # close when dismiss

            setattr(dialog, 'on_dismiss_old', on_dismiss_func)
            setattr(dialog, 'on_dismiss', lambda event: (
                (event.control.on_dismiss_old or (lambda event: ()))(event),
                self.close_dialog()
            ))


if __name__ == '__main__':
    def test(page: ft.Page):
        ui = UI(page)
        page.theme = ft.Theme(color_scheme=ft.ColorScheme(
            on_primary='#114514'))  # 支持 MD3 的颜色, 好耶!
        page.add(ft.ElevatedButton(
            'open',
            on_click=lambda e: ui.add_dialog(
                ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Please confirm"),
                    content=ft.Text(
                        "Test Box"
                    ),
                    actions=[
                        ft.TextButton("Yes"),
                        ft.TextButton("No"),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    on_dismiss=lambda e: print(
                        "Modal dialog dismissed!"
                    ),
                )
            )
        )
        )

    ft.app(target=test)
