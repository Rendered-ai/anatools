"""
Workspace Functions
"""
    
def get_workspace(self):
    """Get Workspace ID of current workspace. 
    
    Returns
    -------
    str
        Workspace ID of current workspace.
    """
    if self.check_logout(): return
    return self.workspace


def set_workspace(self, workspaceId):
    """Set the workspace to the one you wish to work in.
    
    Parameters
    ----------
    workspaceId : str
        Workspace ID for the workspace you wish to work in.
    """
    if self.check_logout(): return
    if workspaceId is None: raise Exception('WorkspaceId must be specified.')
    workspaceSet = False
    self.workspaces = self.ana_api.getWorkspaces()
    for workspace in self.workspaces:
        if workspaceId == workspace['workspaceId']:
            self.workspace = workspace['workspaceId']
            self.organization = workspace['organizationId']
            workspaceSet = True
            break
    if not workspaceSet: raise Exception('Could not find workspace specified.')
    print(f'Organization set to {self.organization}.')
    print(f'Workspace set to {self.workspace}.')
    return


def get_workspaces(self, organizationId=None, workspaceId=None):
    """Shows list of workspaces with id, name, and owner data.
    
    Parameters
    ----------
    organizationId : str
        Organization ID to filter on. Optional
    workspaceId : str
        Workspace ID to filter on. Optional

    Returns
    -------
    list[dict]
        Workspace data for all workspaces for a user.
    """  
    if self.check_logout(): return
    if organizationId is None and workspaceId is None:
        self.workspaces = self.ana_api.getWorkspaces(organizationId, workspaceId)
        return self.workspaces
    else:
        workspaces = self.ana_api.getWorkspaces(organizationId, workspaceId)
        return workspaces


def create_workspace(self, name, channelIds=[], volumeIds=[], code=None):
    """Create a new workspace with specific channels.
    
    Parameters
    ----------
    name : str    
        New workspace name.
    channelIds : list[str]
        List of channel ids to add to workspace.
    volumeIds: list[str]
        List of volume ids that the workspace will have access to.
    code: str
        Content code that used for creating a workspace
    
    Returns
    -------
    str
        Workspace ID if creation was successful. Otherwise returns message.
    """    
    if self.check_logout(): return
    if name is None: raise ValueError("Name must be provided")
    if code is None: code = ''
    return self.ana_api.createWorkspace(organizationId=self.organization, name=name, channelIds = channelIds, volumeIds = volumeIds, code=code)


def delete_workspace(self, workspaceId=None, prompt=True):
    """Delete an existing workspace. 
    
    Parameters
    ----------
    workspaceId : str    
        Workspace ID for workspace to get deleted. Deletes current workspace if not specified. 
    prompt: bool
        Set to True if avoiding prompts for deleting workspace.
    
    Returns
    -------
    str
        Success or failure message if workspace was sucessfully removed.
    """
    if self.check_logout(): return
    if workspaceId is None: workspaceId = self.workspace 
    if prompt:
        response = input('This will remove any configurations, graphs and datasets associated with this workspace.\nAre you certain you want to delete this workspace? (y/n)  ')
        if response not in ['Y', 'y', 'Yes', 'yes']: return
    return self.ana_api.deleteWorkspace(workspaceId=workspaceId)


def edit_workspace(self, name=None, channelIds=None, volumeIds=None, ganIds=None, mapIds=None, workspaceId=None):
    """Edit workspace information. 
    
    Parameters
    ----------
    name : str    
        New name to replace old one.
    channelIds: list[str]
        Names of channels that the workspace will have access to.
    volumeIds: list[str]
        List of volume ids that the workspace will have access to.
    ganIds: list[str]
        List of GAN ids that the workspace will have access to.
    mapIds: list[str]
        List of map ids that the workspace will have access to.
    workspaceId : str    
        Workspace ID for workspace to update.
    
    Returns
    -------
    bool
        Success or failure message if workspace was sucessfully updated.
    """  
    if self.check_logout(): return
    if name is None and channelIds is None and volumeIds is None and ganIds is None and mapIds is None: return
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.editWorkspace(workspaceId=workspaceId, name=name, channelIds=channelIds, volumeIds=volumeIds, ganIds=ganIds, mapIds=mapIds)


