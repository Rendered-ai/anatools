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
import os
import time
from numpy.random import RandomState

initialized = False
channel = None
seed = None
interp_num = None
preview = None
output = None
data = None
random = None
packages = None
channel = None

def initialize(channel, seed=None, interp_num=0, preview=False, output="./output", data="./data"):
    """ Initialize Ana configuration """

    globals()['channel'] = channel

    if seed is None:
        globals()['seed'] = int(str(int(time.time()*1e7))[-9:])
    else:
        globals()['seed'] = seed

    globals()['interp_num'] = interp_num
    globals()['preview'] = preview

    # create output directory if it doesn't already exist
    if output is not None:
        if not os.path.exists(output):
            os.makedirs(output)
    globals()['output'] = output

    # set the data directory
    globals()['data'] = data

    # use this for repeatable random distributions, e.g. self.ctx.ana_random.uniform(0,1)
    globals()['random'] = RandomState(globals()['seed'] + interp_num)

    # make package configurations available to all nodes
    globals()['packages'] = channel.packages

    globals()['initialized'] = True
    