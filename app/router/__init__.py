import os
import traceback
from fastapi import APIRouter
from fastapi.logger import logger


router = APIRouter()

for router_file in os.listdir("app/router/endpoint"):
    try:
        if router_file.endswith(".py"):
            module_name = "app.router.endpoint." + router_file[:-3]
            module = __import__(module_name, fromlist=[""])
            router_object = getattr(module, "router")
            prefix = getattr(module, "prefix", router_file[:-3])

            router.include_router(router_object, prefix="/api", tags=[router_file[:-3]])
            print(f"Loaded router: /api/{prefix} - {router_file}")

    except Exception as e:
        logger.error(f"Error loading router {router_file}:\n{traceback.format_exc()}")
