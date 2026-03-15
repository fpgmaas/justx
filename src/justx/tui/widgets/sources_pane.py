from __future__ import annotations

from typing import Any, ClassVar

from textual.binding import Binding
from textual.message import Message
from textual.widgets import Label, ListItem, ListView

from justx.justfiles.models import JustxConfig, Source
from justx.tui.utils import first_enabled_index


class SourceListItem(ListItem):
    """A ListItem that carries a reference to its Source."""

    def __init__(self, *args: Any, source: Source, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.source = source


class SourcesPane(ListView):
    """Left pane — lists justfile sources grouped by scope."""

    DEFAULT_CSS = """
    SourcesPane > ListItem.header {
        background: $panel;
        color: $accent;
        text-style: bold;
    }
    SourcesPane > ListItem.header:hover {
        background: $panel;
    }
    """

    BINDINGS: ClassVar = [
        Binding("enter", "activate", "Select", show=False, priority=True),
    ]

    class SourceSelected(Message):
        """Emitted when a source is highlighted."""

        def __init__(self, source: Source) -> None:
            self.source = source
            super().__init__()

    class SourceActivated(Message):
        """Emitted when the user confirms a source (Enter key)."""

    def __init__(self, config: JustxConfig) -> None:
        self._config = config
        self._query = ""
        super().__init__(id="sources")
        self.border_title = "Sources"

    def on_mount(self) -> None:
        self._rebuild()

    def filter(self, query: str) -> None:
        self._query = query
        self._rebuild()

    def _rebuild(self) -> None:
        self.clear()

        local_sources = [s for s in self._config.local_sources if s.filter_recipes(self._query)]
        global_sources = [s for s in self._config.global_sources if s.filter_recipes(self._query)]

        def make_header(title: str) -> ListItem:
            item = ListItem(Label(f" {title} "), classes="header")
            item.disabled = True
            return item

        if local_sources:
            self.append(make_header("Local"))
            for source in local_sources:
                self.append(SourceListItem(Label(f"  {source.name}"), source=source))

        if global_sources:
            self.append(make_header("Global"))
            for source in global_sources:
                self.append(SourceListItem(Label(f"  {source.name}"), source=source))

        self.call_after_refresh(lambda: setattr(self, "index", first_enabled_index(self)))

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if isinstance(event.item, SourceListItem):
            self.post_message(self.SourceSelected(event.item.source))

    def action_activate(self) -> None:
        self.post_message(self.SourceActivated())
