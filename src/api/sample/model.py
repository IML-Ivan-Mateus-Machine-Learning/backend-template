"""Define sample models."""

from typing import Annotated

from fastapi import Body
from fastapi import Query
from pydantic import BaseModel


class SampleResponse(BaseModel):
    query_name: str
    query_age: int
    body_name: str
    body_age: int
    sample_path_params: str


class SampleQueryParams(BaseModel):
    query_name: Annotated[
        str,
        Query(
            ...,
            title="Query Name",
            description="Query Name of the sample",
        ),
    ]
    query_age: Annotated[
        int,
        Query(
            default=21,
            title="Query Age",
            description="Query Age of the sample",
            gt=18,
        ),
    ]


class SampleBodyParams(BaseModel):
    body_name: Annotated[
        str,
        Body(
            ...,
            title="Body Name",
            description="Body Name of the sample",
        ),
    ]
    body_age: Annotated[
        int,
        Body(
            default=21,
            title="Body Age",
            description="Body Age of the sample",
            gt=18,
        ),
    ]


__all__ = [SampleQueryParams, SampleBodyParams]
