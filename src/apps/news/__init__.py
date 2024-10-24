from fastapi import APIRouter

from .article import r as article_router
from .ai import router as ai_router

router = APIRouter()


router.include_router(article_router)
router.include_router(ai_router)
