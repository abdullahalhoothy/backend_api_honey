from typing import Dict, List, TypeVar, Generic, Literal, Any, Optional

from pydantic import BaseModel, Field

T = TypeVar("T")


class ResModel(BaseModel, Generic[T]):
    message: str
    request_id: str
    data: T


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


FavorateProductsResponse = ResModel[List[Product]]
PreferenceProductDetailResponse = ResModel[ProductDetail]
