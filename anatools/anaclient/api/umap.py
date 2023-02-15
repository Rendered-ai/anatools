"""
GAN API calls.
"""

def getUMAP(self, umapId, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getUMAP",
            "variables": {
                "workspaceId": workspaceId,
                "umapId": umapId
            },
            "query": """query 
                getUMAP($workspaceId: String!, $umapId: String) {
                    getUMAP(workspaceId: $workspaceId, umapId: $umapId){
                        datasets
                        samples
                        seed
                        status
                        results {
                            id
                            featuresize
                            datasets {
                                datasetId
                                datasetName
                                points {
                                    image
                                    x
                                    y
                                    z
                                }
                            }
                        }
                    }
                }"""})
    return self.errorhandler(response, "getUMAP")


def createUMAP(self, datasetIds, samples, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createUMAP",
            "variables": {
                "workspaceId": workspaceId,
                "datasetIds": datasetIds,
                "samples": samples
            },
            "query": """query 
                createUMAP($workspaceId: String!, $datasetIds: [String]!, $samples: [Int]!) {
                    createUMAP(workspaceId: $workspaceId, datasetIds: $datasetIds, samples: $samples)
                }"""})
    return self.errorhandler(response, "createUMAP")


def deleteUMAP(self, umapId, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteUMAP",
            "variables": {
                "workspaceId": workspaceId,
                "umapId": umapId,
            },
            "query": """mutation 
                deleteUMAP($workspaceId: String!, $umapId: String!) {
                    deleteUMAP(workspaceId: $workspaceId, umapId: $umapId)
                }"""})
    return self.errorhandler(response, "deleteUMAP")

