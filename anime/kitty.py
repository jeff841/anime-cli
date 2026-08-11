import os
import subprocess

def show_image(path, x=60, y=2):
    fd = os.open("/dev/tty", os.O_WRONLY)
    os.write(
        fd,
        f"\033[{y};{x}H".encode()
    )
    subprocess.run(
        [
            "kitty",
            "+kitten",
            "icat",
            "--transfer-mode=stream",
            "--silent",
            str(path),
        ],
        stdout=fd,
    )
    os.close(fd)

def clear_image():
    fd = os.open("/dev/tty", os.O_WRONLY)
    os.write(
        fd,
        b"\033_Ga=d,d=A\033\\"
    )
    os.close(fd)
