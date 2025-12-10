#!/bin/env python3
import subprocess
import tempfile
import random
import logging
import pathlib

logging.basicConfig(level=logging.INFO)

ooti_root = pathlib.Path(__file__).parent.parent
manage_py = ooti_root / "manage.py"
packages_txt = ooti_root / "packages.txt"

superuser_name = "test"
superuser_password = "mypass" * 2

random_port = random.randint(1 << 10, 1 << 16)

with tempfile.TemporaryDirectory() as temp_dir:
    logging.info(f"temp_dir: {temp_dir}")
    venv_bin = pathlib.Path(temp_dir) / "venv" / "bin"
    activate = f". {venv_bin}/activate"
    python = venv_bin / "python"
    pytest = venv_bin / "pytest"

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
            str(random_port),
        ],
        cwd=temp_dir,
    ) as m:
        subprocess.run(
            [pytest, "test_requests.py"],
            env={
                "DJANGO_SERVER_PORT": str(random_port),
            },
        )

        m.terminate()
