"""The client module is used for connecting to Rendered.ai's Platform API."""

envs = {
    'prod': {
        'name': 'Rendered.ai Platform',
        'url':  'https://deckard.rendered.ai',
        'api':  'https://api.rendered.ai/graphql' },
    'test': {
        'name': 'Rendered.ai Test Platform',
        'url':  'https://deckard-test.web.app',
        'api':  'https://api.test.rendered.ai/graphql' },
    'dev': {
        'name': 'Rendered.ai Development Platform',
        'url':  'https://deckard-dev-8eaa5.web.app',
        'api':  'https://api.dev.rendered.ai/graphql' },
    'infra': {
        'name': 'Rendered.ai Infrastructure Platform',
        'url':  'https://deckard-infra.web.app',
        'api':  'https://api.infra.rendered.ai/graphql' }
}


class client:

    def __init__(self, workspaceId=None, environment='prod', email=None, password=None, local=False, interactive=True, verbose=None):
        import getpass
        import time
        import os
        from anatools.anaclient.api import api
        self.verbose = verbose
        self.interactive = interactive
        if environment not in ['dev','test','prod','infra']:  print("Invalid environment argument, must be 'infra', 'dev', 'test' or 'prod'."); return
        if local:
            os.environ['NO_PROXY'] = '127.0.0.1'
            self.__url = 'http://127.0.0.1:3000'
            if interactive: print("Local is set to",self.__url)
        else: self.__url = envs[environment]['api']
        self.__password = password
        self.__logout = True
        self.email = email
        self.user = None
        self.organizations = {}
        self.workspaces ={}
        self.channels = {}
        self.volumes = {}
        self.organization = None

        self.ana_api = api(self.__url, None, self.verbose)
        if not self.email:
            print(f'Enter your credentials for the {envs[environment]["name"]}.') 
            self.email = input('Email: ')
        if not self.__password:
            failcount = 1
            while self.user is None:
                self.__password = getpass.getpass()
                self.user = self.ana_api.login(self.email, self.__password)
        if self.user is None:
            try: self.user = self.ana_api.login(self.email, self.__password)
            except: print(f'Failed to login to {envs[environment]["name"]} with email {self.email}.'); return
        if self.user is False: print(f'Failed to login to {envs[environment]["name"]} with email {self.email}.'); return
        if self.verbose == 'debug': print(f'{self.user["uid"]}\n{self.user["idtoken"]}')
        self.__logout = False
        self.ana_api = api(self.__url, {'uid':self.user['uid'], 'idtoken':self.user['idtoken']}, self.verbose)
        self.get_organizations()
        if len(self.organizations) == 0: print("No organizations available. Contact support@rendered.ai for support or fill out a form at https://rendered.ai/#contact."); return
        found_valid_org = False
        for organization in self.organizations:
            if organization['expired']:
                print("Warning!!!")
                print(f"    The subscription has expired for {organization['name']} organization (organizationId {organization['organizationId']}).") 
                print("    Update the subscription by signing into deckard.rendered.ai or contact sales@rendered.ai.")
            else:
                found_valid_org = True
        if not found_valid_org:
            print("Error: found no valid workspaces. If you believe this is a mistake, contact Rendered.ai at bugs@rendered.ai.")
            return
        self.get_workspaces()
        if len(self.workspaces) == 0: 
            self.workspace = None
            print("No workspaces available. Contact support@rendered.ai for support or fill out a form at https://rendered.ai/#contact."); 
            return
        self.get_channels()
        self.get_volumes()
        if workspaceId:     
            self.workspace = workspaceId
            for workspace in self.workspaces:
                if self.workspace == workspace['workspaceId']: self.organization = workspace['organizationId']
            if self.organization is None:
                print("The workspaceId provided is invalid. If you believe this is a mistake, contact support@rendered.ai for support or fill out a form at https://rendered.ai/#contact.")
                for workspace in self.workspaces: print(workspace["workspaceId"])
                self.workspace = None
                return
        else:
            self.workspace = self.workspaces[0]['workspaceId']
            self.organization = self.workspaces[0]['organizationId']
            if interactive: 
                print(f'These are your organizations and workspaces:')
                for organization in self.organizations:
                    print(f"    {organization['name']+' Organization'[:44]:<44}  {organization['organizationId']:<50}")
                    for workspace in self.workspaces:
                        if workspace["organizationId"] == organization["organizationId"]:
                            print(f"\t{workspace['name'][:40]:<40}  {workspace['workspaceId']:<50}")
        if interactive: 
            print(f'Signed into {envs[environment]["name"]} with {self.email}')
            print(f'The current organization is: {self.organization}')
            print(f'The current workspace is: {self.workspace}')


    def refresh_token(self):
        import time
        from anatools.anaclient.api import api
        if int(time.time()) > int(self.user['expires']):
            self.user = self.ana_api.login(self.email, self.__password)
            self.ana_api = api(self.__url, {'uid': self.user['uid'], 'idtoken': self.user['idtoken']}, self.verbose)


    def check_logout(self):
        if self.__logout: print('You are currently logged out, login to access the Rendered.ai Platform.'); return True
        self.refresh_token()
        return False


    def logout(self):
        """Logs out of the ana sdk and removes credentials from ana."""
        if self.check_logout(): return
        self.__logout = True
        del self.__password, self.__url, self.user


    def login(self, workspaceId=None, environment='prod', email=None, password=None, local=False, interactive=True, verbose=None):
        """Log in to the SDK. 
        
        Parameters
        ----------
        workspaceId: str
            ID of the workspace to log in to. Uses default if not specified.
        environment: str
            Environment to log into. Defaults to production.
        email: str
            Email for the login. Will prompt if not provided.
        password: str
            Password to login. Will prompt if not provided.
        local: bool
            Used for development to indicate pointing to local API.
        verbose: str
            Flag to turn on verbose logging. Use 'debug' to view log output.
        
        """
        self.__init__(workspaceId, environment, email, password, local, interactive, verbose)

    
    from .organizations import get_organization, set_organization, get_organizations, edit_organization, get_organization_members, get_organization_invites, add_organization_member, edit_organization_member, remove_organization_member, remove_organization_invitation ,get_organization_limits, set_organization_limit, get_organization_usage
    from .workspaces    import get_workspace, set_workspace, get_workspaces, create_workspace, edit_workspace, delete_workspace, get_workspace_guests, get_workspace_invites, add_workspace_guest, remove_workspace_guest, remove_workspace_invitation, get_workspace_limits, set_workspace_limit
    from .graphs        import get_staged_graphs, create_staged_graph, edit_staged_graph, delete_staged_graph, download_staged_graph, get_default_graph, set_default_graph
    from .datasets      import get_datasets, create_dataset, edit_dataset, delete_dataset, download_dataset, cancel_dataset, upload_dataset, get_dataset_runs, get_dataset_log
    from .channels      import get_channels, get_managed_channels, create_managed_channel, edit_managed_channel, delete_managed_channel, add_channel_access, remove_channel_access, build_managed_channel, deploy_managed_channel, get_deployment_status, get_channel_documentation, upload_channel_documentation
    from .volumes       import get_volumes, get_managed_volumes, create_managed_volume, edit_managed_volume, delete_managed_volume, add_volume_access, remove_volume_access, get_volume_data, download_volume_data, upload_volume_data, delete_volume_data, mount_volumes
    from .analytics     import get_analytics, get_analytics_types, create_analytics, delete_analytics
    from .annotations   import get_annotations, get_annotation_formats, get_annotation_maps, create_annotation, download_annotation, delete_annotation , get_managed_maps, create_managed_map, edit_managed_map, delete_managed_map, add_map_organization, remove_map_organization
    from .gan           import get_gan_models, get_gan_dataset, create_gan_dataset, delete_gan_dataset, create_managed_gan, delete_gan_model, add_gan_access, remove_gan_access, get_managed_gans, edit_managed_gan, delete_managed_gan, add_gan_organization, remove_gan_organization
    from .umap          import get_umap, create_umap, delete_umap
