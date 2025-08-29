class FakeDeleteResult:
    def __init__(self, deleted_count: int):
        self.deleted_count = deleted_count
        
class FakeCollection:
    def __init__(self):
        self.storage = {}

    async def insert_one(self, doc):
        self.storage[doc["id"]] = doc
        return doc

    async def find_one(self, query):
        return self.storage.get(query["id"])
    
    def find(self):
        async def generator():
            for item in self.storage.values():
                yield item
        return generator()
    
    async def find_one_and_update(self, filter, update, return_document=None):
        item = self.storage.get(filter["id"])
        if not item:
            return None
        if "$set" in update:
            item.update(update["$set"])
        elif "set" in update:
            item.update(update["set"])
        self.storage[filter["id"]] = item
        return item
    
    async def delete_one(self, filter):
        if filter["id"] in self.storage:
            del self.storage[filter["id"]]
            return FakeDeleteResult(deleted_count=1)
        return FakeDeleteResult(deleted_count=0)