import os
import tempfile
import yaml
import requests
import core
from typing import List, Dict
from git import Repo
from namespaces.models import Project, Image, Container, Network, User, EntryPoint


def addImage(projectId: str, name: str, repository_URL: str, repo_visibility: str, config_file_path: str) -> [str, str]:
    """create an image from a Github repository and add it to database"""

    project = Project.objects(id=projectId).first()
    imageTag = projectId + '-' + name + ':latest'
    code, imageAddress = core.getService("image")

    if code == "0":
        response = requests.post(
            'http://' + imageAddress + ':5000/image/build',
            json={'repository_URL': repository_URL,
                  'repo_visibility': repo_visibility,
                  'image_tag': imageTag,
                  'config_file_path': config_file_path})

        if response.status_code == 200:
            imageID = response.json().get('image')
            image = Image(imageId=imageID, owner=project.owner, repository_url=repository_URL,
                          repository_type=repo_visibility, image_tag=imageTag,
                          config_file_path=config_file_path)
            image.save()
            return "0", imageID
        else:
            return "03X" + response.json()['code'], ""
    else:
        return "01001", ""


def addPublicImage(imageTag: str) -> (str, str):
    """pull an image from official Docker registry and add it to database"""

    code, imageAddress = core.getService("image")
    if code == "0":
        response = requests.post('http://' + imageAddress + ':5000/image/pull',
                                 json={'image_tag': imageTag})
        if response.status_code == 200:
            imageID = response.json().get('image')
            image = Image(imageId=imageID, image_tag=imageTag)
            image.save()
            return "0", imageID
        else:
            return "03X" + response.json()['code'], ""
    else:
        return "01001", ""


def addContainer(projectId: str, name: str, imageId: str, environment: List[str], networks: List[str],
                 exposedPort: List[int] = None) -> str:
    """add a container and all these option to database"""

    project = Project.objects(id=projectId).first()
    image = Image.objects(imageId=imageId).first()
    if project:
        if name in project.containers:
            return "04004"
        if not image:
            return "04007"
        code, deployAddress = core.getService("deploy")
        if code == "0":
            for network in networks:
                if network not in project.networks:
                    networkId = projectId + '-' + network
                    responseDep = requests.post(
                        'http://' + deployAddress + ':5000/network/' + networkId)
                    if responseDep.status_code == 200:
                        project.networks[network] = Network(networkId=networkId)
                        project.save()

            if exposedPort:
                entryPoint = []
                for port in exposedPort:
                    dns = projectId + '-' + name + str(port)
                    entryPoint.append(EntryPoint(port=port, dns_prefix=dns))
                container = Container(containerId=projectId + '-' + name, imageId=imageId, environment=environment,
                                      network=networks, entryPoints=entryPoint)
            else:
                container = Container(containerId=projectId + '-' + name, imageId=imageId, environment=environment,
                                      network=networks)

            project.containers[name] = container
            project.save()
            return "0"
        else:
            return "01001"
    else:
        return "04001"


def deleteProject(projectId: str) -> str:
    """delete a project and all object related to it from database and host"""

    project = Project.objects(id=projectId).first()
    res = deleteContainer(projectId, [])
    if res != "0":
        return res
    project.delete()
    return "0"


def deleteContainer(projectId: str, containers: List[str]) -> str:
    """remove a list of container from host and delete it from database"""

    project = Project.objects(id=projectId).first()
    if project:
        code, deployAddress = core.getService("deploy")
        if code == "0":
            if len(containers) == 0:
                for key in project.containers:
                    containers.append(key)
            for containerName in containers:
                container = project.containers[containerName]
                if container:
                    if container.status == "running":
                        responseDep = requests.delete(
                            'http://' + deployAddress + ':5000/manage/' + container.containerId)
                        if responseDep.status_code != 200:
                            return "02X" + responseDep.json()['code']
                    code, imageAddress = core.getService("image")
                    if code == "0":
                        response = requests.delete('http://' + imageAddress + ':5000/image/build',
                                                   json={'id': container.imageId})
                        if response.status_code == 200:
                            image = Image.objects(imageId=container.imageId).first()

                            project.update(**{'unset__containers__' + containerName: 1})
                            if image.owner is not None:
                                image.delete()
                            project.save()
                        else:
                            return "04X" + response.json()['code']
                    else:
                        return "01001"
                else:
                    return "04003"
            project.reload()
            networks = []
            for network in project.networks:
                networks.append(network)
            for network in project.networks:
                for key, cont in project.containers.items():
                    if network in cont.network and network in networks:
                        networks.remove(network)
            for network in networks:
                requests.delete('http://' + deployAddress + ':5000/network/' + project.networks[network].networkId)
                project.update(**{'unset__networks__' + network: 1})
        else:
            return "01001"
    else:
        return "04001"
    return "0"


