class NmapModule:
    name = "nmap"

    def build(self, target, flags="-sCV -T4 -v"):
        return f"nmap {flags} {target}"
