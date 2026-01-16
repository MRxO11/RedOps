from textual.widgets import RichLog


class OutputPanel(RichLog):
    def on_mount(self):
        self.auto_scroll = True
        self.markup = True      
        self.highlight = False 
