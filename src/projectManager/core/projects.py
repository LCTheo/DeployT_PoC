import requests

import core
from namespaces.models import Project, Image, Container, Network


def addContainer(projectId, name, repository_URL, repo_visibility, config_file_path, environment, networks,
                 exposedPort=None):
    project = Project.objects(id=projectId).first()
    if project:
        if name in project.containers:
            return "03003"
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
                        container = Container(imageId=imageID, environment=environment, network=networks,
                                              exposedPort=exposedPort)
                    else:
                        container = Container(imageId=imageID, environment=environment, network=networks)

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
                        return "0"
                    else:
                        return "03X" + responseDep.json()['code']
                else:
                    return "04X" + response.json()['code']
            else:
                return "01001"
        else:
            return "01001"
    else:
        return "03001"


def deleteProject(projectID):
    return 0


def deleteContainer(projectID, containerName):
    return 0


def getProjectId(name, owner):
    project = Project.objects(name=name, owner=owner).first()
    if project:
        return str(project.id)
    else:
        return None
