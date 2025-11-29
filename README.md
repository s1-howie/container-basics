# Container Basics Training

## 1. Prerequisites & Setup

### Install Docker Desktop
* **Windows**: [Download here](https://docs.docker.com/desktop/install/windows-install/). Ensure WSL 2 (Windows Subsystem for Linux) is selected during installation for better performance.
* **Mac**: [Download here](https://docs.docker.com/desktop/install/mac-install/). Choose the correct chip version (Intel vs. Apple Silicon).

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
* **Microservices**:  Break larger applications up into smaller services. Each service/container can be updated independently


---

## 3. What is a Container *Really*?
A container is a kind of virtualization made possible via Linux kernel features working together to create an isolated environment.

1.  **Namespaces (Isolation)**: These trick the process into thinking it is running on its own host machine.
    * *PID (process ID) Namespace*: Gives each container its own isolated process tree (with its own PID 1).  On Linux, PID 1 is the very first process that starts and manages everything else.
    * *NET (network) Namespace*: Gives each container its own isolated network stack.
    * *MNT (mount) Namespace*: Gives each container its own isolated root filesystem.
    * *IPC (inter-process communication) Namespace*: Lets processes in the same container share memory 
    * *UTS (unix time-sharing) Namespace*: Gives  each container its own hostname (doesn't really have to do with time despite the name)
    * *USER  Namespace*: Lets you map user accounts in the container to different user accounts on the underlying host (ie: mapping the container's root user to a non-privileged user on the host).

2.  **Control Groups / cgroups (Limits)**: These limit how much CPU and Memory the container can use. This prevents one container from crashing the whole server.
3.  **Union Filesystem (Storage)**: Allows llow containers to stack multiple read-only image layers into a single unified view, enabling efficient storage by sharing common data across different containers. This architecture relies on a "copy-on-write" mechanism, where any modifications made by the running container are written to a thin, disposable top layer without altering the original underlying image.

---

## 4. The Container Image
An **Image** is a read-only template used to create a container. It contains:
* The Application Code
* The Runtime (e.g., Python, Node.js, Java)
* System Libraries and Dependencies
* Environment Variables

Think of the **Image** as the "cookie cutter" and the **Container** as the "cookie."

---

## 5. Basic Dockerfile Syntax
A `Dockerfile` is a text document that contains all the commands to assemble an image.
[Official Dockerfile reference](https://docs.docker.com/reference/dockerfile/)

| Instruction | Description |
| :--- | :--- |
| `FROM` | The base layer (OS or Runtime) to start with (e.g., `python:3.9-slim`). |
| `WORKDIR` | Sets the working directory inside the container (like `cd`). |
| `COPY` | Copies files from your computer into the container. |
| `RUN` | Runs a command *during the build process* (e.g., `pip install`). |
| `ENV` | Sets environment variables (e.g., `ENV PORT=8080`). |
| `EXPOSE` | Documentation that tells users which port the app listens on. |
| `CMD` | The command that runs if no arguments are passed after the image name. If arguments ARE added after the image name, the CMD is completely ignored and replaced by the user's arguments. |
| `ENTRYPOINT` | The command specified in ENTRYPOINT runs no matter what. If a user passes arguments to docker run, they are appended to the end of the ENTRYPOINT command rather than replacing it. |

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
```

### Step 3: Create a Container from the Image
This will create/run a container named "webserver" from our my-python-app:v1 image.  "--rm" will cause our image to be removed if it is stopped.  Port 8080 on the host will forward to port 5000 in the container.
```bash
docker run -d --name webserver --rm -p 8080:5000 my-python-app:v1
```

### Step 4: List running containers
```bash
docker ps
```

### Step 4: Open a web browser to view your webserver
Click or Copy/Paste this link: [http://localhost:8080](http://localhost:8080)

Was the value of the "message" key what you expected?

The value of APP_MESSAGE was actually set within our Dockerfile.

### Step 5: Stop the webserver container
```bash
docker ps
docker stop webserver
```

### Step 6: Start the webserver again, but specify an environment variable on the command line
```bash
docker run -d --name webserver --rm -p 8080:5000 -e APP_MESSAGE="foo" my-python-app:v1
```

### Step 7: Refresh your browser tab
Notice that the value of the "message" key is now "foo".  Environment variables passed as arguments "win" over values specified via ENV in Dockerfiles.

### Step 8: Stop your webserver
```bash
docker stop webserver
```

### Step 9: Tag and push your image to Docker Hub
Be sure to use your DockerHub Username as the value for the MY_DOCKERHUB_USERNAME variable below!!!
```bash
MY_DOCKERHUB_USERNAME=<specify-your-dockerhub-username-here>
docker tag my-python-app:v1 $MY_DOCKERHUB_USERNAME/my-python-app:v1
docker push $MY_DOCKERHUB_USERNAME/my-python-app:v1
```

### Step 9: Run the image from Docker Hub
```bash
docker run -d --name webserver --rm -p 8080:5000 -e APP_MESSAGE="foo" $MY_DOCKERHUB_USERNAME/my-python-app:v1
```

### Step 10: List the running containers
Notice that the IMAGE is sourcing from Docker Hub (and NOT from your local, docker repository).

AWESOME!  Now you can share it with your friends!! :D

### Step 11: Stop your webserver
```bash
docker stop webserver
```

### Step 12: Edit your Dockerfile
Since our main.py file specifies default values for APP_PORT and APP_MESSAGE, let's remove those values from our Dockerfile by commenting them out.

\# 5. Environment: Set default environment variables (can be overridden at runtime)
\# ENV APP_PORT=5000
\# ENV APP_MESSAGE="Default Message"

Be sure to save your changes!!

### Step 13: Re-build your Image
We can go ahead and tag it for usage with DockerHub.
We'll specify a tag of "v2"
```bash
docker build -t $MY_DOCKERHUB_USERNAME/my-python-app:v2 ./app
```

### Step 14: Push your v2 image to Docker Hub
```bash
docker push $MY_DOCKERHUB_USERNAME/my-python-app:v2
```

### Step 15: Run the v2 image
Be sure to use the "v2" tag and don't pass any environment variables via arguments this time.
```bash
docker run -d --name webserver --rm -p 8080:5000 $MY_DOCKERHUB_USERNAME/my-python-app:v2
```
Refresh your browser and notice that we're now seeing the default APP_MESSAGE value from main.py.

Of course, you can still override that with -e APP_MESSAGE="foo" or any other value you choose.
