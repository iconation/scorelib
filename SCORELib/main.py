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
from .scorelib.exception import *
from .scorelib.bag import *
from .scorelib.set import *
from .scorelib.linked_list import *
from .scorelib.id_factory import *
from .scorelib.iterable_dict import *
from .scorelib.binary_tree import *


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
    @catch_exception
    def bagdb(self) -> BagDB:
        return BagDB('BAG', self.db, int)

    @catch_exception
    def setdb(self) -> SetDB:
        return SetDB('SET', self.db, int)

    @catch_exception
    def linkedlistdb(self) -> LinkedListDB:
        return LinkedListDB('LLDB', self.db, int)

    @catch_exception
    def linkedlistdb_address(self) -> LinkedListDB:
        return LinkedListDB('LLDB', self.db, Address)

    @catch_exception
    def linkedlistdb_str(self) -> LinkedListDB:
        return LinkedListDB('LLDB', self.db, str)

    @catch_exception
    def linkedlistdb_bytes(self) -> LinkedListDB:
        return LinkedListDB('LLDB', self.db, bytes)

    @catch_exception
    def idfactory(self) -> IdFactory:
        return IdFactory('IDFACTORY', self.db)

    @catch_exception
    def iterabledict(self) -> IterableDictDB:
        return IterableDictDB('ITERABLEDICT', self.db, str, str)

    @catch_exception
    def binarytree(self) -> BinaryTreeDB:
        return BinaryTreeDB('BINARY_TREE', self.db, str)

    # ================================================
    #  BAGDB External methods
    # ================================================
    @catch_exception
    @external(readonly=True)
    def bagdb_length(self) -> int:
        return len(self.bagdb())

    @catch_exception
    @external(readonly=True)
    def bagdb_count(self, item: int) -> int:
        return self.bagdb().count(item)

    @catch_exception
    @external
    def bagdb_add(self, item: int) -> None:
        self.bagdb().add(item)

    @catch_exception
    @external
    def bagdb_clear(self) -> None:
        self.bagdb().clear()

    @catch_exception
    @external
    def bagdb_remove(self, item: int) -> None:
        self.bagdb().remove(item)

    @staticmethod
    def bagdb_sentinel(db: IconScoreDatabase, item, **kwargs) -> bool:
        return item == kwargs['match']

    @catch_exception
    @external(readonly=True)
    def bagdb_select(self, offset: int, match: int) -> list:
        return self.bagdb().select(offset, self.bagdb_sentinel, match=match)

    # ================================================
    #  SetDB External methods
    # ================================================
    @catch_exception
    @external(readonly=True)
    def setdb_length(self) -> int:
        return len(self.setdb())

    @catch_exception
    @external
    def setdb_add(self, item: int) -> None:
        self.setdb().add(item)

    @catch_exception
    @external
    def setdb_remove(self, item: int) -> None:
        self.setdb().remove(item)

    @catch_exception
    @external
    def setdb_discard(self, item: int) -> None:
        self.setdb().discard(item)

    @catch_exception
    @external
    def setdb_pop(self) -> None:
        self.setdb().pop()

    @staticmethod
    def setdb_sentinel(db: IconScoreDatabase, item, **kwargs) -> bool:
        return item == kwargs['match']

    @catch_exception
    @external(readonly=True)
    def setdb_select(self, offset: int, match: int) -> list:
        return self.setdb().select(offset, self.setdb_sentinel, match=match)

    # ================================================
    #  LinkedListDB External methods
    # ================================================
    # ---------- INT ----------------
    @catch_exception
    @external
    def linkedlistdb_append(self, item: int) -> None:
        list = self.linkedlistdb()
        list.append(item)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_prepend(self, item: int) -> None:
        list = self.linkedlistdb()
        list.append(item)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_append_after(self, item: int, after_id: int) -> None:
        list = self.linkedlistdb()
        list.append_after(item, after_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_prepend_before(self, item: int, before_id: int) -> None:
        list = self.linkedlistdb()
        list.prepend_before(item, before_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_move_node_after(self, cur_id: int, after_id: int) -> None:
        list = self.linkedlistdb()
        list.move_node_after(cur_id, after_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_move_node_before(self, cur_id: int, before_id: int) -> None:
        list = self.linkedlistdb()
        list.move_node_before(cur_id, before_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_remove_head(self) -> None:
        list = self.linkedlistdb()
        list.remove_head()
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_remove_tail(self) -> None:
        list = self.linkedlistdb()
        list.remove_tail()
        list.serialize()

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_length(self) -> int:
        return len(self.linkedlistdb())

    @catch_exception
    @external
    def linkedlistdb_remove(self, node_id: int) -> None:
        list = self.linkedlistdb()
        list.remove(node_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_clear(self) -> None:
        list = self.linkedlistdb()
        list.clear()
        list.serialize()

    @staticmethod
    def linkedlistdb_sentinel(db: IconScoreDatabase, item, **kwargs) -> bool:
        node_id, value = item
        return value == kwargs['match']

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_select(self, offset: int, match: int) -> list:
        return self.linkedlistdb().select(offset, self.linkedlistdb_sentinel, match=match)

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_next(self, next_id: int) -> int:
        return self.linkedlistdb().next(next_id)

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_prev(self, prev_id: int) -> int:
        return self.linkedlistdb().prev(prev_id)

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_selectall(self, offset: int) -> list:
        return self.linkedlistdb().select(offset)

    # ---------- Address ----------------
    @catch_exception
    @external
    def linkedlistdb_address_append(self, item: Address) -> None:
        list = self.linkedlistdb_address()
        list.append(item)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_address_move_head_to_tail(self) -> None:
        list = self.linkedlistdb_address()
        list.move_head_to_tail()
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_address_move_tail_to_head(self) -> None:
        list = self.linkedlistdb_address()
        list.move_tail_to_head()
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_address_prepend(self, item: Address) -> None:
        list = self.linkedlistdb_address()
        list.append(item)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_address_append_after(self, item: Address, after_id: int) -> None:
        list = self.linkedlistdb_address()
        list.append_after(item, after_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_address_prepend_before(self, item: Address, before_id: int) -> None:
        list = self.linkedlistdb_address()
        list.prepend_before(item, before_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_address_move_node_after(self, cur_id: int, after_id: int) -> None:
        list = self.linkedlistdb_address()
        list.move_node_after(cur_id, after_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_address_move_node_before(self, cur_id: int, before_id: int) -> None:
        list = self.linkedlistdb_address()
        list.move_node_before(cur_id, before_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_address_remove_head(self) -> None:
        list = self.linkedlistdb_address()
        list.remove_head()
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_address_remove_tail(self) -> None:
        list = self.linkedlistdb_address()
        list.remove_tail()
        list.serialize()

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_address_length(self) -> int:
        return len(self.linkedlistdb_address())

    @catch_exception
    @external
    def linkedlistdb_address_remove(self, node_id: int) -> None:
        list = self.linkedlistdb_address()
        list.remove(node_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_address_clear(self) -> None:
        list = self.linkedlistdb_address()
        list.clear()
        list.serialize()

    @staticmethod
    def linkedlistdb_address_sentinel(db: IconScoreDatabase, item, **kwargs) -> bool:
        node_id, value = item
        return value == kwargs['match']

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_address_select(self, offset: int, match: Address) -> list:
        return self.linkedlistdb_address().select(offset, self.linkedlistdb_address_sentinel, match=match)

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_address_next(self, next_id: int) -> int:
        return self.linkedlistdb_address().next(next_id)

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_address_prev(self, prev_id: int) -> int:
        return self.linkedlistdb_address().prev(prev_id)

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_address_selectall(self, offset: int) -> list:
        return self.linkedlistdb_address().select(offset)

    # ---------- str ----------------
    @catch_exception
    @external
    def linkedlistdb_str_append(self, item: str) -> None:
        list = self.linkedlistdb_str()
        list.append(item)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_str_prepend(self, item: str) -> None:
        list = self.linkedlistdb_str()
        list.append(item)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_str_append_after(self, item: str, after_id: int) -> None:
        list = self.linkedlistdb_str()
        list.append_after(item, after_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_str_prepend_before(self, item: str, before_id: int) -> None:
        list = self.linkedlistdb_str()
        list.prepend_before(item, before_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_str_move_node_after(self, cur_id: int, after_id: int) -> None:
        list = self.linkedlistdb_str()
        list.move_node_after(cur_id, after_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_str_move_node_before(self, cur_id: int, before_id: int) -> None:
        list = self.linkedlistdb_str()
        list.move_node_before(cur_id, before_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_str_remove_head(self) -> None:
        list = self.linkedlistdb_str()
        list.remove_head()
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_str_remove_tail(self) -> None:
        list = self.linkedlistdb_str()
        list.remove_tail()
        list.serialize()

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_str_length(self) -> int:
        return len(self.linkedlistdb_str())

    @catch_exception
    @external
    def linkedlistdb_str_remove(self, node_id: int) -> None:
        list = self.linkedlistdb_str()
        list.remove(node_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_str_clear(self) -> None:
        list = self.linkedlistdb_str()
        list.clear()
        list.serialize()

    @staticmethod
    def linkedlistdb_str_sentinel(db: IconScoreDatabase, item, **kwargs) -> bool:
        node_id, value = item
        return value == kwargs['match']

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_str_select(self, offset: int, match: str) -> list:
        return self.linkedlistdb_str().select(offset, self.linkedlistdb_str_sentinel, match=match)

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_str_next(self, next_id: int) -> int:
        return self.linkedlistdb_str().next(next_id)

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_str_prev(self, prev_id: int) -> int:
        return self.linkedlistdb_str().prev(prev_id)

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_str_selectall(self, offset: int) -> list:
        return self.linkedlistdb_str().select(offset)

    # ---------- bytes ----------------
    @catch_exception
    @external
    def linkedlistdb_bytes_append(self, item: bytes) -> None:
        list = self.linkedlistdb_bytes()
        list.append(item)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_bytes_prepend(self, item: bytes) -> None:
        list = self.linkedlistdb_bytes()
        list.append(item)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_bytes_append_after(self, item: bytes, after_id: int) -> None:
        list = self.linkedlistdb_bytes()
        list.append_after(item, after_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_bytes_prepend_before(self, item: bytes, before_id: int) -> None:
        list = self.linkedlistdb_bytes()
        list.prepend_before(item, before_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_bytes_move_node_after(self, cur_id: int, after_id: int) -> None:
        list = self.linkedlistdb_bytes()
        list.move_node_after(cur_id, after_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_bytes_move_node_before(self, cur_id: int, before_id: int) -> None:
        list = self.linkedlistdb_bytes()
        list.move_node_before(cur_id, before_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_bytes_remove_head(self) -> None:
        list = self.linkedlistdb_bytes()
        list.remove_head()
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_bytes_remove_tail(self) -> None:
        list = self.linkedlistdb_bytes()
        list.remove_tail()
        list.serialize()

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_bytes_length(self) -> int:
        return len(self.linkedlistdb_bytes())

    @catch_exception
    @external
    def linkedlistdb_bytes_remove(self, node_id: int) -> None:
        list = self.linkedlistdb_bytes()
        list.remove(node_id)
        list.serialize()

    @catch_exception
    @external
    def linkedlistdb_bytes_clear(self) -> None:
        list = self.linkedlistdb_bytes()
        list.clear()
        list.serialize()

    @staticmethod
    def linkedlistdb_bytes_sentinel(db: IconScoreDatabase, item, **kwargs) -> bool:
        node_id, value = item
        return value == kwargs['match']

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_bytes_select(self, offset: int, match: bytes) -> list:
        return self.linkedlistdb_bytes().select(offset, self.linkedlistdb_bytes_sentinel, match=match)

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_bytes_next(self, next_id: int) -> int:
        return self.linkedlistdb_bytes().next(next_id)

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_bytes_prev(self, prev_id: int) -> int:
        return self.linkedlistdb_bytes().prev(prev_id)

    @catch_exception
    @external(readonly=True)
    def linkedlistdb_bytes_selectall(self, offset: int) -> list:
        return self.linkedlistdb_bytes().select(offset)

    # ================================================
    #  IdFactory External methods
    # ================================================
    @catch_exception
    @external
    def idfactory_gen_uid(self) -> int:
        return self.idfactory().get_uid()

    @catch_exception
    @external(readonly=True)
    def idfactory_get_uid(self) -> int:
        return self.idfactory()._uid.get()

    # ================================================
    #  IterableDict External methods
    # ================================================
    @catch_exception
    @external(readonly=True)
    def iterabledict_keys(self) -> list:
        return self.iterabledict().keys()

    @catch_exception
    @external(readonly=True)
    def iterabledict_values(self) -> list:
        return self.iterabledict().values()

    @catch_exception
    @external(readonly=True)
    def iterabledict_iter(self) -> list:
        for key, value in self.iterabledict():
            yield key, value

    @catch_exception
    @external(readonly=True)
    def iterabledict_contains(self, item: str) -> bool:
        return item in self.iterabledict()

    @catch_exception
    @external(readonly=True)
    def iterabledict_length(self) -> int:
        return len(self.iterabledict())

    @catch_exception
    @external
    def iterabledict_setitem(self, key: str, value: str) -> None:
        self.iterabledict()[key] = value

    @catch_exception
    @external(readonly=True)
    def iterabledict_getitem(self, key: str) -> str:
        return self.iterabledict()[key]

    @catch_exception
    @external
    def iterabledict_delitem(self, key: str) -> None:
        del self.iterabledict()[key]

    @staticmethod
    def iterabledict_sentinel(db: IconScoreDatabase, item, **kwargs) -> bool:
        key, value = item
        return key == kwargs['match']

    @catch_exception
    @external(readonly=True)
    def iterabledict_select(self, offset: int, match: str) -> list:
        return self.iterabledict().select(offset, self.iterabledict_sentinel, match=match)

    @catch_exception
    @external
    def iterabledict_clear(self) -> None:
        self.iterabledict().clear()

    # ================================================
    #  BinaryTreeDB External methods
    # ================================================
    @catch_exception
    @external
    def binarytree_create_node(self, value: str) -> None:
        self.binarytree().create_node(value)

    @catch_exception
    @external
    def binarytree_set_left_child(self, parent_id: int, left_id: int) -> None:
        self.binarytree().set_left_child(parent_id, left_id)

    @catch_exception
    @external
    def binarytree_set_right_child(self, parent_id: int, right_id: int) -> None:
        self.binarytree().set_right_child(parent_id, right_id)

    @staticmethod
    def binarytree_callback(db: IconScoreDatabase, item, **kwargs) -> None:
        kwargs['result'].append(item)

    @catch_exception
    @external(readonly=True)
    def binarytree_traverse_post_order(self, root: int) -> list:
        result = []
        self.binarytree().traverse_post_order(root, self.binarytree_callback, result=result)
        return result

    @catch_exception
    @external(readonly=True)
    def binarytree_traverse_in_order(self, root: int) -> list:
        result = []
        self.binarytree().traverse_in_order(root, self.binarytree_callback, result=result)
        return result

    @catch_exception
    @external(readonly=True)
    def binarytree_traverse_pre_order(self, root: int) -> list:
        result = []
        self.binarytree().traverse_pre_order(root, self.binarytree_callback, result=result)
        return result
