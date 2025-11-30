import app.routes
from app.routes import health_router, upload_router, analysis_router

print("=== ROUTERS LOADED SUCCESSFULLY ===")
print("health_router =", health_router)
print("upload_router =", upload_router)
print("analysis_router =", analysis_router)

print("\n=== ROUTES MODULE FILE ===")
print(app.routes.__file__)
