from typing import List, Optional
from pydantic import BaseModel, NoneStr
import datetime

class Book(BaseModel):
    id: int
    author: str
    title: NoneStr = None
    price: Optional[float] = None
    is_active: Optional[int] = None
    create_date: NoneStr = None
    create_by: NoneStr = None
    update_date: NoneStr = None
    update_by: NoneStr = None

class ListBook(BaseModel):
    __root__: List[Book]