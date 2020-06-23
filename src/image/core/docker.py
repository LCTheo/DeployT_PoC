import tempfile

import docker
from git import Repo


class DockerImage:

    def __init__(self):
        self.client = docker.from_env()

    def clone(self, repo, tag, dockerfilePath):
        d = tempfile.TemporaryDirectory(dir="/tmp")
        Repo.clone_from(repo, d.name)
        res = self.client.images.build(path=d.name, tag=tag, rm=True, nocache=True,
                                       dockerfile=dockerfilePath+"/Dockerfile")
        d.cleanup()
        return res
