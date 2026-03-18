"""GitHub API client for fetching documentation files."""

import asyncio

import httpx

from app.config import get_settings
from app.models.schemas import DocFile, DocModule, FrameworkInfo

GITHUB_API = "https://api.github.com"

# Framework registry — single source of truth
FRAMEWORKS: dict[str, FrameworkInfo] = {
    "vue3": FrameworkInfo(
        id="vue3",
        name="Vue 3",
        repo="vuejs/docs",
        docs_root="src/",
    ),
    "vue-router": FrameworkInfo(
        id="vue-router",
        name="Vue Router 4",
        repo="vuejs/router",
        docs_root="packages/docs/",
    ),
    "pinia": FrameworkInfo(
        id="pinia",
        name="Pinia",
        repo="vuejs/pinia",
        docs_root="packages/docs/",
    ),
}


def _build_headers() -> dict[str, str]:
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = get_settings().github_token
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


async def list_modules(framework_id: str) -> list[DocModule]:
    """List top-level sub-directories under the framework's docs root."""
    fw = FRAMEWORKS[framework_id]
    url = f"{GITHUB_API}/repos/{fw.repo}/contents/{fw.docs_root}"

    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(url, headers=_build_headers())
        resp.raise_for_status()

    modules: list[DocModule] = []
    for item in resp.json():
        if item["type"] == "dir":
            modules.append(
                DocModule(
                    name=item["name"],
                    path=item["path"],
                    label=item["name"].replace("-", " ").title(),
                )
            )
    return modules


async def _list_md_files_recursive(
    client: httpx.AsyncClient,
    repo: str,
    path: str,
) -> list[DocFile]:
    """Recursively list all .md files under a given path."""
    url = f"{GITHUB_API}/repos/{repo}/contents/{path}"
    resp = await client.get(url, headers=_build_headers())
    resp.raise_for_status()

    files: list[DocFile] = []
    sub_dirs: list[str] = []

    for item in resp.json():
        if item["type"] == "file" and item["name"].endswith(".md"):
            files.append(
                DocFile(
                    path=item["path"],
                    name=item["name"],
                    download_url=item["download_url"],
                )
            )
        elif item["type"] == "dir":
            sub_dirs.append(item["path"])

    # Recurse into sub-directories concurrently
    if sub_dirs:
        tasks = [_list_md_files_recursive(client, repo, d) for d in sub_dirs]
        results = await asyncio.gather(*tasks)
        for result in results:
            files.extend(result)

    return files


async def fetch_doc_files(
    framework_id: str, module_paths: list[str]
) -> list[DocFile]:
    """Get all .md file entries for the selected modules."""
    fw = FRAMEWORKS[framework_id]
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [
            _list_md_files_recursive(client, fw.repo, path)
            for path in module_paths
        ]
        results = await asyncio.gather(*tasks)

    return [f for batch in results for f in batch]


async def download_file_content(url: str) -> str:
    """Download raw file content from GitHub."""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        resp = await client.get(url, headers=_build_headers())
        resp.raise_for_status()
        return resp.text


async def download_files_content(files: list[DocFile]) -> dict[str, str]:
    """Download content for multiple files concurrently.

    Returns a dict mapping file path to its content.
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:

        async def _download(file: DocFile) -> tuple[str, str]:
            resp = await client.get(file.download_url, headers=_build_headers())
            resp.raise_for_status()
            return file.path, resp.text

        results = await asyncio.gather(*[_download(f) for f in files])

    return dict(results)