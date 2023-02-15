"""
Channels Functions
"""

def get_channels(self, organizationId=None, workspaceId=None, channelId=None):
    """Shows all channels available to the user. Can filter by organizationId, workspaceId, or channelId.
    
    Parameters
    ----------
    organizationId : str
        Filter channel list on what's available to the organization.
    workspaceId : str    
        Filter channel list on what's available to the workspace.
    channelId: str
        Filter channel list on the specific channelId.
    
    Returns
    -------
    list[dict]
        List of channels associated with user, workspace, organization or channelId.
    """
    if self.check_logout(): return
    channels = self.ana_api.getChannels(organizationId=organizationId, workspaceId=workspaceId, channelId=channelId)
    if channels:
        for channel in channels:
            self.channels[channel['channelId']] = channel['name']
    return channels
       
                

def get_managed_channels(self, channelId=None, organizationId=None):
    """Get information for all managed channels that you own within your organization.
    
    Parameters
    ----------
    channelId : str
        Channel Id to filter.
    organizationId : str
        Organization ID. Defaults to current if not specified.
   
    Returns
    -------
    list[dict]
        channel data
    """
    if self.check_logout(): return
    if organizationId is None: organizationId = self.organization
    return self.ana_api.getManagedChannels(organizationId=organizationId, channelId=channelId)


def create_managed_channel(self, name, description=None, organizationId=None, volumes=[], instance='p2.xlarge', timeout=120, interfaceVersion=1):
    """Create a managed channel for your organization.
    
    Parameters
    ----------
    name : str
        Channel name.
    description : str
        Description of the channel
    organizationId : str
        Organization ID. Defaults to current if not specified.
    volumes : list[str]
        List of the data volume names to associate with this channel.
    instance: str
        AWS Instance type.
    timeout: int
        Maximum runtime of a channel run.
    interface: int
        The ana interface version number.
   
    Returns
    -------
    list[dict]
        channel data
    """
    if self.check_logout(): return
    if organizationId is None: organizationId = self.organization
    result = self.ana_api.createManagedChannel(organizationId=organizationId, name=name, description=description, volumes=volumes, instance=instance, timeout=timeout, interfaceVersion=interfaceVersion)
    self.get_channels()
    return result

def edit_managed_channel(self, channelId, name=None, description=None, volumes=None, instance=None, timeout=None, status=None, interfaceVersion=None):
    """Edit a managed channel for your organization.
    
    Parameters
    ----------
    channelId : str
        ChannelId ID of the channel to edit.
    name : name
        The new name to give the channel.
    description : str
        Description of the channel
    volumes : list[str]
        Data volumes for the channel.
    instance: str
        Instance type to run the channel on.
    timeout: int
        Maximum runtime for the channel run.
    status: str
        The status of the channel.
    interface: int
        The ana interface version number.
    
    Returns
    -------
    bool
        If true, the channel was successfully edited.
    """
    if self.check_logout(): return
    if channelId is None: raise Exception('ChannelId must be specified.')
    result = self.ana_api.editManagedChannel(channelId=channelId, name=name, description=description, volumes=volumes, instance=instance, timeout=timeout, status=status, interfaceVersion=interfaceVersion)
    self.get_channels()
    return result

def delete_managed_channel(self, channelId):
    """Delete a managed channel of your organization.
    
    Parameters
    ----------
    channelId : str
        Id of channel to delete.
    
    Returns
    -------
    str
        Status
    """
    if self.check_logout(): return
    if channelId is None: raise Exception('ChannelId must be specified.')
    result = self.ana_api.deleteManagedChannel(channelId=channelId)
    self.get_channels()
    return result
    
def add_channel_access(self, channelId, organizationId):
    """Add access to a channel for an organization.
    
    Parameters
    ----------
    channelId : str
        Id of channel to add access for.
    organizationId : str
        Organization ID. Defaults to current if not specified.
    
    Returns
    -------
    str
        Access status. 
    """
    if self.check_logout(): return
    if organizationId is None: raise Exception('OrganizationId must be specified.')
    return self.ana_api.addChannelOrganization(channelId=channelId, organizationId=organizationId)


