"""
GAN API calls.
"""

def getGANModels(self, organizationId, workspaceId, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getGANModels",
            "variables": {
                "organizationId": organizationId,
                "workspaceId": workspaceId,
                "modelId": modelId
            },
            "query": """query 
                getGANModels($organizationId: String, $workspaceId: String, $modelId: String) {
                    getGANModels(organizationId: $organizationId, workspaceId: $workspaceId, modelId: $modelId){
                        modelId
                        name
                        description
                    }
                }"""})
    return self.errorhandler(response, "getGANModels")


def getGANDataset(self, datasetId, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getGANDataset",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId
            },
            "query": """query 
                getGANDataset($workspaceId: String!, $datasetId: String!) {
                    getGANDataset(workspaceId: $workspaceId, datasetId: $datasetId) {
                        datasetId: datasetid
                        channelId
                        graphId: source
                        parentDataset: ganparent
                        modelId: ganmodelId
                        interpretations: scenarios
                        user
                        status
                        files
                        size
                        name
                        description
                    }
                }"""})
    return self.errorhandler(response, "getGANDataset")


def createGANDataset(self, modelId, datasetId, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createGANDataset",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId,
                "modelId": modelId,
            },
            "query": """mutation 
                createGANDataset($workspaceId: String!, $datasetId: String!, $modelId: String!) {
                    createGANDataset(workspaceId: $workspaceId, datasetId: $datasetId, modelId: $modelId)
                }"""})
    return self.errorhandler(response, "createGANDataset")


def deleteGANDataset(self, datasetId, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteGANDataset",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId
            },
            "query": """mutation 
                deleteGANDataset($workspaceId: String!, $datasetId: String!) {
                    deleteGANDataset(workspaceId: $workspaceId, datasetId: $datasetId)
                }"""})
    return self.errorhandler(response, "deleteGANDataset")


def createManagedGAN(self, organizationId, name, description, flags):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createManagedGAN",
            "variables": {
                "organizationId": organizationId,
                "name": name,
                "description": description,
                "flags": flags,
            },
            "query": """mutation 
                createManagedGAN($organizationId: String!, $name: String!, $description: String!, $flags: String) {
                    createManagedGAN(organizationId: $organizationId, name: $name, description: $description, flags: $flags){
                        modelId
                        url
                        fields {
                            key
                            bucket
                            algorithm
                            credential
                            date
                            token
                            policy
                            signature
                        }
                    }
                }"""})
    return self.errorhandler(response, "createManagedGAN")


def deleteGANModel(self, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteGANModel",
            "variables": {
                "modelId": modelId,
            },
            "query": """mutation 
                deleteGANModel($modelId: String!) {
                    deleteGANModel(modelId: $modelId)
                }"""})
    return self.errorhandler(response, "deleteGANModel")


def addGANAccess(self, organizationId, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "addGANAccess",
            "variables": {
                "organizationId": organizationId,
                "modelId": modelId,
            },
            "query": """mutation 
                addGANAccess($organizationId: String!, $modelId: String!) {
                    addGANAccess(organizationId: $organizationId, modelId: $modelId)
                }"""})
    return self.errorhandler(response, "addGANAccess")


def removeGANAccess(self, organizationId, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "removeGANAccess",
            "variables": {
                "organizationId": organizationId,
                "modelId": modelId,
            },
            "query": """mutation 
                removeGANAccess($organizationId: String!, $modelId: String!) {
                    removeGANAccess(organizationId: $organizationId, modelId: $modelId)
                }"""})
    return self.errorhandler(response, "removeGANAccess")

def getManagedGANs(self, organizationId, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getManagedGANs",
            "variables": {
                "organizationId": organizationId,
                "modelId": modelId
            },
            "query": """query 
                getManagedGANs($organizationId: String!, $modelId: String) {
                    getManagedGANs(organizationId: $organizationId, modelId: $modelId) {
                        createdAt
                        createdBy
                        description
                        modelId
                        name
                        organizationId
                        updatedAt
                        updatedBy
                    }
                }"""})
    return self.errorhandler(response, "getManagedGANs")

def editManagedGAN(self, modelId, name=None, description=None, flags=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "editManagedGAN",
            "variables": {
                "modelId": modelId,
                "name": name,
                "description": description,
                "flags": flags
            },
            "query": """mutation 
                editManagedGAN($modelId: String!, $name: String, $description: String, $flags: String) {
                    editManagedGAN(modelId: $modelId, name: $name, description: $description, flags: $flags)
                }"""})
    return self.errorhandler(response, "editManagedGAN")

def deleteManagedGAN(self, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteManagedGAN",
            "variables": {
                "modelId": modelId,
            },
            "query": """mutation 
                deleteManagedGAN($modelId: String!) {
                    deleteManagedGAN(modelId: $modelId)
                }"""})
    return self.errorhandler(response, "deleteManagedGAN")

def addGANOrganization(self, modelId, organizationId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "addGANOrganization",
            "variables": {
                "organizationId": organizationId,
                "modelId": modelId
            },
            "query": """mutation 
                addGANOrganization($organizationId: String!, $modelId: String!) {
                    addGANOrganization(organizationId: $organizationId, modelId: $modelId)
                }"""})
    return self.errorhandler(response, "addGANOrganization")


def removeGANOrganization(self, modelId, organizationId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "removeGANOrganization",
            "variables": {
                "organizationId": organizationId,
                "modelId": modelId
            },
            "query": """mutation 
                removeGANOrganization($organizationId: String!, $modelId: String!) {
                    removeGANOrganization(organizationId: $organizationId, modelId: $modelId)
                }"""})
    return self.errorhandler(response, "removeGANOrganization")