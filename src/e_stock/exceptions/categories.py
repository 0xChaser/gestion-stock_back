from e_stock.exceptions.base import NotFound
from uuid import UUID

class CategoryNotFound(NotFound):
    def __init__(self, id: UUID):
        self.message = f"Category {id} not found"
        super().__init__(self.message)