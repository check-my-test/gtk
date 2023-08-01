import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
import asyncio
import asyncio_glib

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Список товаров")

        self.button1 = Gtk.Button(label="Загрузить из API")
        self.button1.connect("clicked", self.on_button1_clicked)
        self.button2 = Gtk.Button(label="Загрузить из файла")
        self.button2.connect("clicked", self.on_button2_clicked)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)

        self.box.pack_start(self.button1, True, True, 50)
        self.box.pack_start(self.button2, True, True, 50)

    def on_button1_clicked(self, widget):
        self.show_loading_spinner("Loading from API")
        GLib.idle_add(self.do_api_loading)

    def on_button2_clicked(self, widget):
        self.show_loading_spinner("Loading from file")
        GLib.idle_add(self.do_file_loading)

    def show_loading_spinner(self, message):
        dialog = Gtk.Dialog(
            title=message,
            parent=self,
            flags=0,
            buttons=(),
        )

        spinner = Gtk.Spinner()
        dialog.vbox.pack_start(spinner, True, True, 0)
        spinner.show()

        dialog.set_transient_for(self)
        dialog.set_modal(True)

        def hide_dialog():
            dialog.destroy()

        dialog.show()
        spinner.start()

        GLib.idle_add(hide_dialog)

    def do_api_loading(self):
        print("Loading from API")
        # Здесь можно добавить код для загрузки данных из API
        # ...

        # Когда загрузка завершена, закрываем модальное окно:
        self.hide_modal_dialog()

    def do_file_loading(self):
        print("Loading from file")
        # Здесь можно добавить код для загрузки данных из файла
        # ...

        # Когда загрузка завершена, закрываем модальное окно:
        self.hide_modal_dialog()

    def hide_modal_dialog(self):
        for widget in self.get_children():
            if isinstance(widget, Gtk.Dialog):
                widget.destroy()

win = MyWindow()
win.set_default_size(800, 600)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
