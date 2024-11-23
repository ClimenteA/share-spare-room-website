from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from common.render_template import render_template


router = APIRouter(tags=["CDALegal"], prefix="/cda")


@router.get("/politica-cookies", response_class=HTMLResponse)
async def cda_get_cookies_template(request: Request):
    return await render_template(request, "cda/politica_cookies.html")


@router.get("/politica-de-confidentialitate", response_class=HTMLResponse)
async def cda_get_gdpr_template(request: Request):
    return await render_template(request, "cda/politica_de_confidentialitate.html")


@router.get("/termeni-si-conditii", response_class=HTMLResponse)
async def cda_get_toc_template(request: Request):
    return await render_template(request, "cda/termeni_si_conditii.html")


@router.get("/despre-noi", response_class=HTMLResponse)
async def cda_get_about_us_template(request: Request):
    return await render_template(request, "cda/about_us.html")
