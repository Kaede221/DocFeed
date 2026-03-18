from pydantic import BaseModel


class DocFile(BaseModel):
    """A single documentation file from a GitHub repository."""

    path: str
    name: str
    download_url: str


class DocModule(BaseModel):
    """A documentation module (sub-directory) within a framework."""

    name: str
    path: str
    label: str  # human-readable label, e.g. "Guide", "API"


class FrameworkInfo(BaseModel):
    """Metadata for a supported framework."""

    id: str  # e.g. "vue3"
    name: str  # e.g. "Vue 3"
    repo: str  # e.g. "vuejs/docs"
    docs_root: str  # e.g. "src/"
    modules: list[DocModule] = []


class FrameworkListResponse(BaseModel):
    frameworks: list[FrameworkInfo]


class GenerateRequest(BaseModel):
    """Request body for generating context text."""

    framework_id: str
    module_paths: list[str]  # selected module paths, e.g. ["src/guide", "src/api"]


class GenerateResponse(BaseModel):
    framework: str
    modules: list[str]
    context: str
    file_count: int
    char_count: int