def remove_channel_access(self, channelId, organizationId):
    """Remove access to a channel for an organization.
    
    Parameters
    ----------
    channelId : str
        Id of channel to remove access to.
    organizationId : str
        Organization ID. Defaults to current if not specified.
    
    Returns
    -------
    str
        Access status. 
    """
    if self.check_logout(): return
    if organizationId is None: raise Exception('OrganizationId must be specified.')
    return self.ana_api.removeChannelOrganization(channelId=channelId, organizationId=organizationId)


def build_managed_channel(self, channelfile, enforce_size_limit=True):
    """Build the Docker image of a channel.
    
    Parameters
    ----------
    channelfile : str
        The channel file for the channel to build.
    enforce_size_limit: bool
        Flag that controls the size of the Docker Image and will block the build if larger than 7.5GB. Set this to False if the channel will be larger than 7.5GB.
    Returns
    -------
    bool
        A boolean that indicates if the channel Docker image was successfully built.
    """
    import os
    import shutil
    import docker
    import time

    # make sure we can connect to docker
    try: dockerclient = docker.from_env()
    except: raise Exception('Cannot connect to Docker host.')

    # build dockerfile
    print('Building Dockerfile...', end='')
    if not os.path.isfile(channelfile): raise Exception(f'No channel file {channelfile} found.')
    channeldir, channelfile = os.path.split(channelfile)
    if channeldir == "": channeldir = "./"   
    if not os.path.isdir(os.path.join(channeldir, '.devcontainer')): raise Exception(f'No .devcontainer directory found in channel directory.')
    if not os.path.isfile(os.path.join(channeldir, '.devcontainer/Dockerfile')): raise Exception(f'Issue detected with .devcontainer directory, build requires Dockerfile.')
    builddir = os.path.join(channeldir,'.devcontainer/.build')
    if os.path.isdir(builddir): shutil.rmtree(builddir)
    os.mkdir(builddir)
    with open(os.path.join(builddir, 'Dockerfile'), 'w+') as buildfile:
        with open(os.path.join(channeldir,'.devcontainer/Dockerfile')) as dockerfile: buildfile.write(dockerfile.read())
        deploycommands = """
# Commands used for deployment
RUN sudo mkdir /ana /data
COPY . /ana/
WORKDIR /ana
RUN sudo /home/$USERNAME/miniconda3/bin/pip install -r /ana/requirements.txt > /dev/null 2>&1 && \\
    sudo /home/$USERNAME/miniconda3/envs/anatools/bin/pip install -r /ana/requirements.txt > /dev/null 2>&1
ENTRYPOINT []
CMD ["bash"]
USER root"""
        buildfile.write(deploycommands)
    print('done.')

    # build the tar file, include what's necesary for the container
    print('Building Docker Context...', end='')
    dirs_to_not_include = ['.devcontainer', 'data', 'output']
    files = [path for path in os.listdir(channeldir) if path not in dirs_to_not_include]
    for filepath in files:
        full_path = os.path.join(channeldir, filepath)
        is_symbolic_link = os.path.islink(full_path)
        if not is_symbolic_link:
            if os.path.isdir(full_path): shutil.copytree(full_path, os.path.join(builddir, filepath))
            else: shutil.copyfile(full_path, os.path.join(builddir, filepath))
    print('done.')

    # call the docker build command
    print('Building Docker Image...', end='', flush=True)
    dockerclient = docker.from_env()
    image, logs = dockerclient.images.build(path=builddir, tag=channelfile.split('.')[0])
    print('done.')

    if enforce_size_limit and not __check_docker_image_size(image):
        return False

    # cleanup
    shutil.rmtree(builddir)
    return True

def __check_docker_image_size(image):
    """ Helper function that computes size of docker image. 
    
    Parameters
    ----------
    image : object
        Docker Image Object
    
    Returns
    -------
    bool
        True if size is less than 7.5GB. False if it's bigger.
    """
    import sys

    # limit size to 7.5GB
    size_of_image = image.attrs['VirtualSize']
    size_limit = 8053063680

    if size_of_image > size_limit:
        print('\033[91m' + 'ERROR: Docker Image size is greater than 7.5GB and cannot be uploaded.' + '\033[0m')
        print('Exiting...')
        return False

    return True  

