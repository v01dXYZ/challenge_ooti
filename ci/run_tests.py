#!/bin/env python3
import subprocess
import random

from run import run_ctx

port = random.randint(1 << 10, 1 << 16)

with run_ctx(port) as venv_bin:
    pytest = venv_bin / "pytest"

    subprocess.run(
        [pytest, "test_requests.py"],
        env={
            "DJANGO_SERVER_PORT": str(port),
        },
    )
