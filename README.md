# Container Basics Training

## 1. Prerequisites & Setup

### Install Docker Desktop
* **Windows**: [Download here](https://docs.docker.com/desktop/install/windows-install/). Ensure WSL 2 (Windows Subsystem for Linux) is selected during installation for better performance.
* **Mac**: [Download here](https://docs.docker.com/desktop/install/mac-install/). Choose the correct chip version (Intel vs. Apple Silicon/M1/M2/M3).

### Create a Docker Hub Account
Docker Hub is a registry where container images are stored.
1.  Go to [hub.docker.com](https://hub.docker.com/).
2.  Sign up for a free account.
3.  Note your `username`; you will need it to push images later.

---

## 2. Why Containers?
Before containers, applications were often deployed on **Virtual Machines (VMs)**.
* **VMs** are heavy: They include a full Guest OS (GBs in size) and take minutes to boot.
* **Containers** are light: They share the Host OS kernel, are MBs in size, and start in milliseconds.

**Why they became popular:**
* **Portability**: "It works on my machine" is solved. If it runs in a container, it runs anywhere.
* **Efficiency**: You can pack many more containers onto a server than VMs.
* **Isolation**: Apps are isolated from one another, preventing conflicts (e.g., App A needs Python 2, App B needs Python 3).

---

## 3. What is a Container *Really*?
A container is not a real physical object; it is a set of Linux kernel features working together to create an isolated environment.

1.  **Namespaces (Isolation)**: These deceive the process into thinking it has its own dedicated computer.
    * *PID Namespace*: The process thinks it is PID 1 (the only process).
    * *Network Namespace*: The process sees its own IP address and ports.
    * *Mount Namespace*: The process sees its own file system.
2.  **Control Groups / cgroups (Limits)**: These limit how much CPU and Memory the container can use. This prevents one container from crashing the whole server.
3.  **Union Filesystem (Storage)**: This allows images to be built in layers. If you change one file, Docker only saves that specific layer, not the whole OS again.

---

## 4. The Container Image
An **Image** is a read-only template used to create a container. It contains:
* The Application Code
* The Runtime (e.g., Python, Node.js, Java)
* System Libraries
* Environment Variables

Think of the **Image** as the "cookie cutter" and the **Container** as the "cookie."

---

## 5. Basic Dockerfile Syntax
A `Dockerfile` is a text document that contains all the commands to assemble an image.

| Instruction | Description |
| :--- | :--- |
| `FROM` | The base layer (OS or Runtime) to start with (e.g., `python:3.9-slim`). |
| `WORKDIR` | Sets the working directory inside the container (like `cd`). |
| `COPY` | Copies files from your computer into the container. |
| `RUN` | Runs a command *during the build process* (e.g., `pip install`). |
| `ENV` | Sets environment variables (e.g., `ENV PORT=8080`). |
| `EXPOSE` | Documentation that tells users which port the app listens on. |
| `CMD` | The command the container runs when it starts. |

---

## 6. Docker Commands Cheat Sheet
[Official Docker Cheat Sheet PDF](https://docs.docker.com/get-started/docker_cheatsheet.pdf)

### Build & Manage Images
* `docker build -t <name> .` : Build an image from the Dockerfile in the current directory.
* `docker images` : List all local images.
* `docker rmi <image_id>` : Delete an image.
* `docker tag <source> <target>` : Rename/retag an image.

### Run Containers
* `docker run -p 8080:80 <image>` : Run an image mapping host port 8080 to container port 80.
* `docker run -d <image>` : Run in "detached" mode (background).
* `docker run -e MY_VAR=hello <image>` : Pass an environment variable.
* `docker ps` : List running containers.
* `docker ps -a` : List all containers (including stopped ones).

### Inspect & Debug
* `docker logs <container_id>` : View the output logs of a container.
* `docker exec -it <container_id> /bin/sh` : Open a shell terminal *inside* the running container.
* `docker inspect <container_id>` : View detailed JSON metadata (IP, mounts, etc).
* `docker stop <container_id>` : Gracefully stop a container.

### Registry (Sharing)
* `docker login` : Authenticate with Docker Hub.
* `docker push <user>/<image>:<tag>` : Upload an image.
* `docker pull <user>/<image>:<tag>` : Download an image.

---

## 7. Hands-on Lab

### Step 1: Examine the Code
Navigate to the `/app` folder. We have a simple Python web server that is designed for Kubernetes (it reads configuration from the environment).

### Step 2: Build the Image
Run this from the root of the repo:
```bash
docker build -t my-python-app:v1 ./app
