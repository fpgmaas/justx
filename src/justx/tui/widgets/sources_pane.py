from __future__ import annotations

from textual.message import Message
from textual.widgets import Label, ListItem, ListView

from justx.justfiles.models import JustxConfig, Source


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

    class SourceSelected(Message):
        """Emitted when a source is highlighted."""

        def __init__(self, source: Source) -> None:
            self.source = source
            super().__init__()

    def __init__(self, config: JustxConfig) -> None:
        self._id_to_source: dict[str, Source] = {}
        items = self._build_items(config)
        super().__init__(*items, id="sources")

    def _build_items(self, config: JustxConfig) -> list[ListItem]:
        items: list[ListItem] = []

        def make_header(title: str) -> ListItem:
            item = ListItem(Label(f" {title} "), classes="header")
            item.disabled = True
            return item

        items.append(make_header("Local"))
        for i, source in enumerate(config.local_sources):
            item_id = f"source-l{i}"
            self._id_to_source[item_id] = source
            items.append(ListItem(Label(f"  {source.name}"), id=item_id))

        items.append(make_header("Global"))
        for i, source in enumerate(config.global_sources):
            item_id = f"source-g{i}"
            self._id_to_source[item_id] = source
            items.append(ListItem(Label(f"  {source.name}"), id=item_id))

        return items

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if event.item and (source := self._id_to_source.get(event.item.id or "")):
            self.post_message(self.SourceSelected(source))
