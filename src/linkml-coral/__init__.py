try:
    from . import _version
    __version__ = _version.__version__
    __version_tuple__ = _version.__version_tuple__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)
