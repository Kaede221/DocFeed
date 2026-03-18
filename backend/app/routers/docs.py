"""API routes for documentation operations."""

from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    FrameworkInfo,
    FrameworkListResponse,
    GenerateRequest,
    GenerateResponse,
)
from app.services.fetcher import (
    FRAMEWORKS,
    download_files_content,
    fetch_doc_files,
    list_modules,
)
from app.services.processor import build_context

router = APIRouter(prefix="/api", tags=["docs"])


def _get_framework(framework_id: str) -> FrameworkInfo:
    fw = FRAMEWORKS.get(framework_id)
    if not fw:
        raise HTTPException(status_code=404, detail=f"Framework '{framework_id}' not found")
    return fw


@router.get("/frameworks", response_model=FrameworkListResponse)
async def get_frameworks():
    """Return all supported frameworks with their available modules."""
    frameworks: list[FrameworkInfo] = []
    for fw in FRAMEWORKS.values():
        modules = await list_modules(fw.id)
        frameworks.append(fw.model_copy(update={"modules": modules}))
    return FrameworkListResponse(frameworks=frameworks)


@router.get("/frameworks/{framework_id}/modules")
async def get_modules(framework_id: str):
    """Return available documentation modules for a specific framework."""
    _get_framework(framework_id)
    modules = await list_modules(framework_id)
    return {"framework_id": framework_id, "modules": modules}


@router.post("/generate", response_model=GenerateResponse)
async def generate_context(req: GenerateRequest):
    """Generate formatted context text from selected framework modules."""
    fw = _get_framework(req.framework_id)

    if not req.module_paths:
        raise HTTPException(status_code=400, detail="At least one module path is required")

    # 1. List all .md files in selected modules
    doc_files = await fetch_doc_files(fw.id, req.module_paths)
    if not doc_files:
        raise HTTPException(status_code=404, detail="No markdown files found in selected modules")

    # 2. Download file contents concurrently
    file_contents = await download_files_content(doc_files)

    # 3. Build formatted context
    module_names = [p.split("/")[-1] for p in req.module_paths]
    context = build_context(fw.name, module_names, file_contents)

    return GenerateResponse(
        framework=fw.name,
        modules=module_names,
        context=context,
        file_count=len(file_contents),
        char_count=len(context),
    )