def deploy_managed_channel(self, channelId=None, channelfile=None, image=None, enforce_size_limit=True):
    """Deploy the Docker image of a channel.
    
    Parameters
    ----------
    channelId : str
        Channel ID that you are pushing the image to. If the channelId isn't specified, it will use the image name to lookup the channelId.
    channelfile: str
        Name of the channel file to look for. 
    image: str
        The Docker image name. This should match the channel name when running ana. If image is not specified, it will use the channel name for the channelId.
    enforce_size_limit: bool
        Flag that controls the size of the Docker Image and will block the build if larger than 7.5GB. Set this to False if the channel will be larger than 7.5GB.

    Returns
    -------
    str
        deploymentId for current round of deployment or an error message if something went wrong
    """
    import os
    import docker
    import base64
    if self.check_logout(): return
    if channelId is None and image is None: print('The channelId or local image must be specified.'); return
    self.get_channels()

    # make sure we can connect to docker
    try: dockerclient = docker.from_env()
    except: raise Exception('Cannot connect to Docker host.')

    if channelfile:
        if self.build_managed_channel(channelfile, enforce_size_limit=enforce_size_limit):
            image = os.path.split(channelfile)[1].split('.')[0]
        else: return False
    
    # check if channel image is in Docker
    dockerclient = docker.from_env()
    if image and channelId:
        channel = image
        if channelId not in self.channels: 
            print(f'User does not have permissions to deploy to a channel with ID \"{channelId}\" on the Rendered.ai Platform.'); return
    elif image:   
        channel = image
        channels = self.get_managed_channels()
        filteredchannels = [channel for channel in channels if channel['name'] == image]
        if len(filteredchannels) == 1: channelId = filteredchannels[0]['channelId']
        elif len(filteredchannels) == 0: print(f'User does not have permissions to deploy to a channel named \"{image}\" on the Rendered.ai Platform.'); return
        else: print('User has access to multiple channels with name \"{image}\" on the Rendered.ai Platform, please specify channelId.'); return
    else:
        if channelId in self.channels: channel = self.channels[channelId]
        else: print(f'User does not have permissions to deploy to a channel with ID \"{channelId}\" on the Rendered.ai Platform.'); return
    try: 
        channelimage = dockerclient.images.get(channel)
        if enforce_size_limit and not __check_docker_image_size(channelimage):
            return False
    except docker.errors.ImageNotFound: print(f'Could not find Docker image with name \"{channel}\".'); return
    except: raise Exception('Error connecting to Docker.')

    # get repository info
    print(f'Docker image \"{channel}\" will be deployed to the \"{self.channels[channelId]}\" channel.')
    print(f"Pushing Docker Image. This could take awhile...", end='', flush=True)
    dockerinfo = self.ana_api.deployManagedChannel(channelId, image)
    deploymentId = dockerinfo['deploymentId']
    reponame = dockerinfo['ecrEndpoint']
    encodedpass = dockerinfo['ecrPassword']
    if encodedpass:
        encodedbytes = encodedpass.encode('ascii')
        decodedbytes = base64.b64decode(encodedbytes)
        decodedpass = decodedbytes.decode('ascii').split(':')[-1]
    else: print('Failed to retrieve Docker credentials from Rendered.ai platform.'); return

    # tag and push image
    channelimage.tag(reponame)
    if self.verbose:
        for line in dockerclient.images.push(reponame, auth_config={'username':'AWS', 'password':decodedpass}, stream=True, decode=True):
            if 'status' and 'progress' in line:
                    print(f"\x1b[1K\r {line['status']} \"{channel}\" image to \"{self.channels[channelId]} channel\" {line['progress']}",end='')
    else:
        largest = 0
        for line in dockerclient.images.push(reponame, auth_config={'username':'AWS', 'password':decodedpass}, stream=True, decode=True):
            if 'status' and 'progressDetail' in line:
                if 'current' and 'total' in line['progressDetail']:
                    progressDetail = line['progressDetail']
                    if progressDetail['total'] >= largest:
                        largest = progressDetail['total']
                        print(f"\x1b[1K\r[{round((progressDetail['current']/progressDetail['total']) * 100)}%] {line['status']} \"{channel}\" to \"{self.channels[channelId]}\" ",end='')
    print("\nComplete!", flush=True)
    
    # cleanup docker and update channels
    dockerclient.images.remove(reponame)
    dockerclient.close()
    if self.check_logout(): return
    self.get_channels()
    return deploymentId


