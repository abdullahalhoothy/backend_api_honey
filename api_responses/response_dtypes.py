from typing import Dict, List, TypeVar, Generic, Literal, Any, Optional
from decimal import Decimal

from pydantic import BaseModel, Field

T = TypeVar("T")


class UserRating(BaseModel):
    review_id:str
    rating: Optional[str]
    review: Optional[str]
    username: Optional[str]
    description: Optional[str] = None
    userimageurl: Optional[str] = None


class Product(BaseModel):
    product_id: Optional[str]
    name: Optional[str]
    description: Optional[str]
    tagline: Optional[str]
    producturl: Optional[str]
    imageurl: Optional[str]
    averagerating: Optional[str] = None
    totalratings: Optional[str]
    discountedprice: Optional[str]
    discountpercentage: Optional[str]
    originalprice: Optional[str]
    city: Optional[str]
    country: Optional[str]
    userrating: UserRating


class ProductDetail(BaseModel):
    products: list[Product]


class UserReview(BaseModel):
    review_id: int
    name: Optional[str]
    userProfileImageUrl: Optional[str]
    description: Optional[str]
    averageRating: Decimal
    totalRatings: int
    time: Optional[str]


class UserReviews(BaseModel):
    reviews: List[UserReview]


class FavoriteProduct(BaseModel):
    product_id: int
    name: Optional[str]
    searchType: Optional[str]


class FavoriteProducts(BaseModel):
    products: List[FavoriteProduct]


class CoffeeBean(BaseModel):
    id: int
    name: str
    colorCode: str


class CoffeeBeanResponse(BaseModel):
    coffeeBeanTypes: List[CoffeeBean]


class CoffeeProduct(BaseModel):
    product_id: int
    type: str
    imageUrl: str


class CoffeeProductResponse(BaseModel):
    products: List[CoffeeProduct]


class Country(BaseModel):
    id: int
    name: str
    imageUrl: str


class CountryResponse(BaseModel):
    countries: List[Country]


class Region(BaseModel):
    id: int
    name: str
    imageUrl: str


class RegionResponse(BaseModel):
    shopByRegion: List[Region]


class CoffeeDataResponse(BaseModel):
    coffeeData: dict


class ProductFiltersRequest(BaseModel):
    typeIds: List[int]
    minRatingValue: str
    minPrice: str
    maxPrice: str
    countryNames: List[str]
    regionIds: List[int]
    rawMaterialIds: List[int]
    styleIds: List[int]
    sizeIds: List[int]

class UserReviewRequest(BaseModel):
    review_id: int

class SingleUserReview(Product):
    price: Optional[str] = None
    countryflagurl: Optional[str] = None
    
    class Config:
        # Allow population by field name for flexibility
        allow_population_by_field_name = True

class UserReviewsRequest(BaseModel):
    type: str = Field(..., description="Can be helpful/recent/all")