from core.process import CommandProcess

class Engine:
    def __init__(self):
        self.tasks = []
        self.current = None

    async def run(self, command, callback):
        proc = CommandProcess(command)
        self.current = proc
        self.tasks.append(proc)
        await proc.run(callback)
        self.current = None

    def stop_current(self):
        if self.current:
            self.current.stop()
            return True
        return False
