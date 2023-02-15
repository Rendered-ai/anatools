"""
Volumes Functions
"""

def get_volumes(self, volumeId=None, organizationId=None):
    """Retrieves all volumes the user has access to.
    
    Parameters
    ----------
    volumeId : str
        The ID of a specific Volume.
    organizationId : str
        The ID of the organization that the volume belongs to.
    
    Returns
    -------
    list[dict]
        Volume Info
    """
    if self.check_logout(): return
    volumes = self.ana_api.getVolumes(organizationId=organizationId, volumeId=volumeId)
    if volumes:
        for volume in volumes:
            self.volumes[volume['volumeId']] = volume['name']
    return volumes    


def get_managed_volumes(self, volumeId=None, organizationId=None):
    """Retrieves the managed volumes for an organization.
    
    Parameters
    ----------
    volumeId : str
        The ID of a specific Volume.
    organizationId : str
        The ID of the organization that the managed volume belongs to.
    
    Returns
    -------
    list[dict]
        Volume Info
    """
    if self.check_logout(): return
    if organizationId is None: organizationId = self.organization
    return self.ana_api.getManagedVolumes(organizationId=organizationId, volumeId=volumeId)


def create_managed_volume(self, name, description=None, organizationId=None):
    """Creates a new volume with the specified name in the organization.
    
    Parameters
    ----------
    name : str
        The name of the new volume. Note: this name needs to be unique per organization.
    description : str
        Description of the volume
    organizationId : str
        The ID of the organization that the managed volume will belong to.
    
    Returns
    -------
    str
        volumeId
    """
    if self.check_logout(): return
    if organizationId is None: organizationId = self.organization
    if name is None: raise Exception("Name must be specified.")
    return self.ana_api.createManagedVolume(organizationId=organizationId, name=name, description=description)

    
def delete_managed_volume(self, volumeId):
    """Removes the volumeId from the organization. Note that this will delete any remote data in the volume 
    and channels that rely on this volume will need to be updated.
    
    Parameters
    ----------
    volumeId : str
        The ID of a specific Volume to delete.
    
    Returns
    -------
    str
        Status
    """
    if self.check_logout(): return
    if volumeId is None: raise Exception('VolumeId must be specified.')
    return self.ana_api.deleteManagedVolume(volumeId=volumeId)


def edit_managed_volume(self, volumeId, name=None, description=None):
    """Edits the name of a volume.
    
    Parameters
    ----------
    volumeId: str
        The volumeId that will be updated.
    name : str
        The new name of the new volume. Note: this name needs to be unique per organization.
    description : str
        Description of the volume
    
    Returns
    -------
    str
        Status
    """
    if self.check_logout(): return
    if volumeId is None: raise Exception('VolumeId must be specified.')
    if name is None and description is None: raise Exception("Either name or description must be specified.")
    return self.ana_api.editManagedVolume(volumeId=volumeId, name=name, description=description)


def add_volume_access(self, volumeId, organizationId):
    """Add access to a volume for an organization.
    
    Parameters
    ----------
    volumeId : str
        VolumeId to add access for.
    organizationId : str
        Organization ID to add access
    
    Returns
    -------
    str
        Status
    """
    if self.check_logout(): return
    if organizationId is None: raise Exception('OrganizationId must be specified.')
    if volumeId is None: raise Exception('VolumeId must be specified.')
    return self.ana_api.addVolumeOrganization(volumeId=volumeId, organizationId=organizationId)


def remove_volume_access(self, volumeId, organizationId):
    """Remove access to a volume for an organization.
    
    Parameters
    ----------
    volumeId : str
       VolumeId to remove access to.
    organizationId : str
        Organization ID to remove access.
    
    Returns
    -------
    str
       Status
    """
    if self.check_logout(): return
    if organizationId is None: raise Exception('OrganizationId must be specified.')
    if volumeId is None: raise Exception('VolumeId must be specified.')
    return self.ana_api.removeVolumeOrganization(volumeId=volumeId, organizationId=organizationId)


