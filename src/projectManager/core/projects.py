from typing import List

import requests

import core
from namespaces.models import Project, Image, Container, Network


def addContainer(projectId, name, repository_URL, repo_visibility, config_file_path, environment, networks,
                 exposedPort=None):
    project = Project.objects(id=projectId).first()
    if project:
        if name in project.containers:
            return "04004"
        imageTag = projectId + '-' + name + ':latest'
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
                    if exposedPort:
                        container = Container(containerId=projectId + '-' + name, imageId=imageID,
                                              environment=environment,
                                              network=networks, exposedPort=exposedPort)
                    else:
                        container = Container(containerId=projectId + '-' + name, imageId=imageID,
                                              environment=environment,
                                              network=networks)

                    project.containers[name] = container
                    project.save()
                    netid = []
                    for network in networks:
                        netid.append(project.networks[network].networkId)
                    responseDep = requests.post(
                        'http://' + deployAddress + ':5000/deployment/' + imageTag,
                        json={'name': projectId + '-' + name,
                              'hostname': name,
                              'environment': environment,
                              'network': netid})
                    if responseDep.status_code == 200:
                        project.containers[name].status = 'running'
                        project.save()
                        return "0"
                    else:
                        return "02X" + responseDep.json()['code']
                else:
                    return "03X" + response.json()['code']
            else:
                return "01001"
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


def deleteContainer(projectId, containerName):
    project = Project.objects(id=projectId).first()
    if project:
        container = project.containers[containerName]
        if container:
            code, deployAddress = core.getService("deploy")
            if code == "0":
                responseDep = requests.delete('http://' + deployAddress + ':5000/manage/' + container.containerId)
                if responseDep.status_code == 200:
                    code, imageAddress = core.getService("image")
                    if code == "0":
                        response = requests.delete(
                            'http://' + imageAddress + ':5000/image/build',
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
                                responseDep = requests.delete(
                                    'http://' + deployAddress + ':5000/network/' + project.networks[network].networkId)
                                project.update(**{'unset__networks__' + network: 1})

                            project.update(**{'unset__containers__' + containerName: 1})
                            project.save()
                            return "0"
                        else:
                            return "04X" + responseDep.json()['code']
                    else:
                        return "01001"
                else:
                    return "02X" + responseDep.json()['code']
            else:
                return "01001"
        else:
            return "04003"
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
                            response = requests.post(
                                'http://' + deployAddress + ':5000/deployment/' + container.imageId,
                                json={'name': container.containerId,
                                      'hostname': containerName,
                                      'environment': container.environment,
                                      'network': container.network})
                            if response.status_code == 200:
                                container.status = 'running'
                            else:
                                return "02X" + response.json()['code']
                    elif action == "stop":
                        if container.status == "running":
                            response = requests.delete('http://' + deployAddress + ':5000/manage/' + container.containerId)
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
