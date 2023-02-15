"""
Annotations Functions
"""
import os
import requests

def get_annotation_formats(self):
    """Retrieves the annotation formats supported by the Platform.
    
    Returns
    -------
    str
        The annotation formats supported by the Platform.
    """
    if self.check_logout(): return
    return self.ana_api.getAnnotationFormats()


def get_annotation_maps(self, organizationId=None, workspaceId=None, mapId=None):
    """Retrieves annotation maps.
    
    Parameters
    ----------
    organizationId : str
        Organization ID to retrieve maps for. If not specified then the current
        organization is used.
    workspaceId: str
        Workspace ID to retrieve maps for. If not specified then the current
        workspace is used.
    mapId: str
        Annotation map ID to retrieve
    
    Returns
    -------
    str
        The requested annotation maps.
    """
    if self.check_logout(): return
    if organizationId is None: organizationId = self.organization
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.getAnnotationMaps(organizationId, workspaceId, mapId)

def get_managed_maps(self, organizationId=None, mapId=None):
    """Retrieves the map(s) managed by the organization
    
    Parameters
    ----------
    organizationId : str
        Organization ID to retrieve maps for. If not specified then the current
        organization is used.
    mapId: str
        Annotation map ID to retrieve
    
    Returns
    -------
    str
        The requested annotation maps.
    """
    if self.check_logout(): return
    if organizationId is None: organizationId = self.organization
    return self.ana_api.getManagedMaps(organizationId, mapId)


def get_annotations(self, datasetId=None, annotationId=None, workspaceId=None):
    """Retrieve information about existing annotations generated for a dataset. Querying requires both datasetId and annotationId.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID to generate annotations for.
    annotationId : str
        Annotation ID for a specific annotations job.
    workspaceId: str
        Workspace ID where the annotations exist. If none is provided, the current workspace will get used. 
    
    Returns
    -------
    list[dict]
        Annotation information.
    """
    if self.check_logout(): return
    if annotationId is None and datasetId is None: raise ValueError('datasetId and annotationId must be specified.')
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.getAnnotations(workspaceId=workspaceId, datasetId=datasetId, annotationId=annotationId)
    

def create_annotation(self, datasetId, format, map, workspaceId=None):
    """Generates annotations for an existing dataset. 
    
    Parameters
    ----------
    datasetId : str
        Dataset ID to generate annotation for.
    format : str
        Annotation format. Call get_annotation_formats() to find supported formats.
    map: str
        The map file used for annotations. Call get_annotation_maps() to find supported maps.
    workspaceId: str
        Workspace ID of the dataset to generate annotation for. If none is provided, the current workspace will get used. 
    
    Returns
    -------
    str
        The annotationsId for the annotation job.
    """
    if self.check_logout(): return
    if datasetId is None: raise ValueError("DatasetId must be defined.")
    if format is None: raise ValueError("Format must be defined.")
    if map is None: raise ValueError("Map must be defined.")
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.createAnnotation(workspaceId=workspaceId, datasetId=datasetId, format=format, map=map)
    

def download_annotation(self, datasetId, annotationId, workspaceId=None):
    """Downloads annotations archive.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID to download image annotation for.
    annotationId : str
        Id of previously generated image annotation. 
    workspaceId: str
        Workspace ID of the dataset to generate annotation for. If none is provided, the current workspace will get used. 
    
    Returns
    -------
    str
        The name of the archive file that got downloaded.
    """
    import requests
    if self.check_logout(): return
    if workspaceId is None: workspaceId = self.workspace
    url = self.ana_api.downloadAnnotation(workspaceId=workspaceId, datasetId=datasetId, annotationId=annotationId)
    fname = url.split('?')[0].split('/')[-1]
    with requests.get(url, stream=True) as downloadresponse:
        with open(fname, 'wb') as outfile:
            downloadresponse.raise_for_status()
            outfile.write(downloadresponse.content)
            with open(fname, 'wb') as f:
                for chunk in downloadresponse.iter_content(chunk_size=8192):
                    f.write(chunk)
    return fname


