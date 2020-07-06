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
        try:
            res = self.client.images.build(path=d.name, tag=tag, rm=True, nocache=True,
                                           dockerfile=dockerfilePath + "/Dockerfile")
            d.cleanup()
            return "0", res[0]
        except docker.errors.APIError:
            return "04001", None
        except docker.errors.BuildError:
            return "04002", None
        except TypeError:
            return "04003", None

    def delete(self, imageId):
        try:
            self.client.images.remove(image=imageId)
            return "0"
        except docker.errors.APIError:
            return "04001"
