import psutil

pythons = [[" ".join(p.cmdline()), p.pid] for p in psutil.process_iter()
            if p.name().lower() in ("python.exe", "pythonw.exe")]

print(pythons)