def getProjectId(name: str, owner: str) -> str:
    """get a project id based on is name and is owner"""

    user = User.objects(username=owner).first()
    if user:
        project = Project.objects(name=name, owner=user.id).first()
        if project:
            return str(project.id)
        else:
            return ""
    else:
        return ""


def containerStatus(projectId: str, containers: List[str], action: str) -> str:
    """change the status of a list of container form stopped to running or from running to stopped"""

    project = Project.objects(id=projectId).first()
    if project:
        code, deployAddress = core.getService("deploy")
        if code == "0":
            if len(containers) == 0:
                for key in project.containers:
                    containers.append(key)
            for containerName in containers:
                container = project.containers[containerName]
                if container:
                    if action == "start":
                        if container.status == "stopped":
                            netid = []
                            labels = []
                            for network in container.network:
                                netid.append(project.networks[network].networkId)
                            if len(container.entryPoints) != 0:
                                netid.append('proxy')
                                labels = redactLabels(container)
                            response = requests.post(
                                'http://' + deployAddress + ':5000/deployment/' + container.imageId,
                                json={'name': container.containerId,
                                      'hostname': containerName,
                                      'environment': container.environment,
                                      'network': netid,
                                      'labels': labels})
                            if response.status_code == 200:
                                container.status = 'running'
                            else:
                                return "02X" + response.json()['code']
                    elif action == "stop":
                        if container.status == "running":
                            response = requests.delete(
                                'http://' + deployAddress + ':5000/manage/' + container.containerId)
                            if response.status_code == 200:
                                container.status = 'stopped'
                    else:
                        return "03005"
                    project.save()
        else:
            return "01001"
    else:
        return "03001"
    return "0"


def validateURL(URL: str) -> str:
    """verify if the given URL is a valid git repository URL"""

    rep = requests.get(URL)
    if rep.status_code == 200:
        return "0"
    else:
        return "03006"


def extractConfigFile(repository_URL: str, repo_visibility: str, config_file_path: str) -> [str, Dict]:
    """extract the content of a docker-compose file given in a repository"""

    if repo_visibility == "public":
        d = tempfile.TemporaryDirectory(dir="/tmp")
        Repo.clone_from(repository_URL, d.name)
        if config_file_path == ".":
            path = d.name
        else:
            path = d.name + "/" + config_file_path
        if os.path.isfile(path + "/docker-compose.yml"):
            with open(path + "/docker-compose.yml") as f:
                config = yaml.load(f, Loader=yaml.FullLoader)
        else:
            return "03008", {}
        return "0", config


