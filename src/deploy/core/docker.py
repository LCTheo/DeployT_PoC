from typing import List

import docker
from docker.models.containers import Container
from docker.models.networks import Network


class DockerContainer:
    """a handling class for a docker client to manage container and network"""

    def __init__(self):
        self.client = docker.from_env()

    def deploy(self, image: str, name: str, hostname: str, environment: List[str], labels: List[str], networks: List[str]):
        """deploy a container on the host with the passed argument

            :returns 0 if the container was deployed successfully or an error code otherwise
        """
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

    def imageExist(self, image: str):
        """check if the passed image exist or not

            :returns 0 if the image exist or an error code otherwise
        """
        try:
            self.client.images.get(image)
            return "0"
        except docker.errors.APIError:
            return "02001"
        except docker.errors.ImageNotFound:
            return "02004"

    def deleteContainer(self, containerID):
        """remove a container from the host

            :returns 0 if the container was removed successfully or an error code otherwise
        """
        try:
            container = self.client.containers.get(containerID)
            container.remove(force=True)
            return "0"
        except docker.errors.NotFound:
            return "02005"
        except docker.errors.APIError:
            return "02001"

    def getContainer(self, containerID) -> (str, Container):
        """return the container object corresponding to the Id if it exist

            :returns the tuple (0, containerObject) if the container exist or an tuple (errorCode, None) otherwise
        """
        try:
            container = self.client.containers.get(containerID)
            return "0", container
        except docker.errors.NotFound:
            return "02005", None
        except docker.errors.APIError:
            return "02001", None

    def createNetwork(self, networkId):
        """create a network for container on the host

            :returns 0 if the network was created successfully or an error code otherwise
        """
        try:
            self.client.networks.create(networkId, driver="bridge", attachable=True, internal=True, check_duplicate=True)
            return "0"
        except docker.errors.APIError:
            return "02001"

    def getNetwork(self, networkId) -> (str, Network):
        """return the network object corresponding to the Id if it exist

            :returns the tuple (0, networkObject) if the network exist or a tuple (errorCode, None) otherwise
        """
        try:
            network = self.client.networks.get(networkId)
            return "0", network
        except docker.errors.APIError:
            return "02001", None
        except docker.errors.NotFound:
            return "02006", None

    def deleteNetwork(self, networkId):
        """remove a network from the host

            :returns 0 if the network was removed successfully or an error code otherwise
        """
        try:
            network = self.getNetwork(networkId)
            network[1].remove()
            return "0"
        except docker.errors.APIError:
            return "02001"
