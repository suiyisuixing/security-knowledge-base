# Frontend — Security Knowledge Base & Agent Memory Lab

React + Vite single-page frontend for the v3.0-rc release.

## Development

```cmd
cd /d C:\Users\27827\Desktop\Event\security-knowledge-base\frontend
npm install --registry=https://registry.npmmirror.com
npm run dev
```

Vite proxies `/api-backend/*` to the FastAPI backend at `http://127.0.0.1:8000`.

## Build

```cmd
npm run build
```

The frontend is intentionally framework-light: plain CSS, no chart library, no
external UI toolkit. All panels are card / table / pre-block.
