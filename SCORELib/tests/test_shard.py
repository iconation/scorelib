# -*- coding: utf-8 -*-

# Copyright 2018 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
import time

from .utils import *
from .scorelib_utils import *
from iconservice import *

DIR_PATH = os.path.abspath(os.path.dirname(__file__))

from SCORELib.scorelib.shard import ShardDB

def profiler(func):
    @wraps(func)
    def __wrapper(self: object, *args, **kwargs):
        start_time = time.time()
        func(self, *args, **kwargs)
        end_time = time.time()
        time_elapsed = (end_time - start_time)
        print("%s => %.03fs elapsed" % (str(func), time_elapsed))
    return __wrapper

class TestShard(ScoreLibTests):
    def setUp(self):
        super().setUp()

    @profiler
    def test_shard_set(self):
        self.shard_set("key", 123)

    @profiler
    def test_shard_multiset(self):
        self.shard_multiset(1000)

    @profiler
    def test_shard_get(self):
        key = "key"
        value = 123
        self.shard_set(key, value)
        result = self.shard_get(key)