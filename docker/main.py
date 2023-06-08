#!/usr/bin/env python
import subprocess
import json
import os

import click
import docker
from io import BytesIO
from docker.errors import BuildError, ImageNotFound, NotFound
from docker import APIClient
from pathlib import Path


@click.group()
def cli():
    pass


workspace_root = Path(__file__).parent.parent.resolve()
curr_dir = Path(__file__).parent.resolve()
docker_file_path = curr_dir / "Dockerfile"
shell_file_path = (curr_dir / "shell.sh").resolve()
image_name = "laygo2_sky130_docker"
container_name = "laygo2_sky130_container"
image_version = "0.0.1"


@cli.command()
def build():
    docker_api_cli = APIClient()
    print("Building docker image")
    with open(docker_file_path, "rb") as f:
        build_gen = docker_api_cli.build(
            path=str(workspace_root),
            dockerfile=str(docker_file_path),
            tag=image_name,
        )

        for line in build_gen:
            line = json.loads(line)
            if "stream" in line:
                print(line["stream"].strip())
    try:
        client = docker.from_env()
        # check if image exists
        img = client.images.get(image_name)
        # tag image with latest and the current version
        client.images.get(img.id).tag(f"{image_name}:latest")
        client.images.get(img.id).tag(f"{image_name}:{image_version}")
    except ImageNotFound:
        raise Exception("Image build failed")


@cli.command()
def run():
    client = docker.from_env()
    # check if container already running
    try:
        container = client.containers.get(container_name)
        if container.status == "running":
            print("Container already running")
            return
        elif container.status == "exited":
            container.start()
            print("Container restarted")
            return
        else:
            print("Container status: ", container.status)
            return
    except NotFound:
        container = None

    # check if image exists
    try:
        img = client.images.get(f"uduse/{image_name}:latest")
    except ImageNotFound:
        try:
            img = client.images.get(f"{image_name}:latest")
        except ImageNotFound:
            print("Image not found.")
            return

    print(f"Running docker container using {img.id}")
    # docker run -d -p 6080:80 -v /dev/shm:/dev/shm laygo2_sky130 --name laygo2_sky130_container
    client.containers.run(
        img.id,
        detach=True,
        ports={"80": "6080"},
        volumes={"/dev/shm": {"bind": "/dev/shm", "mode": "rw"}},
        name=container_name,
    )
    print("Docker container running")


@cli.command()
def shell():
    client = docker.from_env()
    container = client.containers.get(container_name)
    if container.status != "running":
        print("Container is not running")
        print("Starting container")
        run()
    else:
        command = f"docker exec -it {container_name} /bin/bash"
        os.execv("/usr/bin/docker", command.split(" "))


@cli.command()
def stop():
    client = docker.from_env()
    container = client.containers.get(container_name)
    if container.status != "running":
        print("Container is not running")
        return
    container.stop()
    print("Container stopped")


if __name__ == "__main__":
    cli()
    # shell()
