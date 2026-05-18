# Release Checklist — v3.0-rc

## Before tagging
- [ ] `python -m pytest` passes locally
- [ ] `python -m compileall backend/app tests tools` passes
- [ ] `npm run build` passes in `frontend/`
- [ ] CI passes on `main`

## Repository hygiene
- [ ] No `.venv/`
- [ ] No `frontend/node_modules/`
- [ ] No `frontend/dist/` or `frontend/.vite/`
- [ ] No `.pytest_cache/` or `__pycache__/`
- [ ] No `*.db` or `.env`
- [ ] `logs/*.log` and `logs/*.jsonl` are ignored
- [ ] No real data
- [ ] No real API keys
- [ ] No unauthorized scanning commands
- [ ] No exploit code
- [ ] README renders cleanly on GitHub
- [ ] Screenshots (optional) committed under `docs/screenshots/`

## Tagging

```cmd
git tag v3.0-rc
git push origin v3.0-rc
```
