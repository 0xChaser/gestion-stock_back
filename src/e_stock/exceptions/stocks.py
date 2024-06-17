from uuid import UUID

from e_stock.exceptions.base import NotFound


class StockNotFound(NotFound):
    def __init__(self, id: UUID):
        self.message = f"Stock {id} not found"
        super().__init__(self.message)
