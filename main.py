import csv

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

import asyncio
import gbulb.gtk

gbulb.install(gtk=True)


class CustomListBox(Gtk.ListBox):
    def __init__(self):
        super().__init__()
        self.connect("scroll-event", self.on_scroll_event)

    def on_scroll_event(self, widget, event):
        # Handle scrolling with the mouse wheel
        if event.direction == Gdk.ScrollDirection.UP:
            self.get_adjustment().step_increment(-1)
        elif event.direction == Gdk.ScrollDirection.DOWN:
            self.get_adjustment().step_increment(1)


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super().__init__()
        self.data = " | ".join(data)
        self.add(Gtk.Label(label=data, xalign=0.0))


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

        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.EXTERNAL, Gtk.PolicyType.EXTERNAL)
        self.scrolled_window.set_kinetic_scrolling(True)

        self.list_box = CustomListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.NONE)
        self.scrolled_window.add(self.list_box)



    def on_button1_clicked(self, widget):
        dialog = self.show_loading_spinner("Loading from API")
        asyncio.gather(self.do_api_loading(dialog))

    def on_button2_clicked(self, widget):
        dialog = self.show_loading_spinner("Loading from file")
        asyncio.gather(self.do_file_loading(dialog))

    async def do_api_loading(self, dialog):
        print("Loading from API")
        await asyncio.sleep(1)
        data = [("Product 1", 10.99), ("Product 2", 25.50), ("Product 3", 5.75)]
        self.update_list_box(data, dialog)


    async def do_file_loading(self, dialog):
        print("Loading from file")
        await asyncio.sleep(0.5)
        with open("base.csv", newline="", encoding="utf-8") as file:
            rows = csv.reader(file)
            rows = list(rows)
        self.update_list_box(rows, dialog)
        print("updated")



    def update_list_box(self, rows, dialog):
        for row in rows:
            self.list_box.add(ListBoxRowWithData(row[1:]))
        dialog.destroy()
        self.button1.set_visible(False)
        self.button2.set_visible(False)
        self.box.pack_start(self.scrolled_window, True, True, 0)
        self.scrolled_window.show_all()



    def show_loading_spinner(self, message):
        dialog = Gtk.Dialog(
            title=message,
            parent=self,
            flags=0,
        )

        dialog.set_default_size(300, 150)

        spinner = Gtk.Spinner()
        dialog.vbox.pack_start(spinner, True, True, 0)
        spinner.show()

        dialog.set_transient_for(self)
        dialog.set_modal(True)

        dialog.show()
        spinner.start()

        return dialog


if __name__ == "__main__":
    asyncio.set_event_loop_policy(gbulb.gtk.GtkEventLoopPolicy())
    window = MyWindow()
    window.set_default_size(800, 600)
    window.connect("destroy", lambda *args: loop.stop())
    window.show_all()

    loop = asyncio.get_event_loop()
    loop.run_forever()