def get_deployment_status(self, deploymentId, stream=False):
    """Retrieves status for a channel's deployment.
    
    Parameters
    ----------
    deploymentId: str
        The deploymentId to retrieve status for
    stream: bool
        Flag to print information to the terminal so the user can avoid constant polling to retrieve status.

    Returns
    -------
    list[dict]
        Deployment status. 
    """
    import time
    if self.check_logout(): return
    if deploymentId is None: raise Exception('DeploymentId must be specified.')
    if stream:
        UP = "\033[3F"
        CLR = "\x1B[0K"
        
        data = self.ana_api.getChannelDeployment(deploymentId=deploymentId)
        print(f"{UP}Step: {data['status']['step']}{CLR}\nState: {data['status']['state']}{CLR}\nMessage: {data['status']['message']}{CLR}\n", end='', flush=True)

        while (data['status']['state'] not in ['Channel Deployment Complete','Channel Deployment Failed']):
            time.sleep(10)
            print(f"{UP}Step: {data['status']['step']}{CLR}\nState: {data['status']['state']}{CLR}\nMessage: {data['status']['message']}{CLR}\n", end='', flush=True)
            if self.check_logout(): return
            data = self.ana_api.getChannelDeployment(deploymentId=deploymentId)
        print(f"{UP}Step: {data['status']['step']}\nState: {data['status']['state']}\nMessage: {data['status']['message']}", flush=True)
    else: return self.ana_api.getChannelDeployment(deploymentId=deploymentId)

    
def get_channel_documentation(self, channelId, localDir=None):
    """Downloads a markdown file for channel documentation.
    
    Parameters
    ----------
    channelID: str
        The channelId of the channel
    localDir: str
        The location to download the file to.

    Returns
    -------
    list[str]
        The list of filenames downloaded.
    """
    import os
    import requests

    if channelId not in self.channels: raise ValueError(f'Could not find channel with ID "{channelId}"')
    if localDir is None: localDir = './'
    elif not os.path.isdir(localDir): raise ValueError(f'Could not find directory {localDir}')

    docfile = self.ana_api.getChannelDocumentation(channelId=channelId)[0]
    downloadresponse = requests.get(url=docfile['markdown'])
    filename = os.path.join(localDir, channelId+"."+docfile['markdown'].split('?')[0].split('/')[-1].split('.')[1])
    with open(filename, 'wb') as outfile:
        outfile.write(downloadresponse.content)
    return filename


def upload_channel_documentation(self, channelId, mdfile):
    """Uploads a markdown file for channel documentation.
    
    Parameters
    ----------
    channelID: str
        The channelId of the channel
    mdfile: str
        The filepath of the markdown file used for channel documentation.

    Returns
    -------
    bool
        Success/Failure of channel documenation upload.
    """
    import os
    import requests

    if channelId not in self.channels: raise ValueError(f'Could not find channel with ID "{channelId}"')
    if not os.path.isfile(mdfile): raise ValueError(f'Could not find file {mdfile}')
    if os.path.splitext(mdfile)[1] != '.md': raise ValueError('The channel documentation file must be in markdown format with .md extension.') 
    fileinfo = self.ana_api.uploadChannelDocumentation(channelId=channelId, keys=[os.path.basename(mdfile)])[0]
    with open(mdfile, 'rb') as filebytes:
        files = {'file': filebytes}
        data = {
            "key":                  fileinfo['fields']['key'],
            "bucket":               fileinfo['fields']['bucket'],
            "X-Amz-Algorithm":      fileinfo['fields']['algorithm'],
            "X-Amz-Credential":     fileinfo['fields']['credential'],
            "X-Amz-Date":           fileinfo['fields']['date'],
            "X-Amz-Security-Token": fileinfo['fields']['token'],
            "Policy":               fileinfo['fields']['policy'],
            "X-Amz-Signature":      fileinfo['fields']['signature'],
        }
        response = requests.post(fileinfo['url'], data=data, files=files)
        if response.status_code != 204: 
            print(response.status_code)
            raise Exception('Failed to upload channel documentation file.')
    return True
