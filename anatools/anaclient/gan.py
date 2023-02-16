"""
GAN Functions
"""
import os
import requests

def get_gan_models(self, organizationId=None, workspaceId=None, modelId=None):
    """Retrieve information about GAN models
    
    Parameters
    ----------
    organizationId : str
        Organization ID that owns the models
    workspaceId : str
        Workspace ID that contains the models
    modelId : str
        Model ID to retrieve information for. 
    
    Returns
    -------
    list[dict]
        GAN Model information.
    """
    if self.check_logout(): return
    if organizationId is None: organizationId = self.organization
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.getGANModels(organizationId=organizationId, workspaceId=workspaceId, modelId=modelId)
    

def get_gan_dataset(self, datasetId, workspaceId=None):
    """Retrieve information about GAN dataset jobs.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID to retrieve information for. 
    workspaceId : str
        Workspace ID where the dataset exists.
    
    Returns
    -------
    list[dict]
        Information about the GAN Dataset.
    """
    if self.check_logout(): return
    if datasetId is None: raise ValueError("DatasetId must be provided.")
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.getGANDataset(workspaceId=workspaceId, datasetId=datasetId)


def create_gan_dataset(self, modelId, datasetId, workspaceId=None):
    """Create a new GAN dataset based off an existing dataset. This will start a new job.
    
    Parameters
    ----------
    modelId : str
        Model ID to use for the GAN.
    datasetId : str
        Dataset ID to input into the GAN. 
    workspaceId : str
        Workspace ID where the dataset exists.
    
    Returns
    -------
    str
        The datsetId for the GAN Dataset job.
    """
    if self.check_logout(): return
    if modelId is None: raise ValueError("ModelId must be provided.")
    if datasetId is None: raise ValueError("DatasetId must be provided.")
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.createGANDataset(workspaceId=workspaceId, datasetId=datasetId, modelId=modelId)


def delete_gan_dataset(self, datasetId, workspaceId=None):
    """Deletes a GAN dataset job.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID for the GAN dataset. 
    workspaceId : str
        Workspace ID where the dataset exists.
    
    Returns
    -------
    bool
        Returns true if the GAN dataset was successfully deleted.
    """
    if self.check_logout(): return
    if datasetId is None: raise ValueError("DatasetId must be provided.")
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.deleteGANDataset(workspaceId=workspaceId, datasetId=datasetId)


def create_managed_gan(self, name, description, modelfile, flags=None, organizationId=None):
    """Uploades a GAN model to the microservice. The model will be owned by the specified organization.
    If organizationId is not given the model will be owned by that of the analcient.
    
    Parameters
    ----------
    name : str
        A name for model.
    description : str
        Details about the model.
    modelfile : str
        The file of the model - relative to the local directry.
    flags : str
        Parameters for use when running the model.
    organizationId : str
        Id of organization that owns the model, that of the anaclient if not given.
    
    Returns
    -------
    modleId : str
        The unique identifier for this model.
    """
    if self.check_logout(): return

    if not os.path.exists(modelfile):
        print("File not found in " + os.getcwd())
        return

    if organizationId is None: organizationId = self.organization

    self.refresh_token()
    fileinfo = self.ana_api.createManagedGAN(organizationId=organizationId, name=name, description=description, flags=flags)
    # fileinfo keys:
    # "key": S3 Key
    # "modelId": modelId,
    # "url": s3 url
    # "fields": dictionary of details to access presigned url
    if not fileinfo:
        print(fileinfo)
        return
    
    try:
        with open(modelfile, 'rb') as filebytes:
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

    return fileinfo['modelId']


def delete_gan_model(self, modelId):
    """Delete the GAN model and remove access to it from all shared organizations.
    This can only be done by a user in the organization that owns the model.
    
    Parameters
    ----------
    modelId : str
        The ID of a specific GAN model.
    
    Returns
    -------
    str
        Status
    """
    if self.check_logout(): return
    if modelId is None: raise Exception('ModelId must be specified.')
    return self.ana_api.deleteGANModel(modelId=modelId)

def get_managed_gans(self, organizationId=None, modelId=None):
    """Retrieves the managed GANs for an organization.
    
    Parameters
    ----------
    organizationId : str
        The ID of the organization that the managed GAN belongs to.
    modelId : str
        The ID of a specific model.

    Returns
    -------
    list[dict]
        Model Info
    """
    if self.check_logout(): return
    if organizationId is None: organizationId = self.organization
    return self.ana_api.getManagedGANs(organizationId=organizationId, modelId=modelId)

def edit_managed_gan(self, modelId, name=None, description=None, flags=None):
    """Edits the name, description, and flags of a managed gan.
    
    Parameters
    ----------
    modelId: str
        The modelId that will be updated.
    name : str
        The new name of the managed gan. Note: this name needs to be unique per organization.
    description : str
        Description of the managed gan
    flags : str
        Flags for the model
    
    Returns
    -------
    bool
        Status
    """
    if self.check_logout(): return
    if modelId is None: raise Exception('ModelId must be specified.')
    if name is None and description is None and flags is None: return
    return self.ana_api.editManagedGAN(modelId=modelId, name=name, description=description, flags=flags)

def delete_managed_gan(self, modelId):
    """Removes the managed map
    
    Parameters
    ----------
    modelId : str
        The ID of a specific Model to delete.
    
    Returns
    -------
    bool
        Status
    """
    if self.check_logout(): return
    if modelId is None: raise Exception('ModelId must be specified.')
    return self.ana_api.deleteManagedGAN(modelId=modelId)

def add_gan_organization(self, modelId, organizationId):
    """Add access to a map for an organization.
    
    Parameters
    ----------
    modelId : str
        ModelId to add access for.
    organizationId : str
        Organization ID to add access
    
    Returns
    -------
    bool
        Status
    """
    if self.check_logout(): return
    if organizationId is None: raise Exception('OrganizationId must be specified.')
    if modelId is None: raise Exception('ModelId must be specified.')
    return self.ana_api.addGANOrganization(modelId=modelId, organizationId=organizationId)


def remove_gan_organization(self, modelId, organizationId):
    """Remove access to a map for an organization.
    
    Parameters
    ----------
    modelId : str
       ModelId to remove access to.
    organizationId : str
        Organization ID to remove access.
    
    Returns
    -------
    bool
       Status
    """
    if self.check_logout(): return
    if organizationId is None: raise Exception('OrganizationId must be specified.')
    if modelId is None: raise Exception('ModelId must be specified.')
    return self.ana_api.removeGANOrganization(modelId=modelId, organizationId=organizationId)