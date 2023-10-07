from anunnaki_server.model.extension import Extension
from dataclasses import dataclass

@dataclass
class Repo:
    """Used to get online extensions info"""
    url: str = "https://raw.githubusercontent.com/hasanpasha/anunnaki-extensions/repo"
    index_file: str = "index.min.json"

    def index_path(self):
        """Url path to index*.json"""
        return f"{self.url}/{self.index_file}"
    
    def unique_version_name(self, ext: Extension):
        """returns `{ext.lang}_{ext.pkg}_v{ext.version}`"""
        return f"{ext.lang}_{ext.pkg}_v{ext.version}"

    def zip_file(self, ext: Extension):
        """attach `.zip` to unique_version_name"""
        return f"{self.unique_version_name(ext)}.zip"
        
    def zip_url(self, ext: Extension):
        """append zip_file to repo.url"""
        return f"{self.url}/zip/{self.zip_file(ext)}"

    def icon_file(self, ext: Extension):
        """attach `.png` to unique_version_name"""
        return f"{self.unique_version_name(ext)}.png"
    
    def icon_url(self, ext: Extension):
        """append icon_file to repo.url"""
        return f"{self.url}/icon/{self.icon_file(ext)}"