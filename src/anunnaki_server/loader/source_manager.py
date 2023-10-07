from anunnaki_source import Source
from anunnaki_source.models import * 

from dataclasses import dataclass
from typing import Type, List, Dict
import inspect
import json



@dataclass
class SourceManager:
    name: str
    id: int
    type: Type[Source]
    klass: Source

    @property
    def source_methods(self) -> List:
        return [method_name for method_name in self.klass.__dir__() 
                if method_name.startswith('get')]

    @property
    def source_attributes(self) -> Dict:
        return {
            field
            for c in self.klass.__class__.mro() if hasattr(c, '__annotations__')
            for field in c.__annotations__
        }
    
    @property
    def source_models(self):
        return [
            MediasPage, Media, Season, SeasonList, Episode, EpisodeList,
            Video, VideoList, Subtitle, SubtitleList,
            Filter, FilterList, Kind
        ]
    
    def get_attr(self, name):
        if name in self.source_attributes:
            return getattr(self.klass, name)
    
    async def call_method(self, method_name: str, data: bytes):
        dict_args = json.loads(data)
        if not isinstance(dict_args, dict):
            raise Exception("The methods arguments should only be passed as a json object")
        
        if not method_name in self.source_methods:
            raise NotImplementedError("The source doesn't implement this methods")
        
        method = getattr(self.klass, method_name)
        method_signature = inspect.signature(method)
        method_return_type = method_signature.return_annotation
        method_params = method_signature.parameters
        
        passed_kwargs = dict()
        for param_name, param_type in method_params.items():
            if param_name not in dict_args.keys():
                if param_type.default == inspect._empty:
                    raise TypeError(f"You didn't provide sufficient arguments: no {param_name}")
            
            arg_value = dict_args.get(param_name)
                    
            arg_type = param_type.annotation
            if arg_value is None:
                if arg_type == inspect._empty:
                    raise Exception(f"The called method parameter `{param_name}` doesn't specify a type")
                continue

            if arg_type in self.source_models:
                value = arg_type.model_validate(arg_value)
            else:
                value = arg_type(arg_value)

            passed_kwargs[param_name] = value

        # Call the method
        result = await method(**passed_kwargs)
        
        if method_return_type in self.source_models:
            return method_return_type.validate(result)
        return result