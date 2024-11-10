class ArgInfo:
    """
    Represents information about a command-line argument.

    Attributes:
        flags (str): The command-line flags (e.g., "-h, --help").
        help (str): The help text describing the argument.
    """

    def __init__(self, flags: str, help: str, _builder: bool = False):
        """
        Initializes an ArgInfo instance.

        Args:
            flags (str): The command-line flags.
            help (str): The help text.
            _builder (bool): Internal flag to enforce builder usage.

        Raises:
            Exception: If not instantiated via ArgInfoBuilder.
        """
        if not _builder:
            raise Exception("ArgInfo must be created using ArgInfoBuilder.")
        self.flags = flags
        self.help = help

    def __repr__(self):
        return f"ArgInfo(flags='{self.flags}', help='{self.help}')"


class ArgInfoBuilder:
    """
    Builder class for constructing ArgInfo instances.
    """

    def __init__(self):
        self._flags = None
        self._help = None

    def set_flags(self, flags: str):
        self._flags = flags
        return self

    def set_help(self, help_text: str):
        self._help = help_text
        return self

    def build(self) -> ArgInfo:
        """
        Builds and returns an ArgInfo instance.

        Returns:
            ArgInfo: The constructed ArgInfo object.

        Raises:
            ValueError: If required fields are not set.
        """
        if not self._flags:
            raise ValueError("Flags must be set before building ArgInfo.")
        if not self._help:
            raise ValueError("Help text must be set before building ArgInfo.")
        return ArgInfo(flags=self._flags, help=self._help, _builder=True)
