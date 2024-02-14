from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path

from .model import SampleBodyParams
from .model import SampleQueryParams
from .model import SampleResponse

router = APIRouter(
    prefix="/sample",
    tags=["sample"],
)


@router.post(
    "/{sample_path_params}",
    summary="Sample endpoint",
    response_description="Sample response",
    response_model=SampleResponse,
)
def trigger_simulation(
    sample_query_params: Annotated[SampleQueryParams, Depends()],
    sample_body_params: SampleBodyParams,
    sample_path_params: Annotated[str, Path(title="Sample Path Params")],
):
    print(
        f"POST /sample start with query {sample_query_params}, body {sample_body_params} and path "
        f"{sample_path_params}"
    )

    response_dict = {
        **sample_query_params.dict(),
        **sample_body_params.dict(),
        **{"sample_path_params": sample_path_params},
    }
    print(response_dict)
    response: SampleResponse = SampleResponse(**response_dict)

    print(
        f"POST /sample finished with data {sample_query_params}, body {sample_body_params} and "
        f"path {sample_path_params} and response {response}"
    )

    return response
