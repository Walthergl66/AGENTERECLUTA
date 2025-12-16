from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import router
from app.config import settings
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejador del ciclo de vida de la aplicación"""
    # Startup
    print(f" {settings.app_name} v{settings.app_version} iniciado")
    print(f" Documentación disponible en: http://{settings.host}:{settings.port}/docs")
    print(f" Modo debug: {settings.debug}")
    yield
    # Shutdown
    print(" Cerrando la aplicación...")

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    **Sistema de Reclutamiento con IA**
    
    Sistema experto de matching entre vacantes y candidatos con:
    - Análisis semántico de habilidades (no keyword matching exacto)
    - Compliance checking automático
    - Scoring ponderado: 50% Hard Skills, 30% Experiencia, 20% Soft Skills
    - Anonimización de datos PII para cumplir normativas
    - Reportes estructurados en JSON
    
    Desarrollado con AGNO + Groq
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(router, prefix="/api/v1", tags=["ATS - Recruitment System"])


if __name__ == "__main__":
    # Ejecutar el servidor
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
