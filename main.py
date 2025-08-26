from typing import Annotated, Literal

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Field

app = FastAPI()


@app.get("/items1/")
async def read_items1(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None,
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}

@app.get("/items2/{item_id}")
async def read_items2(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

@app.get("/items3/{item_id}")
async def read_items3(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)], q: str
):

    """
    ge = Greater than or Equal
    le = Less than or Equal
    gt = Greater Than
    lt Less Than
    """

    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

@app.get("/items31/{item_id}")
async def read_items31(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)],
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results


# Next day


class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/items4/")
async def read_items4(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
