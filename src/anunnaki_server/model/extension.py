from anunnaki_server.utils import serialize_version
from pydantic import BaseModel, RootModel
from typing import List

class Extension(BaseModel):
    id: int
    pkg: str
    name: str
    version: str
    lang: str
    base_url: str = None
    installed: bool = False
    has_new_update: bool = False

    def is_same_version(self, other: 'Extension') -> bool:
        return serialize_version(self.version) == serialize_version(other.version)

    def mark_extension(self, compare_to: List['Extension']) -> 'Extension':
        for c_ext in compare_to:
            if self == c_ext:
                self.installed = True
                self.has_new_update = self > c_ext
                return self
        else:
            self.installed = False
            self.has_new_update = False
            return self

    def __hash__(self) -> int:
        return self.id

    def __lt__(self, other: 'Extension') -> bool:
        return serialize_version(self.version) < serialize_version(other.version)
    
    def __gt__(self, other: 'Extension') -> bool:
        return serialize_version(self.version) > serialize_version(other.version)

    def __eq__(self, other: 'Extension') -> bool:
        return self.id == other.id
   
    
class ExtensionList(RootModel):
    root: List[Extension]