def get_volume_data(self, volumeId, files=[], dir=""):
    """Retrieves information about data from a volume.
    
    Parameters
    ----------
    volumeId : str
       VolumeId to remove access to.
    files : str
        The specific files or directories to retrieve information about from the volume, if you wish to retrieve all then leave the list empty.
    dir : str
        Specific volume directory to retrieve information about. Optional. 
    Returns
    -------
    str
       Status
    """
    if self.check_logout(): return
    if volumeId is None: raise Exception('VolumeId must be specified.')

    result = []
    condition = True
    offset = 0
    
    while condition:
        response = self.ana_api.getVolumeData(volumeId=volumeId, keys=files, dir=dir, limit=100, offset=offset)
        for fileinfo in response['keys']:
            result.append({
                'key':          fileinfo['key'],
                'size':         fileinfo['size'],
                'lastUpdated':  fileinfo['updatedAt'],
                'hash':         fileinfo['hash']
            })
        
        if (response['pageInfo']['totalItems'] > offset + 100):
            offset += 100
        else:
            condition = False

    return result


def download_volume_data(self, volumeId, files=[], localDir=None, sync=False):
    """Download data from a volume.
    
    Parameters
    ----------
    volumeId : str
       VolumeId to download data of.
    files : str
        The specific files or directories to retrieve from the volume, if you wish to retrieve all then leave the list empty.
    localDir : str
        The location of the local directory to download the files to. If not specified, this will download the files to the current directory.
    sync: bool
        Recursively downloads new and updated files from the source to the destination. Only creates folders in the destination if they contain one or more files.
    Returns
    -------
    str
       Status
    """
    import hashlib, requests, traceback, os
    if self.check_logout(): return
    if volumeId is None: raise Exception('VolumeId must be specified.')
    if localDir is None: localDir = os.getcwd()
    if not os.path.exists(localDir): raise Exception(f"Could not find directory {localDir}.")

    response = self.ana_api.getVolumeData(volumeId=volumeId, keys=files, dir=None)
    source_hashes = list(map((lambda x: x['key'] + x['hash']), response))
    destination_files = []
    destination_hashes = []

    if sync == True:    
        for root, dirs, files in os.walk(localDir):
            for file in files:
                filepath = os.path.join(root, file).replace(localDir, '')
                destination_files.append(filepath)
                file_hash = hashlib.md5()
                with open(os.path.join(root, file),'rb') as f: 
                    while True:
                        chunk = f.read(128 * file_hash.block_size)
                        if not chunk:
                            break
                        file_hash.update(chunk)
                destination_hashes.append(filepath + file_hash.hexdigest())

    for index, hash in enumerate(source_hashes):
        if (sync == True and (hash in destination_hashes)):
            print(f"\x1b[1K\rsync: {response[index]['key']}'s hash exists in {localDir}", end='\n' if self.verbose else '', flush=True)
        elif sync == False or (hash not in destination_hashes):
            try:
                downloadresponse = requests.get(url=response[index]['url'])
                filename = os.path.join(localDir, response[index]['key'])
                if not os.path.exists(os.path.dirname(filename)):
                    os.makedirs(os.path.dirname(filename))
                with open(filename, 'wb') as outfile:
                    outfile.write(downloadresponse.content)
                print(f"\x1b[1K\rdownload: {response[index]['key']} to {filename}", end='\n' if self.verbose else '', flush=True)
            except:
                traceback.print_exc()
                print(f"\x1b[1K\rdownload: failed to download {response[index]['key']}", end='\n' if self.verbose else '', flush=True)

    return


