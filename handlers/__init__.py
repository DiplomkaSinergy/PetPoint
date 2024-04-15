# handlers/__init__.py
from aiogram.dispatcher.router import Router
from .start import router as start_router
from .categories import router as categories_router
from .admin import router as admin_router

def setup_handlers(main_router: Router):
    # Регистрация всех маршрутизаторов
    main_router.include_router(start_router)
    main_router.include_router(categories_router)
    main_router.include_router(admin_router)
