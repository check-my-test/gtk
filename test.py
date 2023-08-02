import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import asyncio
import gbulb
import time

gbulb.install(gtk=True)

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
        # dialog = self.show_loading_spinner("Loading from API")
        asyncio.ensure_future(self.do_api_loading())

    def on_button2_clicked(self, widget):
        # dialog = self.show_loading_spinner("Loading from file")
        dialog = None
        asyncio.ensure_future(self.do_file_loading(dialog))

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

        dialog.show()
        spinner.start()

        return dialog

    async def do_api_loading(self):
        print("Loading from API")
        for i in range(100000000):
            pass
        # Здесь можно добавить код для загрузки данных из API
        print("API data loaded")

        dialog = self.show_loading_spinner("Processing data...")
        dialog.destroy()

    async def do_file_loading(self, dialog):
        dialog = self.show_loading_spinner("Processing data...")

        print("Loading from file")
        time.sleep(5)
        print("File data loaded")

        dialog.destroy()

win = MyWindow()
win.set_default_size(800, 600)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