def upload_volume_data(self, volumeId, files=[], localDir=None, sync=False):
    """Upload data to a volume.
    
    Parameters
    ----------
    volumeId : str
       VolumeId to upload data to.
    files : list[str]
        The specific files or directories to push to the volume from the localDir. If you wish to push all data in the root directory, then leave the list empty.
    localDir : str
        The location of the local directory to upload the files from. If not specified, this will try to upload the files from the current directory.
    sync: bool
        Recursively uploads new and updated files from the source to the destination. Only creates folders in the destination if they contain one or more files.
    Returns
    -------
    str
       Status
    """
    import hashlib, requests, traceback, time, os

    if self.check_logout(): return
    if volumeId is None: raise Exception('VolumeId must be specified.')
    if localDir is None: localDir = os.getcwd()
    if not localDir.endswith('/'): localDir+='/'
    if not os.path.exists(localDir): raise Exception(f"Could not find directory {localDir}.")

    source_files = []
    source_hashes = []
    faileduploads = []
        
    if len(files):
        for file in files:
            filepath = os.path.join(localDir, file)
            if os.path.isdir(filepath):
                for root, dirs, files in os.walk(filepath):
                    for file in files:
                        filepath = os.path.join(root, file).replace(localDir, '')
                        source_files.append(filepath)
                        if sync == True:
                            file_hash = hashlib.md5()
                            with open(os.path.join(root,file),'rb') as f: 
                                while True:
                                    chunk = f.read(128 * file_hash.block_size)
                                    if not chunk: break
                                    file_hash.update(chunk)
                            source_hashes.append(filepath + file_hash.hexdigest())
            elif os.path.isfile(filepath):
                source_files.append(file)
                if sync == True:
                    file_hash = hashlib.md5()
                    with open(filepath,'rb') as f: 
                        while True:
                            chunk = f.read(128 * file_hash.block_size)
                            if not chunk: break
                            file_hash.update(chunk)
                    source_hashes.append(file + file_hash.hexdigest())
            else: print(f"Could not find {filepath}.")
    else:
        for root, dirs, files in os.walk(localDir):
            for file in files:
                filepath = os.path.join(root, file).replace(localDir, '')
                source_files.append(filepath)
                if sync == True:
                    file_hash = hashlib.md5()
                    with open(os.path.join(root,file),'rb') as f: 
                        while True:
                            chunk = f.read(128 * file_hash.block_size)
                            if not chunk:
                                break
                            file_hash.update(chunk)
                    source_hashes.append(filepath + file_hash.hexdigest())

    if sync == True:
        response = self.ana_api.getVolumeData(volumeId=volumeId, keys=files)
        destination_hashes = list(map((lambda x: x['key'] + x['hash']), response))
        delete_files = []
        for index, object in enumerate(response):
            if object['key'] not in source_files:
                delete_files.append(object['key'])  

        if (len(delete_files)):
            print(f"The following files will be deleted:", end='\n', flush=True)
            for file in delete_files:
                print(f"   {file}", end='\n', flush=True)
            answer = input("Delete these files [Y/n]: ")
            if answer.lower() == "y":
                self.refresh_token()
                self.ana_api.deleteVolumeData(volumeId=volumeId, keys=delete_files)

    for index, file in enumerate(source_files):
        if (sync == True and (source_hashes[index] in destination_hashes)):
            print(f"\x1b[1K\rsync: {file}'s hash exists", end='\n' if self.verbose else '', flush=True)
        elif sync == False or (source_hashes[index] not in destination_hashes):
            self.refresh_token()
            fileinfo = self.ana_api.putVolumeData(volumeId=volumeId, keys=[file])[0]
            try:
                filepath = os.path.join(localDir, file)
                
                print(f"\x1b[1K\rupload: {file} to the volume. [{index+1} / {len(source_files)}]", end='\n' if self.verbose else '', flush=True)
                with open(filepath, 'rb') as filebytes:
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
                        faileduploads.append(file)
                        print(f"\x1b[1K\rupload: {file} failed", end='\n' if self.verbose else '', flush=True)
                    else:
                        print(f"\x1b[1K\rupload: {file} completed", end='\n' if self.verbose else '', flush=True)
            except:
                traceback.print_exc()
                faileduploads.append(file)
                print(f"\x1b[1K\rupload: {file} failed", end='\n' if self.verbose else '', flush=True)
    print("\x1b[1K\rUploading files completed.", flush=True)
    if len(faileduploads): print('The following files failed to upload:', faileduploads, flush=True)
    return
            

def delete_volume_data(self, volumeId, files=[]):
    """Delete data from a volume.
    
    Parameters
    ----------
    volumeId : str
       VolumeId to delete files from.
    files : str
        The specific files to delete from the volume. If left empty, no files are deleted.
    
    Returns
    -------
    str
       Status
    """
    if self.check_logout(): return
    if volumeId is None: raise Exception('VolumeId must be specified.')
    return self.ana_api.deleteVolumeData(volumeId=volumeId, keys=files)


def mount_volumes(self, volumes):
    """Retrieves credentials for mounting volumes.
    
    Parameters
    ----------
    volumes : [str]
       Volumes to retrieve mount credentials for.

    Returns
    -------
    dict
        Credential information.
    """
    if self.check_logout(): return
    if not len(volumes): raise Exception('A list of volumeIds must be specified.')
    return self.ana_api.mountVolumes(volumes=volumes)
