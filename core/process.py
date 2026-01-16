import asyncio
import signal

class CommandProcess:
    def __init__(self, command: str):
        self.command = command
        self.process = None

    async def run(self, on_output):
        self.process = await asyncio.create_subprocess_shell(
            self.command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            preexec_fn=lambda: signal.signal(signal.SIGINT, signal.SIG_IGN)
        )

        while True:
            line = await self.process.stdout.readline()
            if not line:
                break
            on_output(line.decode(errors="ignore"))

        await self.process.wait()

    def stop(self):
        if self.process and self.process.returncode is None:
            try:
                self.process.terminate()
            except ProcessLookupError:
                pass
