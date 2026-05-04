from gi.repository import Gio
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.label import Label

class NetworkIndicator(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(text="  ", name="network-label")
        self.add(self.label)
        
        # Получаем стандартный монитор сети
        self.monitor = Gio.NetworkMonitor.get_default()
        
        # Подключаем сигнал: как только состояние сети изменится, вызовется метод
        self.monitor.connect("network-changed", self.on_network_changed)
        
        # Инициализируем начальное состояние
        self.on_network_changed(self.monitor, self.monitor.get_network_available())

    def on_network_changed(self, monitor, available):
        if available:
            self.label.set_text("󰖩") # Онлайн (Wi-Fi иконка)
            self.label.get_style_context().remove_class("offline")
        else:
            self.label.set_text("󰖪") # Оффлайн (Перечеркнутый Wi-Fi)
            self.label.get_style_context().add_class("offline")
