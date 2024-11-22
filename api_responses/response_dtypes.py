from typing import Dict, List, TypeVar, Generic, Literal, Any, Optional
from decimal import Decimal

from pydantic import BaseModel, Field

T = TypeVar("T")


class UserRating(BaseModel):
    rating: Optional[str]
    review: Optional[str]
    username: Optional[str]
    description: Optional[str] = None
    userimageurl: Optional[str] = None


class Product(BaseModel):
    id: Optional[str]
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
    userrating: Optional[str]


class ProductDetail(BaseModel):
    products: list[Product]


class UserReview(BaseModel):
    id: int
    name: Optional[str]
    userProfileImageUrl: Optional[str]
    description: Optional[str]
    averageRating: Decimal
    totalRatings: int
    time: Optional[str]


class UserReviews(BaseModel):
    reviews: List[UserReview]


class FavoriteProduct(BaseModel):
    id: int
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
    id: int
    type: str
    imageUrl: str


class CoffeeProductResponse(BaseModel):
    products: List[CoffeeProduct]


class Country(BaseModel):
    id: int
    name: str


class CountryResponse(BaseModel):
    countries: List[Country]


class Region(BaseModel):
    id: int
    name: str


class RegionResponse(BaseModel):
    shopByRegion: List[Region]
