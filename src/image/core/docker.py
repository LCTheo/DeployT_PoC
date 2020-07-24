import tempfile

import docker
from docker.models.images import Image
from git import Repo


class DockerImage:
    """a handling class for a docker client to manage image"""

    def __init__(self):
        self.client = docker.from_env()

    def build(self, repo: str, tag: str, dockerfilePath: str) -> (str, Image):
        """build an image based on a GitHub repository

        :returns the tuple (0, imageObject) if the image was created successfully or a tuple (errorCode, None) otherwise
        """

        d = tempfile.TemporaryDirectory(dir="/tmp")
        Repo.clone_from(repo, d.name)
        if dockerfilePath == '.':
            context = d.name
        else:
            context = d.name + "/" + dockerfilePath
        try:
            res = self.client.images.build(path=context, tag=tag, rm=True, nocache=True,
                                           dockerfile="./Dockerfile")
            d.cleanup()
            return "0", res[0]
        except docker.errors.APIError:
            return "03001", None
        except docker.errors.BuildError:
            return "03002", None
        except TypeError:
            return "03003", None

    def delete(self, imageId):
        """remove a image from the host

            :returns 0 if the image was removed successfully or an error code otherwise
        """
        try:
            self.client.images.remove(image=imageId)
            return "0"
        except docker.errors.APIError:
            return "03001"

    def pull(self, name) -> (str, Image):
        """pull a image from the official Docker registry

        :returns the tuple (0, imageId) if the image was pulled successfully or a tuple (errorCode, None) otherwise"""
        try:
            image = self.client.images.pull(name)
            return "0", image.id
        except docker.errors.APIError:
            return "03001", None