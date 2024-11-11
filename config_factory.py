import json
import os
from dataclasses import dataclass, fields, is_dataclass
from backend_common.common_config import CommonApiConfig



@dataclass
class ApiConfig(CommonApiConfig):
    enable_CORS_url: str = "http://localhost:3000"

    @classmethod
    def get_conf(cls):
        common_conf = CommonApiConfig.get_common_conf()
        conf = cls(**{f.name: getattr(common_conf, f.name) for f in fields(CommonApiConfig)})
        try:
            with open("secrets/secrets_gmap.json", "r", encoding="utf-8") as config_file:
                data = json.load(config_file)
                conf.api_key = data.get("gmaps_api", "")

            return conf
        except Exception as e:
            return conf


CONF = ApiConfig.get_conf()