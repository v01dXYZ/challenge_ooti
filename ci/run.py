#!/bin/env python3

import contextlib
import argparse

import subprocess
import tempfile
import logging
import pathlib

logging.basicConfig(level=logging.INFO)

ooti_root = pathlib.Path(__file__).parent.parent
manage_py = ooti_root / "manage.py"
packages_txt = ooti_root / "packages.txt"

superuser_name = "test"
superuser_password = "mypass" * 2


@contextlib.contextmanager
def run_ctx(port, terminate=True):
    with tempfile.TemporaryDirectory() as temp_dir:
        logging.info(f"temp_dir: {temp_dir}")
        venv_bin = pathlib.Path(temp_dir) / "venv" / "bin"
        activate = f". {venv_bin}/activate"
        python = venv_bin / "python"

        cmds = [
            f"python3 -m venv {temp_dir}/venv",
            activate,
            f"pip install -r {packages_txt}",
            f"{manage_py} makemigrations",
            f"{manage_py} migrate",
            f"DJANGO_SUPERUSER_PASSWORD={superuser_password} {manage_py} createsuperuser --noinput --username {superuser_name} --email none@localhost",
        ]
        subprocess.run(
            "\n".join(cmds),
            shell=True,
            cwd=temp_dir,
        )

        with subprocess.Popen(
            [
                python,
                manage_py,
                "runserver",
                str(port),
            ],
            cwd=temp_dir,
        ) as m:
            yield venv_bin

            if terminate:
                m.terminate()


def main():
    prs = argparse.ArgumentParser()
    prs.add_argument("port", type=int)
    args = prs.parse_args()
    port = args.port

    with run_ctx(port=port, terminate=False):
        pass


if __name__ == "__main__":
    main()
