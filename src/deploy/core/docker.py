import docker


class DockerClient:

    def __init__(self):
        self.client = docker.from_env()

    def deploy(self, image, options):
        self.client.images.list()
        container = self.client.containers.run(image, detach=True)
        return container
