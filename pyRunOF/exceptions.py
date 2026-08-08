"""Public exception hierarchy for PyRunOF."""


class PyRunOFError(Exception):
    """Base exception raised by PyRunOF."""


class ConfigurationError(PyRunOFError, ValueError):
    """Raised when a case or runner configuration is invalid."""


class UnsafePathError(PyRunOFError, ValueError):
    """Raised when an operation targets a path outside its allowed root."""


class CommandExecutionError(PyRunOFError, RuntimeError):
    """Raised when an external solver process exits unsuccessfully."""
