"""
UMAP Functions
"""
import os
import requests

def get_umap(self, umapId, workspaceId=None):
    """Retrieves information about UMAP dataset comparison from the platform.
    
    Parameters
    ----------
    umapId : str
        UMAP Job ID. 
    workspaceId : str
        Workspace ID where the datasets exists.
    
    Returns
    -------
    dict
        UMAP information.
    """
    if self.check_logout(): return
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.getUMAP(umapId=umapId, workspaceId=workspaceId)
    

def create_umap(self, datasetIds, samples, workspaceId=None):
    """Creates a UMAP dataset comparison job on the platform.
    
    Parameters
    ----------
    datasetIds : [str]
        Dataset ID to retrieve information for. 
    samples : [int]
        Samples to take from each dataset.
    workspaceId : str
        Workspace ID where the datasets exists.
    
    Returns
    -------
    str
        The UMAP Job ID.
    """
    if self.check_logout(): return
    if len(datasetIds) != len(samples): raise ValueError("The length of datasetIds must match the length of samples.")
    for sample in samples:
        if sample < 5: raise ValueError("The number of samples must be between the range of 5 and dataset runs.")
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.createUMAP(datasetIds=datasetIds, samples=samples, workspaceId=workspaceId)


def delete_umap(self, umapId, workspaceId=None):
    """Deletes/cancels a UMAP dataset comparison on the platform.
    
    Parameters
    ----------
    umapId : str
        UMAP Job ID. 
    workspaceId : str
        Workspace ID where the datasets exists.
    
    Returns
    -------
    bool
        Status.
    """
    if self.check_logout(): return
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.deleteUMAP(umapId=umapId, workspaceId=workspaceId)
