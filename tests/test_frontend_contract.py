from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_frontend_package_json_exists():
    assert (PROJECT_ROOT / "frontend" / "package.json").exists()


def test_frontend_app_jsx_exists():
    assert (PROJECT_ROOT / "frontend" / "src" / "App.jsx").exists()


def test_frontend_api_js_exists():
    assert (PROJECT_ROOT / "frontend" / "src" / "api.js").exists()


def test_frontend_main_jsx_exists():
    assert (PROJECT_ROOT / "frontend" / "src" / "main.jsx").exists()


def test_frontend_styles_exist():
    assert (PROJECT_ROOT / "frontend" / "src" / "styles.css").exists()


def test_vite_config_exists():
    assert (PROJECT_ROOT / "frontend" / "vite.config.js").exists()


def test_frontend_no_external_ui_framework():
    pkg = (PROJECT_ROOT / "frontend" / "package.json").read_text(encoding="utf-8")
    for forbidden in ("antd", "@mui/", "tailwindcss", "@chakra-ui", "bootstrap"):
        assert forbidden not in pkg, f"unexpected dep {forbidden}"


def test_frontend_no_chart_library():
    pkg = (PROJECT_ROOT / "frontend" / "package.json").read_text(encoding="utf-8")
    for forbidden in ("recharts", "chart.js", "d3", "echarts"):
        assert forbidden not in pkg, f"unexpected dep {forbidden}"
