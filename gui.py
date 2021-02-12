from os import system, environ

environ["KIVY_NO_CONSOLELOG"] = "1"  # to hide kivy debug info

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from constants import info_file


class AddScreen(GridLayout):
    url = ObjectProperty()
    title = ObjectProperty()
    warning = ObjectProperty()

    def warn(self, message=""):
        self.warning.text = message

    def addx(self):
        if self.url.text and self.title.text:
            with open(info_file, 'a') as f:
                f.write(f"{self.url.text},{self.title.text},\n")
            self.url.text = ""
            self.warn("Added " + self.title.text + "!")
            self.title.text = ""
        elif self.url.text:
            self.warn("add title!")
            self.title.focus = True
        elif self.title.text:
            self.warn("add url!")
            self.url.focus = True
        else:
            self.warn("add url and title!")
            self.url.focus = True


class AddApp(App):
    def build(self):
        return AddScreen()


class ReportScreen(GridLayout):
    cols = 1

    def __init__(self, results, **kwargs):
        super().__init__(**kwargs)
        self.results = results

        if len(results) > 1:
            # add open all button
            open_all_btn = Button(text="open all")
            open_all_btn.text_size = (100, 100)
            open_all_btn.height = 20
            open_all_btn.bind(on_press=self.open_all_on_press)
            self.add_widget(open_all_btn)

        # add GridLayout Label and button for each title
        titles_grid = GridLayout(cols=2)
        for result in self.results:
            btn_id = result.current_link
            title_btn = Button(text=result.title)
            title_btn.id = btn_id
            title_btn.bind(on_press=lambda btn: system(
                "start " + btn.id))
            titles_grid.add_widget(title_btn)

            ep_btn = Button(
                text=f"ep {result.old_ep} -> {result.current_ep}")
            ep_btn.id = btn_id
            ep_btn.bind(on_press=lambda btn: system("start " + btn.id))
            titles_grid.add_widget(ep_btn)
        self.add_widget(titles_grid)

        self.add_widget(
            Label(text="Click on any buttons above! :D", y=self.y / 10))

    def open_all_on_press(self, instance):
        for result in self.results:
            system("start " + result.current_link)


class ReportApp(App):
    def __init__(self, results, **kwargs):
        super().__init__(**kwargs)
        self.results = results

    def build(self):
        return ReportScreen(self.results)


if __name__ == "__main__":
    pass
