import shutil
from collections import deque
from collections import OrderedDict

from cachecontrol.caches import FileCache


class LRUCache(object):

    def __init__(self, capacity: int, filecache: FileCache):
        self.capacity = capacity
        self.container = deque()
        self.map = OrderedDict()
        self.item = str()

        self.filecache = filecache

    def filecache_current_size(self) -> int:
        return len(self.map)

    def filecache_is_full(self) -> bool:
        return len(self.map) >= self.capacity
    
    def filecache_is_empty(self) -> bool:
        return len(self.map) == 0
    
    def filecache_pop(self) -> str:
        self.item = self.map.popitem(last=False)[0]
        self.filecache.delete(self.item)
        return "Removed:" + self.item
        
    def filecache_store_request(self, url: str, size: int) -> bool:
        self.map[url] = size
        self.map.move_to_end(url)

        if len(self.map) > self.capacity:
            self.item = self.map.popitem(last=False)[0]
            self.filecache.delete(self.item)
            print("Removing:", self.item)

            return True
        else:
            return False
            
    def filecache_setcapacity(self, capacity: int) -> None:
        self.capacity = capacity

    def get_last_item(self) -> str:
        return self.item

    def close(self) -> None:
        print("Closing cache")
        shutil.rmtree('.webcache')
