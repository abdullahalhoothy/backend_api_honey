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

        # Google Bucket fields
        conf.google_product_bucket_name = "vivi_app"
        conf.google_bucket_credentials_json_path = "secrets/weighty-gasket-437422-h6-a9caa84da98d.json"
        conf.google_product_bucket_path = "postgreSQL/dbo-coffee/raw_schema_marketplace/product_images"
        try:
            with open("secrets/secrets_gmap.json", "r", encoding="utf-8") as config_file:
                data = json.load(config_file)
                conf.api_key = data.get("gmaps_api", "")
            return conf
        except Exception as e:
            return conf


CONF = ApiConfig.get_conf()