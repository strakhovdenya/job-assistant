import sys
from pathlib import Path
from types import ModuleType

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_PATH = PROJECT_ROOT / "apps" / "frontend"

# ВАЖНО: добавляем путь сразу при импорте conftest,
# а не только внутри fixture
if str(FRONTEND_PATH) not in sys.path:
    sys.path.insert(0, str(FRONTEND_PATH))


class StopException(Exception):
    pass


class SessionState(dict):
    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        self[name] = value


class FakeStreamlit(ModuleType):
    def __init__(self):
        super().__init__("streamlit")
        self.session_state = SessionState()
        self.clicked_buttons = set()
        self.text_inputs = {}
        self.text_areas = {}
        self.number_inputs = {}
        self.messages = {
            "success": [],
            "error": [],
            "warning": [],
            "info": [],
            "write": [],
            "caption": [],
        }
        self.switched_page = None

    def set_page_config(self, *args, **kwargs):
        pass

    def title(self, value):
        self.messages["write"].append(value)

    def subheader(self, value):
        self.messages["write"].append(value)

    def write(self, value):
        self.messages["write"].append(value)

    def caption(self, value):
        self.messages["caption"].append(value)

    def success(self, value):
        self.messages["success"].append(value)

    def error(self, value):
        self.messages["error"].append(value)

    def warning(self, value):
        self.messages["warning"].append(value)

    def info(self, value):
        self.messages["info"].append(value)

    def stop(self):
        raise StopException()

    def button(self, label, key=None, **kwargs):
        return label in self.clicked_buttons or key in self.clicked_buttons

    def text_input(self, label, value="", **kwargs):
        return self.text_inputs.get(label, value)

    def text_area(self, label, value="", **kwargs):
        return self.text_areas.get(label, value)

    def number_input(self, label, value=1, **kwargs):
        return self.number_inputs.get(label, value)

    def selectbox(self, label, options, index=0, **kwargs):
        return options[index]

    def switch_page(self, page):
        self.switched_page = page

    def divider(self):
        pass

    def json(self, value):
        self.messages["write"].append(value)

    def container(self, **kwargs):
        return self

    def columns(self, spec):
        count = len(spec) if isinstance(spec, list) else spec
        return [self for _ in range(count)]

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


@pytest.fixture
def fake_streamlit(monkeypatch):

    for module_name in ["ui.state", "ui.components"]:
        sys.modules.pop(module_name, None)

    fake = FakeStreamlit()
    monkeypatch.setitem(sys.modules, "streamlit", fake)

    return fake


@pytest.fixture
def page_path():
    def _page_path(name: str) -> str:
        return str(FRONTEND_PATH / "pages" / name)

    return _page_path