from typing import Optional, List

from fastapi import Depends, Body
from pydantic import BaseModel, Field
from structlog.stdlib import BoundLogger
from ztk_api import ZTK, NineNineArgs, NineNineModel

from core.logger import get_logger
from core.resp.base import ResponseModel, ApiResp
from core.vendor.ztk import get_ztk_api_v2
from ...api import fields
from ...api.app import app
from ...api_utils import api_inner_wrapper


class NineNineResponseModel(ResponseModel):
    data: Optional[List[NineNineModel]] = Field(None, title="具体数据")


class NineNineForm(BaseModel):
    """
    9.9 包邮购请求参数
    """

    page: int = fields.page_field
    page_size: int = fields.page_size_field
    sort: str = fields.sort_fields
    cid: Optional[int] = fields.cid_field
    price: str = Field("0.0-9.9", title="商品价格", description="")

    def to_data(self) -> NineNineArgs:
        return NineNineArgs.from_dict(self.dict())


@app.post(
    "/ztk/nine_nine",
    tags=["折淘客"],
    summary="9.9 包邮购",
    description="",
    response_model=NineNineResponseModel,
)
async def nine_nine(
    g: NineNineForm = Body(..., title="请求参数"),
    logger: BoundLogger = Depends(get_logger),
    ztk: ZTK = Depends(get_ztk_api_v2),
):
    @api_inner_wrapper(logger)
    async def inner():
        data = g.to_data()
        j = await ztk.nine_nine(data)
        return ApiResp.from_data(j.content).to_dict()

    return await inner
