class ToolInputError(Exception):
    """Raised when a tool argument is malformed or refers to unknown data.

    `arg` tells the agent WHICH argument to re-ask the user for.
    """

    def __init__(self, arg: str, message: str):
        super().__init__(message)
        self.arg = arg
        self.message = message