from __future__ import annotations

from justx.config.settings.discovery import DEFAULT_EXCLUDE, DiscoveryConfig


def test_defaults() -> None:
    config = DiscoveryConfig()
    assert config.recursive is False
    assert config.max_depth == 3
    assert config.exclude == DEFAULT_EXCLUDE
    assert config.extend_exclude == []


def test_effective_exclude_without_extend() -> None:
    config = DiscoveryConfig()
    assert config.effective_exclude == set(DEFAULT_EXCLUDE)


def test_effective_exclude_with_extend() -> None:
    config = DiscoveryConfig(extend_exclude=["vendor", ".mypy_cache"])
    assert config.effective_exclude == set(DEFAULT_EXCLUDE) | {"vendor", ".mypy_cache"}


def test_custom_exclude_replaces_default() -> None:
    config = DiscoveryConfig(exclude=["only_this"])
    assert config.exclude == ["only_this"]
    assert config.effective_exclude == {"only_this"}


def test_exclude_default_is_independent_copy() -> None:
    a = DiscoveryConfig()
    b = DiscoveryConfig()
    a.exclude.append("extra")
    assert "extra" not in b.exclude
