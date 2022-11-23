#!/usr/bin/env python
import subprocess
import json
import os

import click
import docker
from io import BytesIO
from docker.errors import BuildError
from docker import APIClient
from pathlib import Path


@click.group()
def cli():
    pass


workspace_root = Path(__file__).parent.parent.resolve()
curr_dir = Path(__file__).parent.resolve()
docker_file_path = curr_dir / "Dockerfile"
shell_file_path = (curr_dir / "shell.sh").resolve()


@cli.command()
def build():
    docker_api_cli = APIClient()
    print("Building docker image")
    with open(docker_file_path, "rb") as f:
        build_gen = docker_api_cli.build(
            path=str(workspace_root),
            dockerfile=str(docker_file_path),
            tag="laygo2_sky130",
        )

        for line in build_gen:
            line = json.loads(line)
            if "stream" in line:
                print(line["stream"].strip())
    print("Docker image built")


@cli.command()
def run():
    client = docker.from_env()
    # docker run -d -p 6080:80 -v /dev/shm:/dev/shm laygo2_sky130 --name laygo2_sky130_container
    client.containers.run(
        "laygo2_sky130",
        detach=True,
        ports={"80": "6080"},
        volumes={"/dev/shm": {"bind": "/dev/shm", "mode": "rw"}},
        name="laygo2_sky130_container",
    )
    print("Docker container running")


@cli.command()
def shell():
    client = docker.from_env()
    container = client.containers.get("laygo2_sky130_container")
    if container.status != "running":
        print("Container is not running")
        print("Starting container")
        run()
    else:
        command = "docker exec -it laygo2_sky130_container /bin/bash"
        os.execv('/usr/bin/docker', command.split(" "))


if __name__ == "__main__":
    cli()
    # shell()
