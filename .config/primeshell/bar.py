import fabric # Импортируем Базовый пакет
# import sass # SASS and SCSS support # Deleted
from fabric import Application # Чтобы запустить, ибо это фундамент всего шелла
from fabric.widgets.box import Box # Берём коробку
from fabric.widgets.label import Label # Тут получаем Label
from fabric.widgets.wayland import WaylandWindow as Window # Берём окно
from fabric.widgets.button import Button
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.datetime import DateTime
from fabric.utils import set_stylesheet_from_file
#from fabric.widgets.revealer import Revealer
from fabric.hyprland.widgets import Language, ActiveWindow, Workspaces, WorkspaceButton, Hyprland
from fabric.utils import FormattedString
from modules.network import NetworkIndicator
from fabric.system_tray.widgets import SystemTray
#from fabric.widgets.svg import Svg
#from fabric.utils import SassProcessor
#from styles import style

class PrimeShellBar(Window):
    def __init__(self, **kwargs):
        super().__init__(
            name="bar",
            layer="top",              # Поверх всех окон
            anchor="top left right",  # Растягиваем по горизонтали вверху
            exclusivity="auto",   # Говорим Niri подвинуть другие окна
            visible=False,
            all_visible=False,
            #keyboard_mode="exclusive", # КРИТИЧНО: Забирает фокус клавиатуры на себя
            **kwargs
        )


        self.date_time = DateTime(
            name="time",
            #width_request=100,
            height_request=500,
            h_expand=False,     # НЕ растягиваться по горизонтали
            v_expand=False,     # НЕ растягиваться по вертикали
            h_align="center",   # Центрироваться внутри своей доли CenterBox
            v_align="center"
        )
        self.workspaces = Workspaces(
            name="workspaces-module",
            spacing=1,
            buttons_factory=lambda ws_id: WorkspaceButton(
                id=ws_id, 
                label=f"{ws_id}", 
                name="worksapce-module-button",
                #width_request=40,
                #height_request=20
            ) if ws_id > 0 else None,
        )
        self.language = Language(
            formatted=FormattedString(
                "{replace_lang(language)}",
                replace_lang=lambda lang: bulk_replace(
                    lang,
                    (r".*Eng.*", r".*Ru.*"),
                    ("ENG", "RUS"),
                    regex=True,
                ),
            ),
            name="language-module"
        )
        self.active_window = ActiveWindow(
            name="active-window-module"
        )

        self.os_button = Button(
            name="os-button",
            label="",
            on_clicked=self.toggle_dashboard
        )

        self.dashboard_button = Button(
            name="dashboard-button",
            label="󰕮"
        )

        #self.right_corner = Svg(svg_file="./assets/right-corner.svg")
        #self.left_corner = Svg(svg_file="./assets/left-corner.svg")

        self.center_modules = Box(
            children = [
                self.workspaces,
                self.dashboard_button,
                self.date_time
            ]
        )
        self.left_modules = Box(
            children = [
                self.os_button,
                self.active_window
            ]
        )

        self.right_modules = Box(
            children = [
                NetworkIndicator(
                    name="network-module"
                ),
                self.language
            ]
        )

        self.children = CenterBox(
            name="bar-body",
            center_children=self.center_modules,
            start_children=self.left_modules,
            end_children=self.right_modules
        ) #left_children=self.box)

        # МАГИЯ ПРОЗРАЧНОСТИ ТУТ:
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)
            
        self.set_app_paintable(True) # Позволяет окну быть "дырявым" (прозрачным)

        self.show_all()
        self.visible = True
    

    def toggle_dashboard(self, *args):
        pass


# Магия для прозрачности фона самого окна
#PrimeShellBar.set_visual(PrimeShellBar.get_screen().get_rgba_visual())

# app.load_style(style) # Not working
#PrimeShellBar.set_stylesheet_from_file("style.css")