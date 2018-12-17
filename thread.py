from threading import Thread as BaseThread

class Thread(BaseThread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.daemon)
        self.daemon = True