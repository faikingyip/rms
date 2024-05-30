from typing import Optional


class OpsBaseError(Exception):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class CreateUserError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class DeleteUserError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class ChangePasswordError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class GetUserListError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class GetUserByIdError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class GetUserByUsernameError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class LoginError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class CreateDiningTableError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class DeleteDiningTableError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class UpdatePositionError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class UpdateSizeError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class UpdateNameError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class GetDiningTableListError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class GetMenuListError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class CreateMenuError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class DeleteMenuError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))


class GetMenuByIdError(OpsBaseError):
    def __init__(self, original_exception: Optional[Exception] = None):
        super().__init__(str(original_exception))
