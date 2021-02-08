from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from os import system

from kivy.uix.label import Label


class ReportScreen(GridLayout):
    cols = 1

    def __init__(self, results, **kwargs):
        super().__init__(**kwargs)
        self.results = results

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

        self.add_widget(Label(text="Click on any buttons above! :D", y=self.y / 10))

    def open_all_on_press(self, instance):
        for result in self.results:
            if result.current_link is not None:
                system("start " + result.current_link)


class AnimeNotifyApp(App):
    def __init__(self, results, **kwargs):
        super().__init__(**kwargs)
        self.results = results

    def build(self):
        return ReportScreen(self.results)
