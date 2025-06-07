from ..additional_fun.information import Information
from typing import Optional, overload
class ModelConfigurator(Information): 
    @overload
    def duplicate_case(
        self,
        src_path: Optional[str] = None,
        dist_path: Optional[str] = None,
        src_key: Optional[str] = None,
        dist_key: Optional[str] = None,
        mode: str = "copy",
    ) -> None:...