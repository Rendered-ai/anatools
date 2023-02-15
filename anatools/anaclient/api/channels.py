"""
Channels API calls.
"""

def getChannels(self, organizationId=None, workspaceId=None, channelId=None, verbose=False):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getChannels",
            "variables": {
                "organizationId": organizationId,
                "workspaceId": workspaceId,
                "channelId": channelId
            },
            "query": """query 
                getChannels($organizationId: String, $workspaceId: String, $channelId: String) {
                    getChannels(organizationId: $organizationId, workspaceId: $workspaceId, channelId: $channelId) {
                        channelId
                        name
                        description
                        organizationId
                        organization
                        createdAt
                        updatedAt
                    }
                }"""})
    return self.errorhandler(response, "getChannels")


def getManagedChannels(self, organizationId, channelId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getManagedChannels",
            "variables": {
                "organizationId": organizationId,
                "channelId": channelId
            },
            "query": """query 
                getManagedChannels($organizationId: String!, $channelId: String) {
                    getManagedChannels(organizationId: $organizationId, channelId: $channelId) {
                        channelId
                        organizationId
                        name
                        instanceType
                        volumes
                        timeout
                        interfaceVersion
                        createdAt
                        updatedAt
                        organizations {
                            organizationId
                            name
                        }
                    }
                }"""})
    return self.errorhandler(response, "getManagedChannels")


def getChannelDeployment(self, deploymentId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getChannelDeployment",
            "variables": {
                "deploymentId": deploymentId
            },
            "query": """query 
                getChannelDeployment($deploymentId: String!) {
                    getChannelDeployment(deploymentId: $deploymentId) {
                        deploymentId
                        channelId
                        status {
                            state
                            step
                            message
                        }
                        createdBy
                        createdAt
                        updatedAt
                    }
                }"""})
    return self.errorhandler(response, "getChannelDeployment")


def createManagedChannel(self, organizationId, name, description=None, volumes=None, instance=None, timeout=None, interfaceVersion=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createManagedChannel",
            "variables": {
                "organizationId": organizationId,
                "name": name,
                "description": description,
                "volumes": volumes,
                "instance": instance,
                "timeout": timeout,
                "interfaceVersion": interfaceVersion
            },
            "query": """mutation 
                createManagedChannel($organizationId: String!, $name: String!, $description: String, $volumes: [String], $instance: String, $timeout: Int, $interfaceVersion: Int) {
                    createManagedChannel(organizationId: $organizationId, name: $name, description: $description, volumes: $volumes, instance: $instance, timeout: $timeout, interfaceVersion: $interfaceVersion)
                }"""})
    return self.errorhandler(response, "createManagedChannel")


def deleteManagedChannel(self, channelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteManagedChannel",
            "variables": {
                "channelId": channelId
            },
            "query": """mutation 
                deleteManagedChannel($channelId: String!) {
                    deleteManagedChannel(channelId: $channelId)
                }"""})
    return self.errorhandler(response, "deleteManagedChannel")


def editManagedChannel(self, channelId, name=None, description=None, volumes=None, instance=None, timeout=None, status=None, interfaceVersion=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "editManagedChannel",
            "variables": {
                "channelId": channelId,
                "name": name,
                "description": description,
                "volumes": volumes,
                "instance": instance,
                "timeout": timeout,
                "status":status,
                "interfaceVersion": interfaceVersion
            },
            "query": """mutation 
                editManagedChannel($channelId: String!, $name: String, $description: String, $volumes: [String], $instance: String, $timeout: Int, $status: String, $interfaceVersion: Int) {
                    editManagedChannel(channelId: $channelId, name: $name, description: $description, volumes: $volumes, instance: $instance, timeout: $timeout, status: $status, interfaceVersion: $interfaceVersion)
                }"""})
    return self.errorhandler(response, "editManagedChannel")


def addChannelOrganization(self, channelId, organizationId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "addChannelOrganization",
            "variables": {
                "channelId": channelId,
                "organizationId": organizationId
            },
            "query": """mutation 
                addChannelOrganization($channelId: String!, $organizationId: String!) {
                    addChannelOrganization(channelId: $channelId, organizationId: $organizationId)
                }"""})
    return self.errorhandler(response, "addChannelOrganization")


def removeChannelOrganization(self, channelId, organizationId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "removeChannelOrganization",
            "variables": {
                "channelId": channelId,
                "organizationId": organizationId
            },
            "query": """mutation 
                removeChannelOrganization($channelId: String!, $organizationId: String!) {
                    removeChannelOrganization(channelId: $channelId, organizationId: $organizationId)
                }"""})
    return self.errorhandler(response, "removeChannelOrganization")


def deployManagedChannel(self, channelId, alias=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deployManagedChannel",
            "variables": {
                "channelId": channelId,
                "alias": alias
            },
            "query": """mutation 
                deployManagedChannel($channelId: String!, $alias: String) {
                    deployManagedChannel(channelId: $channelId, alias: $alias) {
                        deploymentId
                        ecrEndpoint
                        ecrPassword
                    }
                }"""})
    return self.errorhandler(response, "deployManagedChannel")


def setChannelGraph(self, channelId, workspaceId, graphId=None, stagedGraphId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers,
        json = {
            "operationName": "setChannelGraph",
            "variables": {
                "channelId": channelId,
                "workspaceId": workspaceId,
                "graphId": graphId,
                "stagedGraphId": stagedGraphId
            },
            "query": """mutation 
                setChannelGraph($channelId: String!, $workspaceId: String!, $graphId: String, $stagedGraphId: String) {
                    setChannelGraph(channelId: $channelId, workspaceId: $workspaceId, graphId: $graphId, stagedGraphId: $stagedGraphId)
                }"""})
    return self.errorhandler(response, "setChannelGraph")

    
def getChannelDocumentation(self, channelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers,
        json = {
            "operationName": "getChannelDocumentation",
            "variables": {
                "channelId": channelId
            },
            "query": """query getChannelDocumentation($channelId: String!) {
                getChannelDocumentation(channelId: $channelId) {
                    markdown
                }
            }"""})
    return self.errorhandler(response, "getChannelDocumentation")


def uploadChannelDocumentation(self, channelId, keys=[]):
    response = self.session.post(
        url = self.url, 
        headers = self.headers,
        json = {
            "operationName": "uploadChannelDocumentation",
            "variables": {
                "channelId": channelId,
                "keys": keys,
            },
            "query": """mutation uploadChannelDocumentation($channelId: String!, $keys: [String]!) {
                uploadChannelDocumentation(channelId: $channelId, keys: $keys) {
                    key
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
    return self.errorhandler(response, "uploadChannelDocumentation")