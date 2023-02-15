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
import sys
import os
import argparse
import yaml
import logging
from anatools.lib.channel import Channel
from anatools.lib.interp import interp

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('--channel', required=True)
parser.add_argument('--graph', required=True)
parser.add_argument('--loglevel')
parser.add_argument('--logfile')
parser.add_argument('--seed', type=int)
parser.add_argument('--interp_num', type=int)
parser.add_argument('--preview', action="store_true")
parser.add_argument('--output')
parser.add_argument('--data')
args = parser.parse_args()

# Configure initial logging (this may get overridden later)
Channel.configure_logging(loglevel=args.loglevel, logfile=args.logfile, logfile_mode="a")

# get channel file name
channel_file = args.channel
if os.path.splitext(channel_file)[1] == '':
    channel_file = channel_file + ".yml"

channel = Channel(channel_file)
channel.process_args(args)

# read graph
with open(args.graph, "r") as f:
    input_graph = yaml.safe_load(f)

# execute setup
channel.setup()

# interpret graph
try:
    interp(input_graph)
except Exception as e:
    message = f"An exception of type {type(e).__name__} occurred while interpreting graph"
    logging.error(message, exc_info=e)
    sys.exit(1)