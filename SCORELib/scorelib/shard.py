# -*- coding: utf-8 -*-

# Copyright 2021 ICONation
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

from iconservice import *
from .container_util import *

class Shard:
    def __init__(self, var_key: str, db: IconScoreDatabase):
        self.__name = var_key + ShardDB._NAME
        self.__json_db = VarDB(f'{self.__name}__db', db, str)
        self.__deserialize()
    
    @classmethod
    def __serialize_type(cls, value_type: type) -> str:
        supported_types = [int, bool, str, bytes, Address]
        if len(supported_types) > 10:
            raise NotImplementedError("Type serialization need to be 1 byte")
        return str(supported_types.index(value_type))
    
    @classmethod
    def __serialize_type_value(cls, value):
        return cls.__serialize_type(type(value)) + ContainerUtil.to_string(value, type(value))

    @classmethod
    def __deserialize_type(cls, value_type: str) -> type:
        supported_types = [int, bool, str, bytes, Address]
        return supported_types[int(value_type)]

    @classmethod
    def __deserialize_type_value(cls, value):
        value_type = cls.__deserialize_type(value[0])
        return ContainerUtil.from_string(value[1:], value_type)

    def get(self, key):
        return self.__cache[key]

    def set(self, key, value) -> None:
        self.__dirty = True
        self.__cache[key] = value

    def serialize(self) -> None:
        if not self.__dirty:
            # Nothing changed
            return
        serialized = {}
        for key, value in self.__cache.items():
            serialized[self.__serialize_type_value(key)] = self.__serialize_type_value(value)
        self.__json_db.set(json_dumps(serialized))
        self.__dirty = False
    
    def __deserialize(self) -> None:
        self.__cache = {}
        json_db = self.__json_db.get()
        entries = json_loads(json_db) if json_db else {}
        for key, value in entries.items():
            key = self.__deserialize_type_value(key)
            value = self.__deserialize_type_value(value)
            self.__cache[key] = value
        self.__dirty = False

class ShardDB:

    _NAME = '_SHARDDB'

    def __init__(self, var_key, db: IconScoreDatabase, shard_mask_bits: int = 4):
        # shard_mask_bits : 2**shard_mask_bits = number of shards
        # A shard shouldn't contain more than 100 items.
        # If you estimate around 1000 items in your database, you could divide it to 16 shards
        #  => shard_mask_bits = log(16, 2) = 4
        self.__name = str(var_key) + ShardDB._NAME
        self.__db = db
        self.__mask = (1 << shard_mask_bits) - 1
        self.__shards = [None] * (2**shard_mask_bits)

    def __get_shard(self, key) -> Shard:
        # Shard key = sha3(key) & shark_mask
        hash = sha3_256(ContainerUtil.encode_key(key))
        hashint = int.from_bytes(hash, "big")
        shard_key = hashint & self.__mask
        # Read cache
        shard = self.__shards[shard_key]
        if not shard:
            shard = Shard(f'{self.__name}_{shard_key}', self.__db)
            self.__shards[shard_key] = shard
        return shard

    def set(self, key, value) -> None:
        self.__get_shard(key).set(key, value)

    def get(self, key):
        return self.__get_shard(key).get(key)
    
    def serialize(self) -> None:
        for shard in filter(lambda shard: shard is not None, self.__shards):
            shard.serialize()

