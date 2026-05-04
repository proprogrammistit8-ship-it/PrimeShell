import os
from fabric.widgets.box import Box
from fabric.widgets.entry import Entry
from fabric.widgets.button import Button
from fabric.widgets.scrolledwindow import ScrolledWindow
from fabric.widgets.wayland import WaylandWindow as Window

class PrimeShellLauncher(Window):
    def __init__(self, **kwargs):
        super().__init__(
            name="launcher",
            layer="overlay",
            anchor="bottom", # По центру экрана
            visible=False,
            all_visible=False,
            **kwargs
        )

        # Список всех приложений (название: команда)
        # Для начала можно захардкодить пару штук для теста
        self.apps = {
            "Ghostty": "ghostty",
            "Firefox": "firefox",
            "Neovide": "neovide",
            "Discord": "discord"
        }

        self.results_box = Box(orientation="v", spacing=5)
        
        # Поле ввода
        self.search_entry = Entry(
            name="launcher-search",
            placeholder="Search apps...",
            on_changed=self.on_search_changed,
            on_activate=self.on_submit
        )

        # Контейнер со скроллом для результатов
        self.scroll_container = ScrolledWindow(
            min_content_size=(300, 400),
            child=self.results_box
        )

        self.main_box = Box(
            name="launcher-box",
            orientation="v",
            spacing=10,
            children=[self.search_entry, self.scroll_container]
        )

        self.add(self.main_box)
        self.update_list("") # Показываем всё при старте

    def on_search_changed(self, entry, *args):
        query = entry.get_text().lower()
        self.update_list(query)

    def update_list(self, query):
        # Очищаем старые результаты
        for child in self.results_box.get_children():
            self.results_box.remove(child)

        # Фильтруем и добавляем новые
        for name, cmd in self.apps.items():
            if query in name.lower():
                btn = Button(
                    label=name,
                    on_clicked=lambda *args, c=cmd: self.launch(c)
                )
                self.results_box.add(btn)
        self.results_box.show_all()

    def launch(self, cmd):
        os.popen(f"{cmd} &")
        self.hide()

    def on_submit(self, *args):
        # Запускаем первый результат при нажатии Enter
        children = self.results_box.get_children()
        if children:
            children[0].emit("clicked")