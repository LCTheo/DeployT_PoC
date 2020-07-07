import docker
from docker.models.containers import Container
from docker.models.networks import Network


class DockerContainer:

    def __init__(self):
        self.client = docker.from_env()

    def deploy(self, image, name, hostname, environment, labels, networks):
        if self.imageExist(image):
            try:
                self.client.containers.run(image, detach=True, name=name, hostname=hostname,
                                           environment=environment, labels=labels)
                for network in networks:
                    res, net = self.getNetwork(network)
                    if res == "0":
                        net.connect(name)
                return "0"
            except docker.errors.ContainerError:
                return "02002"
            except docker.errors.APIError:
                return "02001"
        else:
            return "02001"

    def imageExist(self, image):
        try:
            self.client.images.get(image)
            return "0"
        except docker.errors.APIError:
            return "02001"
        except docker.errors.ImageNotFound:
            return "02004"

    def deleteContainer(self, containerID):
        try:
            container = self.client.containers.get(containerID)
            container.remove(force=True)
            return "0"
        except docker.errors.NotFound:
            return "02005"
        except docker.errors.APIError:
            return "02001"

    def getContainer(self, containerID) -> (str, Container):
        try:
            container = self.client.containers.get(containerID)
            return "0", container
        except docker.errors.NotFound:
            return "02005", None
        except docker.errors.APIError:
            return "02001", None

    def createNetwork(self, networkId):
        try:
            self.client.networks.create(networkId, driver="bridge", attachable=True, internal=True, check_duplicate=True)
            return "0"
        except docker.errors.APIError:
            return "02001"

    def getNetwork(self, networkId) -> (str, Network):
        try:
            network = self.client.networks.get(networkId)
            return "0", network
        except docker.errors.APIError:
            return "02001", None
        except docker.errors.NotFound:
            return "02006", None

    def deleteNetwork(self, networkId):
        try:
            network = self.getNetwork(networkId)
            network[1].remove()
            return "0"
        except docker.errors.APIError:
            return "02001"
