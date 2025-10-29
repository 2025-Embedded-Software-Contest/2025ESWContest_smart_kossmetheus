from __future__ import annotations

try:
    from kiwipiepy import Kiwi

    _kiwi_instance: Kiwi | None = None
    KIWI_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency
    Kiwi = None  # type: ignore
    _kiwi_instance = None
    KIWI_AVAILABLE = False


def get_kiwi() -> Kiwi:
    if not KIWI_AVAILABLE:
        raise RuntimeError("Kiwi is not available in this environment")
    global _kiwi_instance
    if _kiwi_instance is None:
        _kiwi_instance = Kiwi()
    return _kiwi_instance

