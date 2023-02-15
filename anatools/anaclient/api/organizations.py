"""
Organizations API calls.
"""

def getOrganizations(self, organizationId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getOrganizations",
            "variables": {
                "organizationId": organizationId
            },
            "query": """query 
                getOrganizations($organizationId: String) {
                    getOrganizations(organizationId: $organizationId) {
                        organizationId
                        name
                        role
                        expired
                        expirationDate
                    }
                }"""})
    return self.errorhandler(response, "getOrganizations")


def editOrganization(self, organizationId, name):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "editOrganization",
            "variables": {
                "organizationId": organizationId,
                "name": name
            },
            "query": """mutation 
                editOrganization($organizationId: String!, $name: String!) {
                    editOrganization(organizationId: $organizationId, name: $name) 
                }"""})
    return self.errorhandler(response, "editOrganization")
