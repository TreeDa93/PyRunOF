from typing import overload

from ..additional_fun.information import Information

class ModelConfigurator(Information):
    @overload
    def duplicate_case(
        self,
        src_path: str | None = None,
        dist_path: str | None = None,
        src_key: str | None = None,
        dist_key: str | None = None,
        mode: str = "copy",
    ) -> None: ...
