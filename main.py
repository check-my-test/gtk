import csv
import gi
import httpx

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import asyncio
import gbulb.gtk

gbulb.install(gtk=True)


class ListBoxRowWithData(Gtk.ListBoxRow):
    def __init__(self, data):
        super().__init__()
        self.data = " ".join(data)
        self.add(Gtk.Label(label=self.data))


async def request_to_api(request_id, url):
    async with httpx.AsyncClient() as client:
        data = await client.get(url)
        if data.status_code != 200:
            data = {}
        return request_id, data.json()


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
        self.scrolled_window.set_policy(
            Gtk.PolicyType.EXTERNAL, Gtk.PolicyType.EXTERNAL
        )
        self.scrolled_window.set_kinetic_scrolling(True)

        self.list_box = Gtk.ListBox()
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
        coros = []
        for num in range(1, 3):
            url = f"https://paycon.su/api{num}.php"
            coros.append(request_to_api(num, url))
        responses = await asyncio.gather(*coros)
        result_data = []
        for request_id, response_data in sorted(responses):
            result_data.extend(response_data)
        columns = ["name", "price"]
        rows = [[str(item.get(column)) for column in columns] for item in result_data]
        self.update_list_box(data=rows, dialog=dialog)

    async def do_file_loading(self, dialog):
        print("Loading from file")
        await asyncio.sleep(0.5)  # Имитация долгой загрузки
        with open("base.csv", newline="", encoding="utf-8") as file:
            rows = csv.reader(file)
            rows = list(rows)[1:]
        rows = [row[1:3] for row in rows]
        self.update_list_box(data=rows, dialog=dialog)
        print("updated")

    def update_list_box(self, data, dialog):
        for row in data:
            self.list_box.add(ListBoxRowWithData(row))
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
