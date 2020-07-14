import os
import tempfile
from typing import List, Dict

import yaml
from git import Repo
import requests

import core
from namespaces.models import Project, Image, Container, Network


def addImage(projectId, name, repository_URL, repo_visibility, config_file_path) -> [str, str]:
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


def addContainer(projectId, name, imageId, environment, networks, exposedPort=None):
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
                container = Container(containerId=projectId + '-' + name, imageId=imageId, environment=environment,
                                      network=networks, exposedPort=exposedPort)
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


def deleteProject(projectId):
    project = Project.objects(id=projectId).first()
    for name in project.containers.key:
        res = deleteContainer(projectId, name)
        if res != "0":
            return res
    project.delete()
    return "0"


def deleteContainer(projectId, containers):
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
                            image.delete()
                            networks = []
                            for network in container.network:
                                networks.append(network)
                            for network in container.network:
                                for key, cont in project.containers.items():
                                    if key != containerName:
                                        if network in cont.network:
                                            networks.remove(network)
                            for network in networks:
                                requests.delete(
                                    'http://' + deployAddress + ':5000/network/' + project.networks[network].networkId)
                                project.update(**{'unset__networks__' + network: 1})

                            project.update(**{'unset__containers__' + containerName: 1})
                            project.save()
                            return "0"
                        else:
                            return "04X" + response.json()['code']
                    else:
                        return "01001"
                else:
                    return "04003"
        else:
            return "01001"
    else:
        return "04001"


def getProjectId(name, owner):
    project = Project.objects(name=name, owner=owner).first()
    if project:
        return str(project.id)
    else:
        return None


def containerStatus(projectId: str, containers: List[str], action: str):
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
                            for network in container.network:
                                netid.append(project.networks[network].networkId)
                            response = requests.post(
                                'http://' + deployAddress + ':5000/deployment/' + container.imageId,
                                json={'name': container.containerId,
                                      'hostname': containerName,
                                      'environment': container.environment,
                                      'network': netid})
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
    rep = requests.get(URL)
    if rep.status_code == 200:
        return "0"
    else:
        return "03006"


def extractConfig(repository_URL, repo_visibility, config_file_path) -> [str, Dict]:
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


def redactContainer(config: Dict, projectId, configType, repo_URL=None, logger=None) -> [str, List]:
    containerList = []
    if 'networks' in config:
        defaultNetwork = False
    else:
        defaultNetwork = True
    for key in config['services']:
        container = config['services'][key]
        logger.error(container)
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
                logger.error('environment List ')
                setting.append([])
        else:
            logger.error('environment')
            setting.append([])

        if 'networks' in container:
            if defaultNetwork:
                setting.append(['default'])
            elif type(container['networks']) is list:
                setting.append(container['networks'])
            else:
                logger.error('networks List ')
                setting.append([])
        else:
            logger.error('networks')
            setting.append([])

        if 'ports' in container:
            if type(container['ports']) is list:
                ports = []
                for port in container['ports']:
                    host, inter = port.split(":")
                    ports.append(inter)
                setting.append(ports)
            else:
                logger.error('ports List ')
                setting.append([])
        else:
            logger.error('ports')
            setting.append([])

        containerList.append(setting)
    for containerConfig in containerList:
        logger.error(containerConfig)
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
            rep = addContainer(projectId, containerConfig[0], containerConfig[1], containerConfig[2],
                               containerConfig[3],
                               containerConfig[4])
            if rep != "0":
                return rep
