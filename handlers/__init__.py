# handlers/__init__.py
from aiogram.dispatcher.router import Router
from .start import router as start_router
from .categories import router as categories_router
from .admin import router as admin_router
from .products import router as products_router
from .shops import router as shops_router
from .orders import router as orders_router
from .orders_list import router as list_orders_router
from .shopping import router as shopping_router

def setup_handlers(main_router: Router):
    # Регистрация всех маршрутизаторов
    main_router.include_router(start_router)
    main_router.include_router(categories_router)
    main_router.include_router(admin_router)
    main_router.include_router(products_router)
    main_router.include_router(shops_router)
    main_router.include_router(orders_router)
    main_router.include_router(list_orders_router)
    main_router.include_router(shopping_router)