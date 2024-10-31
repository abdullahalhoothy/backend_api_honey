from typing import Dict, List, TypeVar, Generic, Literal, Any, Optional
from decimal import Decimal

from pydantic import BaseModel, Field

T = TypeVar("T")


class UserRating(BaseModel):
    rating: str
    review: str
    username: str
    description: Optional[str] = None
    userimageurl: Optional[str] = None


class Product(BaseModel):
    id: str
    name: str
    description: str
    tagline: str
    producturl: str
    imageurl: str
    ratingtext: str
    ratingvalue: Optional[str] = None
    averagerating: Optional[str] = None
    totalratings: str
    discountedprice: str
    discountpercentage: str
    originalprice: str
    city: str
    country: str
    countryflagurl: str
    userrating: UserRating


class ProductDetail(BaseModel):
    product: Product


class UserReview(BaseModel):
    id: int
    name: str
    userProfileImageUrl: str
    description: str
    averageRating: Decimal
    totalRatings: int
    time: str


class UserReviews(BaseModel):
    reviews: List[UserReview]


class FavoriteProduct(BaseModel):
    id: int
    name: str
    searchType: str


class FavoriteProducts(BaseModel):
    products: List[FavoriteProduct]
