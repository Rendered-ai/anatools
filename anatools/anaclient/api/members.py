"""
Members API calls.
"""

def getMembers(self, organizationId=None, workspaceId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getMembers",
            "variables": {
                "organizationId": organizationId,
                "workspaceId": workspaceId
            },
            "query": """query 
                getMembers($organizationId: String, $workspaceId: String) {
                    getMembers(organizationId: $organizationId, workspaceId: $workspaceId) {
                        organizationId
                        workspaceId
                        userId
                        email
                        name
                        role
                    }
                }"""})
    return self.errorhandler(response, "getMembers")

def getInvitations(self, organizationId=None, workspaceId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getInvitations",
            "variables": {
                "organizationId": organizationId,
                "workspaceId": workspaceId
            },
            "query": """query 
                getInvitations($organizationId: String, $workspaceId: String) {
                    getInvitations(organizationId: $organizationId, workspaceId: $workspaceId) {
                        invitationId
                        email
                        timestamp
                        organizationId
                        role
                        workspaceId
                    }
                }"""})
    return self.errorhandler(response, "getInvitations")


def addMember(self, email, role=None, organizationId=None, workspaceId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "addMember",
            "variables": {
                "organizationId": organizationId,
                "workspaceId": workspaceId,
                "email": email,
                "role": role
            },
            "query": """mutation 
                addMember($organizationId: String, $workspaceId: String, $email: String!, $role: String) {
                    addMember(organizationId: $organizationId, workspaceId: $workspaceId, email: $email, role: $role)
                }"""})
    return self.errorhandler(response, "addMember")


def removeMember(self, email, organizationId=None, workspaceId=None, invitationId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "removeMember",
            "variables": {
                "organizationId": organizationId,
                "workspaceId": workspaceId,
                "email": email,
                "invitationId":invitationId
            },
            "query": """mutation 
                removeMember($organizationId: String, $workspaceId: String, $email: String!, $invitationId: String) {
                    removeMember(organizationId: $organizationId, workspaceId: $workspaceId, email: $email, invitationId: $invitationId)
                }"""})
    return self.errorhandler(response, "removeMember")


def editMember(self, email, organizationId, role):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "editMember",
            "variables": {
                "organizationId": organizationId,
                "email": email,
                "role": role
            },
            "query": """mutation 
                editMember($organizationId: String!, $email: String!, $role: String!) {
                    editMember(organizationId: $organizationId, email: $email, role: $role)
                }"""})
    return self.errorhandler(response, "editMember")
