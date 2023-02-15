"""API Module"""

class api:
    
    def __init__(self, url, headers, verbose=False):
        import requests
        self.url = url
        self.headers = headers
        self.verbose = verbose
        self.session = requests.Session()

    def login(self, email, password):
        response = self.session.post(
            url = self.url, 
            json = {
                "operationName": "signIn",
                "variables": {
                    "email": email,
                    "password": password
                },
                "query": """mutation 
                    signIn($email: String!, $password: String!) {
                        signIn(email: $email, password: $password) {
                            uid
                            idtoken
                            expires
                        }
                    }"""})
        if 'errors' in response.json(): return False
        return self.errorhandler(response, "signIn")

    def close(self):
        self.session.close()

    from .handlers      import errorhandler
    from .organizations import getOrganizations, editOrganization
    from .channels      import getChannels, getManagedChannels, getChannelDeployment, createManagedChannel, deleteManagedChannel, editManagedChannel, addChannelOrganization, removeChannelOrganization, deployManagedChannel, setChannelGraph, getChannelDocumentation, uploadChannelDocumentation
    from .volumes       import getVolumes, getManagedVolumes, createManagedVolume, deleteManagedVolume, editManagedVolume, addVolumeOrganization, removeVolumeOrganization, getVolumeData, putVolumeData, deleteVolumeData, mountVolumes
    from .members       import getMembers, addMember, removeMember, editMember, getInvitations
    from .workspaces    import getWorkspaces, createWorkspace, deleteWorkspace, editWorkspace
    from .graphs        import getGraphs, createGraph, deleteGraph, editGraph, downloadGraph, getDefaultGraph
    from .datasets      import getDatasets, createDataset, deleteDataset, editDataset, downloadDataset, cancelDataset, datasetUpload, getDatasetRuns, getDatasetLog
    from .limits        import getPlatformLimits, setPlatformLimit, getOrganizationLimits, setOrganizationLimit, getWorkspaceLimits, setWorkspaceLimit, getOrganizationUsage
    from .analytics     import getAnalytics, getAnalyticsTypes, createAnalytics, deleteAnalytics
    from .annotations   import getAnnotations, getAnnotationFormats, getAnnotationMaps, createAnnotation, downloadAnnotation, getManagedMaps, createManagedMap, editManagedMap, deleteManagedMap, addMapOrganization, removeMapOrganization
    from .gan           import getGANModels, getGANDataset, createGANDataset, deleteGANDataset, createManagedGAN, deleteGANModel, addGANAccess, removeGANAccess, getManagedGANs, editManagedGAN, deleteManagedGAN, addGANOrganization, removeGANOrganization
    from .umap          import getUMAP, createUMAP, deleteUMAP
