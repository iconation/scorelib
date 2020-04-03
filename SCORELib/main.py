# -*- coding: utf-8 -*-

# Copyright 2020 ICONation
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
from .checks import *
from .scorelib.bag import *
from .scorelib.set import *
from .scorelib.linked_list import *


class SCORELib(IconScoreBase):

    # ================================================
    #  Initialization
    # ================================================
    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)

    def on_install(self) -> None:
        super().on_install()

    def on_update(self) -> None:
        super().on_update()

    # ================================================
    #  Internal methods
    # ================================================
    @catch_error
    def bagdb(self) -> BagDB:
        return BagDB('BAG', self.db, int)

    @catch_error
    def setdb(self) -> SetDB:
        return SetDB('SET', self.db, int)

    @catch_error
    def linkedlistdb(self) -> LinkedListDB:
        return LinkedListDB('LLDB', self.db, int)

    # ================================================
    #  BAGDB External methods
    # ================================================
    @catch_error
    @external(readonly=True)
    def bagdb_length(self) -> int:
        return len(self.bagdb())

    @catch_error
    @external(readonly=True)
    def bagdb_count(self, item: int) -> int:
        return self.bagdb().count(item)

    @catch_error
    @external
    def bagdb_add(self, item: int) -> None:
        self.bagdb().add(item)

    @catch_error
    @external
    def bagdb_clear(self) -> None:
        self.bagdb().clear()

    @catch_error
    @external
    def bagdb_remove(self, item: int) -> None:
        self.bagdb().remove(item)

    @staticmethod
    def bagdb_sentinel(db, item, **kwargs) -> bool:
        return item == kwargs['match']

    @catch_error
    @external(readonly=True)
    def bagdb_select(self, offset: int, match: int) -> list:
        return self.bagdb().select(offset, self.bagdb_sentinel, match=match)

    # ================================================
    #  SetDB External methods
    # ================================================
    @catch_error
    @external(readonly=True)
    def setdb_length(self) -> int:
        return len(self.setdb())

    @catch_error
    @external
    def setdb_add(self, item: int) -> None:
        self.setdb().add(item)

    @catch_error
    @external
    def setdb_remove(self, item: int) -> None:
        self.setdb().remove(item)

    @catch_error
    @external
    def setdb_discard(self, item: int) -> None:
        self.setdb().discard(item)

    @catch_error
    @external
    def setdb_pop(self) -> None:
        self.setdb().pop()

    @staticmethod
    def setdb_sentinel(db, item, **kwargs) -> bool:
        return item == kwargs['match']

    @catch_error
    @external(readonly=True)
    def setdb_select(self, offset: int, match: int) -> list:
        return self.setdb().select(offset, self.setdb_sentinel, match=match)

    # ================================================
    #  LinkedListDB External methods
    # ================================================
    @catch_error
    @external
    def linkedlistdb_append(self, item: int) -> None:
        self.linkedlistdb().append(item)

    @catch_error
    @external
    def linkedlistdb_prepend(self, item: int) -> None:
        self.linkedlistdb().append(item)

    @catch_error
    @external
    def linkedlistdb_append_after(self, item: int, after_id: int) -> None:
        self.linkedlistdb().append_after(item, after_id)

    @catch_error
    @external
    def linkedlistdb_prepend_before(self, item: int, before_id: int) -> None:
        self.linkedlistdb().prepend_before(item, before_id)

    @catch_error
    @external
    def linkedlistdb_move_node_after(self, cur_id: int, after_id: int) -> None:
        self.linkedlistdb().move_node_after(cur_id, after_id)

    @catch_error
    @external
    def linkedlistdb_move_node_before(self, cur_id: int, before_id: int) -> None:
        self.linkedlistdb().move_node_before(cur_id, before_id)

    @catch_error
    @external
    def linkedlistdb_remove_head(self) -> None:
        self.linkedlistdb().remove_head()

    @catch_error
    @external
    def linkedlistdb_remove_tail(self) -> None:
        self.linkedlistdb().remove_tail()

    @catch_error
    @external(readonly=True)
    def linkedlistdb_length(self) -> int:
        return len(self.linkedlistdb())

    @catch_error
    @external
    def linkedlistdb_remove(self, node_id: int) -> None:
        self.linkedlistdb().remove(node_id)

    @catch_error
    @external
    def linkedlistdb_clear(self) -> None:
        self.linkedlistdb().clear()

    @staticmethod
    def linkedlistdb_sentinel(db, item, **kwargs) -> bool:
        node_id, value = item
        return value == kwargs['match']

    @catch_error
    @external(readonly=True)
    def linkedlistdb_select(self, offset: int, match: int) -> list:
        return self.linkedlistdb().select(offset, self.linkedlistdb_sentinel, match=match)

    @catch_error
    @external(readonly=True)
    def linkedlistdb_next(self, next_id: int) -> int:
        return self.linkedlistdb().next(next_id)

    @catch_error
    @external(readonly=True)
    def linkedlistdb_prev(self, prev_id: int) -> int:
        return self.linkedlistdb().prev(prev_id)

    @catch_error
    @external(readonly=True)
    def linkedlistdb_selectall(self, offset: int) -> list:
        return self.linkedlistdb().select(offset)
