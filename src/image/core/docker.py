import tempfile

import docker
from docker.models.images import Image
from git import Repo


class DockerImage:

    def __init__(self):
        self.client = docker.from_env()

    def build(self, repo, tag, dockerfilePath) -> (str, Image):
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
        try:
            self.client.images.remove(image=imageId)
            return "0"
        except docker.errors.APIError:
            return "03001"

    def pull(self, name) -> (str, Image):
        try:
            image = self.client.images.pull(name)
            return "0", image.id
        except docker.errors.APIError:
            return "03001", None