from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from odoo import api, fields, models
from odoo.api import Environment

from odoo.addons.fastapi.dependencies import odoo_env, authenticated_partner_env


class FastapiEndpoint(models.Model):

    _inherit = "fastapi.endpoint"

    app: str = fields.Selection(
        selection_add=[("demo", "Demo Endpoint")], ondelete={"demo": "cascade"}
    )

    def _get_fastapi_routers(self):
        if self.app == "demo":
            return [demo_api_router]
        return super()._get_fastapi_routers()


# create a router
demo_api_router = APIRouter()


class PartnerInfo(BaseModel):
    name: str
    email: str


@demo_api_router.get("/partners", response_model=list[PartnerInfo])
# def get_partners(env: Annotated[Environment, Depends(authenticated_partner_env)]) -> list[PartnerInfo]:
def get_partners(env: Annotated[Environment, Depends(odoo_env)]) -> list[PartnerInfo]:
    return [
        PartnerInfo(name=partner.name, email=partner.email or '*@*')
        for partner in env["res.partner"].search([])
    ]
