"""
Annotations API calls.
"""

def getAnnotations(self, workspaceId, datasetId, annotationId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getAnnotations",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId,
                "annotationId": annotationId,
            },
            "query": """query 
                getAnnotations($workspaceId: String!, $datasetId: String! $annotationId: String!) {
                    getAnnotations(workspaceId: $workspaceId, datasetId: $datasetId, annotationId: $annotationId){
                        workspaceId
                        datasetId
                        annotationId
                        map
                        format
                        status
                    }
                }"""})
    return self.errorhandler(response, "getAnnotations")


def getAnnotationFormats(self):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getAnnotationFormats",
            "variables": {},
            "query": """query 
                getAnnotationFormats{
                    getAnnotationFormats
                }"""})
    return self.errorhandler(response, "getAnnotationFormats")


def getAnnotationMaps(self, organizationId, workspaceId, mapId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getAnnotationMaps",
            "variables": {
                "organizationId": organizationId,
                "workspaceId": workspaceId,
                "mapId": mapId
            },
            "query": """query 
                getAnnotationMaps($organizationId: String, $workspaceId: String, $mapId: String) {
                    getAnnotationMaps(organizationId: $organizationId, workspaceId: $workspaceId, mapId: $mapId) {
                        description
                        mapId
                        name
                        organization
                        organizationId
                        updatedAt
                    }
                }"""})
    return self.errorhandler(response, "getAnnotationMaps")

def getManagedMaps(self, organizationId, mapId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getManagedMaps",
            "variables": {
                "organizationId": organizationId,
                "mapId": mapId
            },
            "query": """query 
                getManagedMaps($organizationId: String!, $mapId: String) {
                    getManagedMaps(organizationId: $organizationId, mapId: $mapId) {
                        createdAt
                        createdBy
                        description
                        mapId
                        name
                        organizationId
                        updatedAt
                        updatedBy
                    }
                }"""})
    return self.errorhandler(response, "getManagedMaps")


def createAnnotation(self, workspaceId, datasetId, format, map):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createAnnotation",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId,
                "format": format,
                "map": map
            },
            "query": """mutation 
                createAnnotation($workspaceId: String!, $datasetId: String!, $format: String!, $map: String!) {
                    createAnnotation(workspaceId: $workspaceId, datasetId: $datasetId, format: $format, map: $map)
                }"""})
    return self.errorhandler(response, "createAnnotation")


def downloadAnnotation(self, workspaceId, datasetId, annotationId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "downloadAnnotation",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId,
                "annotationId": annotationId
            },
            "query": """mutation 
                downloadAnnotation($workspaceId: String!, $datasetId: String!, $annotationId: String!) {
                    downloadAnnotation(workspaceId: $workspaceId, datasetId: $datasetId, annotationId: $annotationId)
                }"""})
    return self.errorhandler(response, "downloadAnnotation")


def deleteAnnotation(self, workspaceId, annotationId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteAnnotation",
            "variables": {
                "workspaceId": workspaceId,
                "annotationId": annotationId
            },
            "query": """mutation 
                deleteAnnotation($workspaceId: String!, $annotationId: String!) {
                    deleteAnnotation(workspaceId: $workspaceId, annotationId: $annotationId)
                }"""})
    return self.errorhandler(response, "deleteAnnotation")

def createManagedMap(self, organizationId, name, description):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createManagedMap",
            "variables": {
                "organizationId": organizationId,
                "name": name,
                "description": description
            },
            "query": """mutation 
                createManagedMap($organizationId: String!, $name: String!, $description: String) {
                    createManagedMap(organizationId: $organizationId, name: $name, description: $description){
                        mapId
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
    return self.errorhandler(response, "createManagedMap")

def editManagedMap(self, mapId, name=None, description=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "editManagedMap",
            "variables": {
                "mapId": mapId,
                "name": name,
                "description": description
            },
            "query": """mutation 
                editManagedMap($mapId: String!, $name: String, $description: String) {
                    editManagedMap(mapId: $mapId, name: $name, description: $description)
                }"""})
    return self.errorhandler(response, "editManagedMap")

def deleteManagedMap(self, mapId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteManagedMap",
            "variables": {
                "mapId": mapId,
            },
            "query": """mutation 
                deleteManagedMap($mapId: String!) {
                    deleteManagedMap(mapId: $mapId)
                }"""})
    return self.errorhandler(response, "deleteManagedMap")

def addMapOrganization(self, mapId, organizationId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "addMapOrganization",
            "variables": {
                "organizationId": organizationId,
                "mapId": mapId
            },
            "query": """mutation 
                addMapOrganization($organizationId: String!, $mapId: String!) {
                    addMapOrganization(organizationId: $organizationId, mapId: $mapId)
                }"""})
    return self.errorhandler(response, "addMapOrganization")


def removeMapOrganization(self, mapId, organizationId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "removeMapOrganization",
            "variables": {
                "organizationId": organizationId,
                "mapId": mapId
            },
            "query": """mutation 
                removeMapOrganization($organizationId: String!, $mapId: String!) {
                    removeMapOrganization(organizationId: $organizationId, mapId: $mapId)
                }"""})
    return self.errorhandler(response, "removeMapOrganization")