"""
Volumes API calls.
"""

def getVolumes(self, organizationId=None, volumeId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getVolumes",
            "variables": {
                "organizationId": organizationId,
                "volumeId": volumeId
            },
            "query": """query 
                getVolumes($organizationId: String, $volumeId: String) {
                    getVolumes(organizationId: $organizationId, volumeId: $volumeId) {
                        volumeId
                        name
                        description
                        organization
                        organizationId
                        permission
                        createdAt
                        updatedAt
                    }
                }"""})
    return self.errorhandler(response, "getVolumes")


def getManagedVolumes(self, organizationId, volumeId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getManagedVolumes",
            "variables": {
                "organizationId": organizationId,
                "volumeId": volumeId
            },
            "query": """query 
                getManagedVolumes($organizationId: String, $volumeId: String) {
                    getManagedVolumes(organizationId: $organizationId, volumeId: $volumeId) {
                        volumeId
                        organizationId
                        name
                        description
                        createdAt
                        updatedAt
                        organizations {
                            organizationId
                            name
                        }
                    }
                }"""})
    return self.errorhandler(response, "getManagedVolumes")


def getVolumeData(self, volumeId, keys=[], dir=None, offset=None, limit=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getVolumeData",
            "variables": {
                "volumeId": volumeId,
                "keys": keys,
                "dir": dir,
                "offset": offset,
                "limit": limit
            },
            "query": """query 
                getVolumeData($volumeId: String!, $keys: [String], $dir: String, $limit: Int, $offset: Int) {
                    getVolumeData(volumeId: $volumeId, keys: $keys, dir: $dir, limit: $limit, offset: $offset){
                        keys {
                            key
                            size
                            updatedAt
                            hash
                            url
                        }
                        pageInfo {
                            totalItems
                            offset
                            limit
                        }
                    }
                }"""})
    return self.errorhandler(response, "getVolumeData")


def createManagedVolume(self, organizationId, name, description=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createManagedVolume",
            "variables": {
                "organizationId": organizationId,
                "name": name,
                "description": description
            },
            "query": """mutation 
                createManagedVolume($organizationId: String!, $name: String!, $description: String) {
                    createManagedVolume(organizationId: $organizationId, name: $name, description: $description)
                }"""})
    return self.errorhandler(response, "createManagedVolume")


def deleteManagedVolume(self, volumeId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteManagedVolume",
            "variables": {
                "volumeId": volumeId,
            },
            "query": """mutation 
                deleteManagedVolume($volumeId: String!) {
                    deleteManagedVolume(volumeId: $volumeId)
                }"""})
    return self.errorhandler(response, "deleteManagedVolume")


def editManagedVolume(self, volumeId, name=None, description=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "editManagedVolume",
            "variables": {
                "volumeId": volumeId,
                "name": name,
                "description": description
            },
            "query": """mutation 
                editManagedVolume($volumeId: String!, $name: String, $description: String) {
                    editManagedVolume(volumeId: $volumeId, name: $name, description: $description)
                }"""})
    return self.errorhandler(response, "editManagedVolume")


def addVolumeOrganization(self, volumeId, organizationId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "addVolumeOrganization",
            "variables": {
                "volumeId": volumeId,
                "organizationId": organizationId
            },
            "query": """mutation 
                addVolumeOrganization($volumeId: String!, $organizationId: String!) {
                    addVolumeOrganization(volumeId: $volumeId, organizationId: $organizationId)
                }"""})
    return self.errorhandler(response, "addVolumeOrganization")


def removeVolumeOrganization(self, volumeId, organizationId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "removeVolumeOrganization",
            "variables": {
                "volumeId": volumeId,
                "organizationId": organizationId
            },
            "query": """mutation 
                removeVolumeOrganization($volumeId: String!, $organizationId: String!) {
                    removeVolumeOrganization(volumeId: $volumeId, organizationId: $organizationId)
                }"""})
    return self.errorhandler(response, "removeVolumeOrganization")


def putVolumeData(self, volumeId, keys=[]):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "putVolumeData",
            "variables": {
                "volumeId": volumeId,
                "keys": keys
            },
            "query": """mutation 
                putVolumeData($volumeId: String!, $keys: [String]!) {
                    putVolumeData(volumeId: $volumeId, keys: $keys){
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
    return self.errorhandler(response, "putVolumeData")


def deleteVolumeData(self, volumeId, keys=[]):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteVolumeData",
            "variables": {
                "volumeId": volumeId,
                "keys": keys
            },
            "query": """mutation 
                deleteVolumeData($volumeId: String!, $keys: [String]!) {
                    deleteVolumeData(volumeId: $volumeId, keys: $keys)
                }"""})
    return self.errorhandler(response, "deleteVolumeData")


def mountVolumes(self, volumes):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "mountVolumes",
            "variables": {
                "volumes": volumes
            },
            "query": """mutation 
                mountVolumes($volumes: [String]!) {
                    mountVolumes(volumes: $volumes){
                        keys
                        rw
                        credentials {
                            accesskeyid
                            accesskey
                            sessiontoken
                        }
                    }
                }"""})
    return self.errorhandler(response, "mountVolumes")