import docker


class DockerClient:

    def __init__(self):
        self.client = docker.from_env()

    def deploy(self, image, name, hostname, environment, labels, network):
        if self.imageExist(image):
            try:
                self.client.containers.run(image, detach=True, name=name, hostname=hostname,
                                           environment=environment, labels=labels, network=network)
                return True
            except (docker.errors.ContainerError, docker.errors.APIError):
                return False
        else:
            return False

    def imageExist(self, image):
        try:
            self.client.images.get(image)
            return True
        except (docker.errors.ImageNotFound, docker.errors.APIError):
            return False

    def deleteContainer(self, containerID):
        try:
            container = self.client.containers.get(containerID)
            container.remove(force=True)
            return 0
        except docker.errors.NotFound:
            return -1
        except docker.errors.APIError:
            return -1

    def getContainer(self, containerID):
        try:
            container = self.client.containers.get(containerID)
            return container
        except docker.errors.NotFound:
            return -1
        except docker.errors.APIError:
            return -1
