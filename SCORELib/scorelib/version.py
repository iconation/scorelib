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
from .auth import *
from .exception import *


class ABCIconScoreVersion(ABC):
    @abstractmethod
    def get_version_number(self) -> str:
        pass


class IconScoreVersion(ABCIconScoreVersion):

    _NAME = 'SCORE_VERSION'

    # ================================================
    #  Fields
    # ================================================
    @property
    def __number(self) -> VarDB:
        return VarDB(f'{IconScoreVersion._NAME}_NUMBER', self.db, value_type=str)

    # ================================================
    #  Private methods
    # ================================================
    @staticmethod
    def __as_tuple(version: str) -> tuple:
        parts = []
        for part in version.split('.'):
            parts.append(int(part))
        return tuple(parts)

    # ================================================
    #  Internal methods
    # ================================================
    def version_update(self, version: str) -> None:
        self.__number.set(version)

    def is_less_than_target_version(self, target: str) -> bool:
        return IconScoreVersion.__as_tuple(self.__number.get()) < IconScoreVersion.__as_tuple(target)

    # ================================================
    #  External methods
    # ================================================
    @catch_exception
    @external(readonly=True)
    def get_version_number(self) -> str:
        return self.__number.get()
