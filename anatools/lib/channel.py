# Copyright 2019-2022 DADoES, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the root directory in the "LICENSE" file or at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import yaml
import glob
import logging
import os
import sys
import importlib
from pathlib import Path
import anatools
import anatools.lib.context as ctx

logger = logging.getLogger(__name__)


def find_channelfile():
    channel = None
    channelfiles = []
    # search local directory
    localfiles = [file for file in os.listdir('.') if file.endswith('.yml') or file.endswith('.yaml') ]
    for file in localfiles: channelfiles.append(file)
    # search workspace directory (devcontainer)
    if os.path.exists('/workspaces'):
        workspaces = os.listdir('/workspaces')
        for workspace in workspaces: 
            workspacefiles = [f'/workspaces/{workspace}/{file}' for file in os.listdir(f'/workspaces/{workspace}') if file.endswith('.yml') or file.endswith('.yaml') ]
            for file in workspacefiles: channelfiles.append(file)
    # search ana directory (deployed)
    if os.path.exists('/ana'):
        anafiles = [f'/ana/{file}' for file in os.listdir(f'/ana') if file.endswith('.yml') or file.endswith('.yaml') ]
        for file in anafiles: channelfiles.append(file)
    for channelfile in channelfiles:
        with open(channelfile, 'r') as f:
            cfg = yaml.safe_load(f)
            # if it adds packages then assume it's a channel file
            if "add_packages" in cfg:
                channel = channelfile
                print(f'Using channelfile found at {channel}.\nIf this is the wrong channel, specify a channelfile using the --channel argument.')
                break
    return channel

def get_schema_files(package_name):
    ''' Return a list of all schema files in the package '''
    try:
        package = importlib.import_module(package_name)
    except:
        logger.critical(f"Error importing package {package_name}")
        sys.exit(1)
 
    package_init = package.__file__
    if package_init is None:
        logger.critical(f"Package {package.__name__} is missing __init__.py")
        raise ValueError
    package_dir = os.path.dirname(os.path.realpath(package_init))
    node_dir = os.path.join(package_dir, "nodes")
    schema_files = []
    if os.path.isdir(node_dir):
        schema_files = glob.glob(os.path.join(node_dir, "*.yml"))
    return schema_files

