from fastapi import APIRouter
from .service import FiltersService

filters_router = APIRouter(prefix="/filters", tags=["Filters"])


@filters_router.get(path="/emotions", response_model=dict[str, str])
def get_emotions_filters():
  return FiltersService.get_emotions_filters()


@filters_router.get(path="/sentiments", response_model=dict[str, str])
def get_sentiments_filters():
  return FiltersService.get_sentiments_filters()


@filters_router.get(path="/categories-level1", response_model=dict[str, str])
def get_categories_level1_filters():
  return FiltersService.get_categories_level1_filters()


@filters_router.get(path="/categories-level2", response_model=dict[str, str])
def get_categories_level2_filters():
  return FiltersService.get_categories_level2_filters()