def delete_annotation(self, annotationId, workspaceId=None):
    """Delete a dataset annotation.
    
    Parameters
    ----------
    annotationId : str
        AnnoationId of the annotation job.
    workspaceId: str
        Workspace ID of the dataset to generate annotation for. If none is provided, the current workspace will get used. 
    
    Returns
    -------
    bool
        If true, successfully deleted the annotation.
    """
    if self.check_logout(): return
    if annotationId is None: raise ValueError("AnnotationId must be defined.")
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.deleteAnnotation(workspaceId=workspaceId, annotationId=annotationId)

def create_managed_map(self, name, description, mapfile, organizationId=None):
    """Uploades an annotation map to the microservice. The map will be owned by the specified organization.
    If not organizationId is given the model will be owned by that of the analcient.
    
    Parameters
    ----------
    name : str
        A name for map.
    description : str
        Details about the map.
    mapfile : str
        The map file - relative to the local directry.
    organizationId : str
        Id of organization that owns the map, that of the anaclient if not given.
    
    Returns
    -------
    mapId : str
        The unique identifier for this map.
    """
    if self.check_logout(): return

    if not os.path.exists(mapfile):
        print("File not found in " + os.getcwd())
        return

    if organizationId is None: organizationId = self.organization

    self.refresh_token()
    fileinfo = self.ana_api.createManagedMap(organizationId=organizationId, name=name, description=description)
    # fileinfo keys:
    # "mapId": mapId,
    # "url": s3 url
    # "fields": dictionary of details to access presigned url
    if not fileinfo:
        print(fileinfo)
        return
    
    try:
        with open(mapfile, 'rb') as filebytes:
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
                if self.verbose: print(f"Failure", flush=True)
            else:
                if self.verbose: print('Success', flush=True)
    except Exception as e:
        # traceback.print_exc()
        print('Failed to upload: {}'.format(e), flush=True)

    return fileinfo['mapId']

def edit_managed_map(self, mapId, name=None, description=None):
    """Edits the name of a managed map.
    
    Parameters
    ----------
    mapId: str
        The mapId that will be updated.
    name : str
        The new name of the managed map. Note: this name needs to be unique per organization.
    description : str
        Description of the managed map
    
    Returns
    -------
    bool
        Status
    """
    if self.check_logout(): return
    if mapId is None: raise Exception('MapId must be specified.')
    if name is None and description is None: return
    return self.ana_api.editManagedMap(mapId=mapId, name=name, description=description)

def delete_managed_map(self, mapId):
    """Removes the managed map
    
    Parameters
    ----------
    mapId : str
        The ID of a specific Map to delete.
    
    Returns
    -------
    bool
        Status
    """
    if self.check_logout(): return
    if mapId is None: raise Exception('MapId must be specified.')
    return self.ana_api.deleteManagedMap(mapId=mapId)

def add_map_organization(self, mapId, organizationId):
    """Add access to a map for an organization.
    
    Parameters
    ----------
    mapId : str
        MapId to add access for.
    organizationId : str
        Organization ID to add access
    
    Returns
    -------
    bool
        Status
    """
    if self.check_logout(): return
    if organizationId is None: raise Exception('OrganizationId must be specified.')
    if mapId is None: raise Exception('MapId must be specified.')
    return self.ana_api.addMapOrganization(mapId=mapId, organizationId=organizationId)


def remove_map_organization(self, mapId, organizationId):
    """Remove access to a map for an organization.
    
    Parameters
    ----------
    mapId : str
       MapId to remove access to.
    organizationId : str
        Organization ID to remove access.
    
    Returns
    -------
    bool
       Status
    """
    if self.check_logout(): return
    if organizationId is None: raise Exception('OrganizationId must be specified.')
    if mapId is None: raise Exception('MapId must be specified.')
    return self.ana_api.removeMapOrganization(mapId=mapId, organizationId=organizationId)