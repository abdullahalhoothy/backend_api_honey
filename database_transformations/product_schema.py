SCHEMA = {
    "product_id": "TEXT PRIMARY KEY",
    "name": "varchar(70)",
    "description": "text",
    "tagline": "text",
    "producturl": "varchar(500)",
    "imageurl": "varchar(500)",
    "ratingtext": "varchar(10000)",
    "ratingvalue": "varchar(10000)",
    "averagerating": "varchar(10000)",
    "totalratings": "varchar(10000)",
    "discountedPrice": "varchar(10000)",
    "discountPercentage": "varchar(10000)",
    "originalPrice": "varchar(10000)",
    "city": "varchar(30)",
    "country": "varchar(30)",
    "countryflagurl": "varchar(500)",
    "userRating": "JSONB",
    "additionalDetail": "JSONB",
}


REVIEW = {
    "review_id": "TEXT PRIMARY KEY UNIQUE",
    "consumerName": "TEXT",
    "outOf5Rating": "TEXT",
    "description": "TEXT",
    "product_id": "TEXT",
    "CONSTRAINT fk_product": 'FOREIGN KEY (product_id) REFERENCES "schema_marketplace".products(product_id)',
}