def get_workspace_guests(self, workspaceId=None):
    """Get guests of a workspace. Uses default workspace if not specified.
    
    Parameters
    ----------
    workspaceId : str
        Workspace Id. Optional.
    
    Returns
    -------
    list[dict]
        Information about guests of an workspace.
    """
    if self.check_logout(): return
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.getMembers(workspaceId=workspaceId)

def get_workspace_invites(self, workspaceId=None):
    """Get invitations of a workspace. Uses default workspace if not specified.
    
    Parameters
    ----------
    workspaceId : str
        Workspace Id. Optional.
    
    Returns
    -------
    list[dict]
        Information about invitations of an workspace.
    """
    if self.check_logout(): return
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.getInvitations(workspaceId=workspaceId)


def add_workspace_guest(self, email, workspaceId=None):
    """Add a guest to an existing workspace.
    
    Parameters
    ----------
    email: str
        Email of guest to add.
    workspaceId : str    
        Workspace ID to add a guest to. Uses current if not specified.
    
    Returns
    -------
    str
        Response status if guest got added to workspace succesfully. 
    """
    if self.check_logout(): return
    if email is None: raise ValueError("Email must be provided.")
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.addMember(email=email, role=None, organizationId=None, workspaceId=workspaceId)


def remove_workspace_guest(self, email, workspaceId=None):
    """Remove a guest from an existing workspace.
    
    Parameters
    ----------
    email : str
        Guest email to remove.
    workspaceId : str    
        Workspace ID to remove guest from. Removes from current workspace if not specified. 
    
    Returns
    -------
    str
        Response status if guest got removed from workspace succesfully. 
    """
    if self.check_logout(): return
    if email is None: raise ValueError("Email must be provided.")
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.removeMember(email=email, organizationId=None, workspaceId=workspaceId)

def remove_workspace_invitation(self, email, workspaceId=None, invitationId=None ):
    """Remove a invitation from an existing organization.
    
    Parameters
    ----------
    email : str
        Invitation email to remove.
    workspaceId: str
        Workspace ID to remove member from. Removes from current organization if not specified.
    inviteId: str
        Invitation ID to remove invitation from. Removes from current organization if not specified.
    
    Returns
    -------
    str
        Response status if member got removed from organization succesfully. 
    """
    if self.check_logout(): return
    if email is None: raise ValueError("Email must be provided.")
    if invitationId is None: raise ValueError("No invitation found.")
    if workspaceId is None: workspaceId = self.organization
    return self.ana_api.removeMember(email=email, workspaceId=workspaceId, organizationId=None, invitationId=invitationId)


def get_workspace_limits(self, setting=None, workspaceId=None):
    """Get information about Workspace limits and settings.

    Parameters
    ----------
    setting : str
        Setting name.
    workspaceId : str
        Workspace ID. Defaults to current if not specified.
    
    Returns
    -------
    list[dict]
        Workspace limit information.
    """
    if self.check_logout(): return
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.getWorkspaceLimits(workspaceId=workspaceId, setting=setting)


def set_workspace_limit(self, setting, limit, workspaceId=None):
    """Set a limit for a workspace.

    Parameters
    ----------
    setting : str
        Setting name.
    limit : int
        Limit to set at.
    workspaceId : str
        Workspace ID. Defaults to current if not specified.
    
    Returns
    -------
    list[dict]
        Workspace limit information.
    """
    if self.check_logout(): return
    if setting is None: raise("Setting must be provided.")
    if limit is None: raise("Limit must be provided.")
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.setWorkspaceLimit(workspaceId=workspaceId, setting=setting, limit=limit)