def redactContainer(config: Dict, projectId: str, configType: str, repo_URL: str = None) -> [str, List]:
    """add containers to the database based on a configFile"""

    containerList = []
    if 'networks' in config:
        defaultNetwork = False
    else:
        defaultNetwork = True
    for key in config['services']:
        container = config['services'][key]
        setting = [key]
        if 'image' in container:
            if type(container['image']) is str:
                setting.append(container['image'])
            else:
                return "001" + key
        elif 'build' in container:
            if type(container['build']) is dict:
                if 'context' in container['build']:
                    if 'repository' in container['build']:
                        setting.append([container['build']['context'], container['build']['repository']])
                    else:
                        setting.append([container['build']['context']])
                else:
                    return "002" + key
            else:
                setting.append([container['build']])
        else:
            return "004" + key

        if 'environment' in container:
            if type(container['environment']) is dict:
                env = []
                for varName in container['environment']:
                    env.append(varName + '=' + container['environment'][varName])
                setting.append(env)
            elif type(container['environment']) is list:
                setting.append(container['environment'])
            else:

                setting.append([])
        else:
            setting.append([])

        if 'networks' in container:
            if type(container['networks']) is list:
                setting.append(container['networks'])
            else:
                if defaultNetwork:
                    setting.append(['default'])
                else:
                    setting.append([])
        else:
            if defaultNetwork:
                setting.append(['default'])
            else:
                setting.append([])

        if 'ports' in container:
            if type(container['ports']) is list:
                ports = []
                for port in container['ports']:
                    host, inter = port.split(":")
                    ports.append(inter)
                setting.append(ports)
            else:
                setting.append([])
        else:
            setting.append([])

        containerList.append(setting)
    for containerConfig in containerList:
        if type(containerConfig[1]) is list:
            if configType == "compose":
                code, image = addImage(projectId, containerConfig[0], repo_URL, "public", containerConfig[1][0])
                if code == "0":
                    rep = addContainer(projectId, containerConfig[0], image, containerConfig[2], containerConfig[3],
                                       containerConfig[4])
                    if rep != "0":
                        return rep
                else:
                    return code
        else:
            image = Image.objects(image_tag=containerConfig[1], owner=None).first()
            if image:
                imageId = image.imageId
            else:
                code, imageId = addPublicImage(containerConfig[1])
                if code != "0":
                    return code
            rep = addContainer(projectId, containerConfig[0], imageId, containerConfig[2],
                               containerConfig[3], containerConfig[4])
            if rep != "0":
                return rep
    return "0"


def redactLabels(container: Container):
    """create a list of labels for the Traefik service to expose the given container"""
    DNSRecord = os.getenv('DNSRecord')
    labels = ['traefik.enable:true']
    for entryPoint in container.entryPoints:
        labels.append('traefik.http.routers.' + entryPoint.dns_prefix + '.rule:Host(`' + entryPoint.dns_prefix + '.' +
                      DNSRecord + '`)')
        labels.append('traefik.http.routers.' + entryPoint.dns_prefix + '.entrypoints:http')
        labels.append(
            'traefik.http.routers.' + entryPoint.dns_prefix + '.service:' + entryPoint.dns_prefix + '-service')
        labels.append('traefik.http.routers.' + entryPoint.dns_prefix + '-service.loadbalancer.server.port'
                      + str(entryPoint.port))
    return labels


def containerInfo(projectId: str, containers: List[str]) -> (str, Dict):
    project = Project.objects(id=projectId).first()
    if project:
        if len(containers) == 0:
            for key in project.containers:
                containers.append(key)
        Infos = {}
        for containerName in containers:
            contInfo = {}
            container = project.containers[containerName]
            image = Image.objects(imageId=container.imageId).first()
            if image.owner is None:
                image = {'type': 'public', 'image': image.image_tag}
            else:
                image = {'type': 'custom', 'base_repo': image.repository_url,
                         'config_file_path': image.config_file_path}
            contInfo['image'] = image
            envVar = []
            for var in container.environment:
                envVar.append(str(var))
            contInfo['environment_variable'] = envVar
            networks = []
            for network in container.network:
                networks.append(str(network))
            contInfo['networks'] = networks
            entryPoints = []
            DNSRecord = os.getenv('DNSRecord')
            for entryPoint in container.entryPoints:
                entryPoints.append([str(entryPoint.port), str(entryPoint.dns_prefix + DNSRecord)])
            contInfo['entryPoints'] = entryPoints
            contInfo['status'] = container.status
            Infos[containerName] = contInfo
        return "0", Infos
    else:
        return "04001", {}


def projectInfo(username: str) -> (str, List[str]):
    owner = User.objects(username=username).first()
    if owner:
        projects = Project.objects(owner=owner)
        Info = []
        for project in projects:
            Info.append(project.name)

        return "0", Info
    else:
        return "04008", []
