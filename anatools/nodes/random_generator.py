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
import logging
import ast
import sys
import anatools.lib.context as ctx
from anatools.lib.node import Node

logger = logging.getLogger(__name__)


def _float_or_list(val):
    """Input conversion - expecting a float or a list of floats"""
    if isinstance(val, str):
        try:
            val = ast.literal_eval(val)
        except:
            logger.error("Expected float or list of floats")
            sys.exit(1)
    if isinstance(val, list) or isinstance(val, float):
        return val
    elif isinstance(val, int):
        return float(val)
    else:
        logger.error("Expected float or list of floats")
        sys.exit(1)

def _int_or_list(val):
    """Input conversion - expecting an int or a list of ints"""
    if isinstance(val, str):
        try:
            val = ast.literal_eval(val)
        except:
            logger.error("Expected integer or list of integers")
            sys.exit(1)
    if isinstance(val, list) or isinstance(val, int):
        return val
    else:
        logger.error("Expected integer or list of integers")
        sys.exit(1)

def _none_or_int_or_list(val):
    """Input conversion - expecting None, empty string, int, or a list of ints"""
    if val is None or val == "":
        # assume empty string means null - necessary for GUI when user backspaces over field
        return None
    elif isinstance(val, str):
        try:
            val = ast.literal_eval(val)
        except:
            logger.error("Expected empty string, integer, or list of integers")
            sys.exit(1)
    if isinstance(val, list):
        return tuple(val)
    elif isinstance(val, int):
        return val
    else:
        logger.error("Expected empty string, integer, or list of integers")
        sys.exit(1)

class RandomTriangular(Node):
    """
    Draw random samples from a triangular distribution over the closed interval [left, right].
    See numpy.random.triangular for details.
    """

    def exec(self):
        """Execute node"""
        logger.info("Executing {}".format(self.name))

        # get inputs
        left = _float_or_list(self.inputs["left"][0])
        mode = _float_or_list(self.inputs["mode"][0])
        right = _float_or_list(self.inputs["right"][0])
        size = _none_or_int_or_list(self.inputs["size"][0])

        # draw samples
        out = ctx.random.triangular(left, mode, right, size)

        return {"out": out}

class RandomUniform(Node):
    """
    Draw random samples from a uniform distribution over the half-open interval [low, high).
    See numpy.random.uniform for details.
    """

    def exec(self):
        """Execute node"""
        logger.info("Executing {}".format(self.name))

        # get inputs
        low = _float_or_list(self.inputs["low"][0])
        high = _float_or_list(self.inputs["high"][0])
        size = _none_or_int_or_list(self.inputs["size"][0])

        # draw samples
        out = ctx.random.uniform(low, high, size)

        return {"out": out}

class RandomRandint(Node):
    """
    Return random integers from low (inclusive) to high (exclusive).
    See numpy.random.randint for details.
    """

    def exec(self):
        """Execute node"""
        logger.info("Executing {}".format(self.name))

        # get inputs
        low = _int_or_list(self.inputs["low"][0])
        high = _int_or_list(self.inputs["high"][0])
        size = _none_or_int_or_list(self.inputs["size"][0])

        # draw samples
        out = ctx.random.randint(low, high, size)

        return {"out": out}

class RandomNormal(Node):
    """
    Draw random samples from a normal (Gaussian) distribution.
    See numpy.random.normal for details.
    """

    def exec(self):
        """Execute node"""
        logger.info("Executing {}".format(self.name))

        # get inputs
        loc = _float_or_list(self.inputs["loc"][0])
        scale = _float_or_list(self.inputs["scale"][0])
        size = _none_or_int_or_list(self.inputs["size"][0])

        # draw samples
        out = ctx.random.normal(loc, scale, size)

        return {"out": out}


class RandomChoice(Node):

    def exec(self):
        logger.info("Executing {}".format(self.name))
        # parse inputs
        choice_list = list(self.inputs["List_of_Choices"][0])
        number = int(self.inputs["Number_of_Choices"][0])
        unique = str(self.inputs["Unique_Choices"][0])
        if unique is "True":    choices = ctx.random.choice(choice_list, number, replace=False) 
        else:                   choices = ctx.random.choice(choice_list, number, replace=True) 
        return {"Choices": choices}
