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

class ContainerUtil(object):
    @classmethod
    def encode_key(cls, key) -> bytes:
        if key is None:
            raise NotImplementedError('key is None')

        if isinstance(key, int):
            bytes_key = cls.int_to_bytes(key)
        elif isinstance(key, str):
            bytes_key = key.encode('utf-8')
        elif isinstance(key, Address):
            bytes_key = key.to_bytes()
        elif isinstance(key, bytes):
            bytes_key = key
        else:
            raise NotImplementedError(f'Unsupported key type: {type(key)}')
        return bytes_key

    @classmethod
    def to_string(cls, value, value_type: type) -> str:
        if value_type == bool: return str(int(value))
        if value_type == int: return str(value)
        if value_type == str: return value
        elif value_type == Address: return str(value)
        elif value_type == bytes: return value.hex()
        else: raise NotImplementedError(f"Invalid type {value_type}")

    @classmethod
    def from_string(cls, value: str, value_type: type):
        if value_type == bool: return bool(int(value))
        if value_type == int: return int(value)
        if value_type == str: return value
        elif value_type == Address: return Address.from_string(value)
        elif value_type == bytes: return bytes.fromhex(value)
        else: raise NotImplementedError(f"Invalid type {value_type}")

    @classmethod
    def encode_value(cls, value) -> bytes:
        if isinstance(value, int):
            byte_value = cls.int_to_bytes(value)
        elif isinstance(value, str):
            byte_value = value.encode('utf-8')
        elif isinstance(value, Address):
            byte_value = value.to_bytes()
        elif isinstance(value, bool):
            byte_value = cls.int_to_bytes(int(value))
        elif isinstance(value, bytes):
            byte_value = value
        else:
            raise NotImplementedError(f'Unsupported value type: {type(value)}')
        return byte_value

    @classmethod
    def decode_object(cls, value: bytes, value_type: type):
        if value is None:
            return cls.get_default_value(value_type)

        obj_value = None
        if value_type == int:
            obj_value = cls.bytes_to_int(value)
        elif value_type == str:
            obj_value = value.decode()
        elif value_type == Address:
            obj_value = Address.from_bytes(value)
        if value_type == bool:
            obj_value = bool(cls.bytes_to_int(value))
        elif value_type == bytes:
            obj_value = value
        return obj_value

    @classmethod
    def bytes_to_int(cls, v: bytes) -> int:
        return int.from_bytes(v, byteorder='big', signed=True)

    @classmethod
    def byte_length_of_int(cls, n: int):
        if n < 0:
            # adds 1 because `bit_length()` always returns a bit length of absolute-value of `n`
            n += 1
        return (n.bit_length() + 8) // 8

    @classmethod
    def int_to_bytes(cls, n: int) -> bytes:
        length = cls.byte_length_of_int(n)
        return n.to_bytes(length, byteorder='big', signed=True)

    @classmethod
    def get_default_value(cls, value_type: type):
        if value_type == int: return 0
        elif value_type == str: return ""
        elif value_type == bool: return False
        elif value_type == Address: return None
        elif value_type == bytes: return None
        raise NotImplementedError(f'Unsupported value type: {value_type}')