class Channel:
    console_logging_configured = False
    logfile_logging_configured = False
    def __init__(self, channel_file):
        """ Create a channel class from a channel file """
        self.classes = {}
        self.schemas = {}
        self.packages = {}
        self.type = "blender" # assume it's a blender channel unless otherwise specified

        # get directory where ana is installed
        ana_init = anatools.__file__
        self.ana_package_dir = os.path.dirname(os.path.realpath(ana_init))

        # default execution flags
        self.execution_flags = {
            "--channel": "channel.yml",
            "--graph": "graphs/default.yml",
            "--loglevel": "ERROR",
            "--logfile": None,
            "--seed": None,
            "--interp_num": 0,
            "--preview": False,
            "--output": "./output",
            "--data": "./data"
        }

        # default channel settings
        self.channel_settings = {
            "type": "blender"
        }

        # get an ordered list of the channel files to load
        done = False
        channel_file_list = [channel_file]
        while not done:
            with open(channel_file, 'r') as f:
                cfg = yaml.safe_load(f)

            if "channel" in cfg and "base" in cfg["channel"]:
                channel_file = cfg["channel"]["base"]
                channel_file_list.append(channel_file)
            else:
                done = True
        channel_file_list.reverse()

        # process channel files in order
        channel_settings = {
            "type": "blender",
        }
        add_setup_modules = []
        remove_setup_modules = []
        add_packages = []
        remove_packages = []
        add_nodes = []
        remove_nodes = []
        rename_nodes = []
        for channel_file in channel_file_list:
            with open(channel_file, 'r') as f:
                cfg = yaml.safe_load(f)
            if "channel" in cfg:
                channel_settings = {**channel_settings, **cfg["channel"]}
            if "add_setup" in cfg:
                add_setup_modules.extend(cfg["add_setup"])
            if "remove_setup" in cfg:
                remove_setup_modules.extend(cfg["remove_setup"])
            if "add_packages" in cfg:
                add_packages.extend(cfg["add_packages"])
            if "remove_packages" in cfg:
                remove_packages.extend(cfg["remove_packages"])
            if "add_nodes" in cfg:
                add_nodes.extend(cfg["add_nodes"])
            if "remove_nodes" in cfg:
                remove_nodes.extend(cfg["remove_nodes"])
            if "rename_nodes" in cfg:
                rename_nodes.extend(cfg["rename_nodes"])
            if "default_execution_flags" in cfg:
                # channel file defaults take precedence
                self.execution_flags = {**self.execution_flags, **cfg["default_execution_flags"]}

        # save channel settings
        self.type = channel_settings["type"]

        # remove setup modules
        for remove_setup_module in remove_setup_modules:
            found = False
            for i, setup_module in enumerate(add_setup_modules):
                if remove_setup_module == setup_module:
                    add_setup_modules.pop(i)
                    found = True
                    break
            if not found:
                logger.critical(f"Can't remove setup module {remove_setup_module}. Not found.")
                raise ValueError
        self.setup_modules = add_setup_modules

        # remove packages
        for remove_package in remove_packages:
            found = False
            for i, add_package in enumerate(add_packages):
                if remove_package == add_package:
                    add_packages.pop(i)
                    found = True
                    break
            if not found:
                logger.critical(f"Can't remove package {remove_package}. Not found.")
                raise ValueError
        
        # import packages
        package_list = []
        for package in add_packages:
            if package not in package_list:
                package_list.append(package)
                schema_files = get_schema_files(package)
                
                # load schemas and save class info
                for schema_file in schema_files:
                    try:
                        with open(schema_file, "r") as f:
                            schema_module = yaml.safe_load(f)
                    except:
                        logger.critical(f"Error reading schema '{schema_file}'")
                        raise
                    python_module = package + ".nodes." + Path(schema_file).stem
                    for schema in schema_module["schemas"]:
                        alias = schema_module["schemas"][schema].get("alias", schema)
                        self.schemas[alias] = schema_module["schemas"][schema]
                        self.classes[alias] = {
                            "module": python_module,
                            "class": schema
                    }

        # add nodes
        for node_dict in add_nodes:
            node_name = node_dict["name"]
            package = node_dict["package"]
            if package not in package_list:
                package_list.append(package)
            alias = node_dict.get("alias", None)
            category = node_dict.get("category", None)
            subcategory = node_dict.get("subcategory", None)
            color = node_dict.get("color", None)
            # get all the schema files in the package
            schema_files = get_schema_files(package)
            if len(schema_files) == 0:
                logger.critical(f"Schema for '{node_name}' not found")
                raise ValueError
            
            # search all schemas in the package for the node name
            found = False
            for schema_file in schema_files:
                try:
                    with open(schema_file, "r") as f:
                        schema_module = yaml.safe_load(f)
                except:
                    logger.critical(f"Error reading schema '{schema_file}'")
                    raise
                for schema in schema_module["schemas"]:
                    if schema == node_name:
                        python_module = package + ".nodes." + Path(schema_file).stem
                        # check if schema file included an alias
                        original_alias = schema_module["schemas"][schema].get("alias", node_name)
                        if alias is None: alias = original_alias
                        if category: schema_module["schemas"][schema]['category'] = category
                        if subcategory: schema_module["schemas"][schema]['subcategory'] = subcategory
                        if color: schema_module["schemas"][schema]['color'] = color
                        self.schemas[alias] = schema_module["schemas"][schema]
                        self.classes[alias] = {
                            "module": python_module,
                            "class": schema
                        }
                        found = True
                        break
                if found:
                    break
            if not found:
                logger.critical(f"Schema for '{node_name}' not found")
                raise ValueError

        # remove nodes
        for node_name in remove_nodes:
            self.schemas.pop(node_name)
            self.classes.pop(node_name)

        # rename node
        for rename_dict in rename_nodes:
            old_name = rename_dict["old_name"]
            new_name = rename_dict["new_name"]
            if old_name not in self.schemas:
                logger.critical(f"Can't rename node - '{old_name}' not found.")
                raise ValueError
            self.schemas[new_name] = self.schemas.pop(old_name)
            self.classes[new_name] = self.classes.pop(old_name)

        # read package configurations
        for package_name in package_list:
            package = importlib.import_module(package_name)
            package_init = package.__file__
            package_dir = os.path.dirname(os.path.realpath(package_init))
            package_config_file = os.path.join(package_dir, "package.yml")
            if os.path.exists(package_config_file):
                with open(package_config_file, "r") as f:
                    self.packages[package_name] = yaml.safe_load(f)
            else:
                self.packages[package_name] = {}

        # construct the node menu
        if "node_menu" in cfg:
            self.node_menu = cfg["node_menu"]
        else:
            self.node_menu = None

        self.name = os.path.splitext(os.path.basename(channel_file))[0]

    @classmethod
    def configure_logging(cls, loglevel="ERROR", logfile=None, logfile_mode="w"):

        # set up logging
        rootLogger = logging.getLogger()
        numeric_level = getattr(logging, loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: {}'.format(loglevel))
        rootLogger.setLevel(numeric_level)
        formatter = logging.Formatter(
            '%(asctime)s %(name)s %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        # log to file
        if not Channel.logfile_logging_configured and logfile is not None:
            fileHandler = logging.FileHandler(logfile, mode=logfile_mode)
            fileHandler.setFormatter(formatter)
            rootLogger.addHandler(fileHandler)
            Channel.logfile_logging_configured = True

        # log to console
        if not Channel.console_logging_configured:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(formatter)
            rootLogger.addHandler(consoleHandler)
            Channel.console_logging_configured = True


    def process_args(self, args):
        if args.channel is not None:
            self.execution_flags["--channel"] = args.channel
        if args.graph is not None:
            self.execution_flags["--graph"] = args.graph
        if args.loglevel is not None:
            self.execution_flags["--loglevel"] = args.loglevel
        if args.logfile is not None:
            self.execution_flags["--logfile"] = args.logfile
        if args.seed is not None:
            self.execution_flags["--seed"] = args.seed
        if args.interp_num is not None:
            self.execution_flags["--interp_num"] = args.interp_num
        if args.preview is not None:
            self.execution_flags["--preview"] = args.preview
        if args.output is not None:
            self.execution_flags["--output"] = args.output
        if args.data is not None:
            self.execution_flags["--data"] = args.data
        
        # Configure logging
        Channel.configure_logging(
            loglevel=self.execution_flags["--loglevel"],
            logfile=self.execution_flags["--logfile"],
            logfile_mode="a"
        )

        # Configure global variables
        ctx.initialize(
            channel=self,
            seed=self.execution_flags["--seed"],
            interp_num=self.execution_flags["--interp_num"],
            preview=self.execution_flags["--preview"],
            output=self.execution_flags["--output"],
            data=self.execution_flags["--data"])

    def setup(self):
        """ Execute channel setup modules """
        for setup_module in self.setup_modules:
            setup_method = getattr(importlib.import_module(setup_module), "setup")
            setup_method()