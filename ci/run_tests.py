#!/bin/env python3
import subprocess
import tempfile
import random
import logging
import os

logging.basicConfig(level=logging.INFO)

random_port = random.randint(1 << 10, 1 << 16)
with tempfile.TemporaryDirectory() as temp_dir:
    logging.info(f"temp_dir: {temp_dir}")
    activate = f". {temp_dir}/bin/activate"
    cmds = [
        f"python3 -m venv {temp_dir}/",
        activate,
        "pip install -r packages.txt",
        "./manage.py makemigrations",
        "./manage.py migrate",
    ]
    subprocess.run(
        "\n".join(cmds),
        shell=True,
    )

    with subprocess.Popen(
        "\n".join([activate, f"./manage.py runserver {random_port}"]),
        shell=True,
    ) as m:
        subprocess.run(
            "\n".join(
                [activate, f"DJANGO_SERVER_PORT={random_port} pytest test_requests.py"]
            ),
            shell=True,
        )

        m.kill()
