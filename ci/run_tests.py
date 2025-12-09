#!/bin/env python3
import subprocess
import tempfile
import random
import logging
import os
import pathlib

logging.basicConfig(level=logging.INFO)

ooti_root = pathlib.Path(__file__).parent.parent
manage_py = ooti_root / "manage.py"
packages_txt = ooti_root / "packages.txt"

random_port = random.randint(1 << 10, 1 << 16)
with tempfile.TemporaryDirectory() as temp_dir:
    logging.info(f"temp_dir: {temp_dir}")
    activate = f". {temp_dir}/venv/bin/activate"
    cmds = [
        f"python3 -m venv {temp_dir}/venv",
        activate,
        f"pip install -r {packages_txt}",
        f"{manage_py} makemigrations",
        f"{manage_py} migrate",
        f"DJANGO_SUPERUSER_PASSWORD=mypassmypass {manage_py} createsuperuser --noinput --username test --email none@localhost",
    ]
    subprocess.run(
        "\n".join(cmds),
        shell=True,
        cwd=temp_dir,
    )

    with subprocess.Popen(
        "\n".join([activate, f"{manage_py} runserver {random_port}"]),
        shell=True,
        cwd=temp_dir,
    ) as m:
        subprocess.run(
            "\n".join(
                [activate, f"DJANGO_SERVER_PORT={random_port} pytest test_requests.py"]
            ),
            shell=True,
        )

        m.terminate()
