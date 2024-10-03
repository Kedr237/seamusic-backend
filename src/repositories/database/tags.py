from dataclasses import dataclass

from sqlalchemy import select, insert, func

from src.converters.repositories.database.sqlalchemy import request_dto_to_model, models_to_dto
from src.dtos.database.tags import AddTagRequestDTO, TagsResponseDTO, Tag as _Tag, AddTagsRequestDTO
from src.models.auth import User, ArtistProfile, ProducerProfile
from src.models.tags import Tag
from src.repositories.database.base import SQLAlchemyRepository


@dataclass
class TagsRepository(SQLAlchemyRepository):
    async def add_tag(self, tag: AddTagRequestDTO) -> int:
        model = request_dto_to_model(model=Tag, request_dto=tag)
        await self.add(model)
        return model.id

    async def add_tags(self, tags: AddTagsRequestDTO) -> None:
        models = list(map(lambda tag: Tag(**tag.model_dump()), tags.tags))
        query = insert(Tag).values(models)
        await self.execute(query)

    async def get_listener_tags(self, user_id: int, offset: int = 0, limit: int = 10) -> TagsResponseDTO:
        query = select(User.followed_tags).filter_by(id=user_id).offset(offset).limit(limit).order_by(Tag.name.desc())
        tags = list(await self.scalars(query))
        return TagsResponseDTO(tags=models_to_dto(models=tags, dto=_Tag))

    async def get_listener_tags_count(self, user_id: int) -> int:
        query = select(func.count(User.followed_tags)).filter_by(id=user_id)
        return await self.scalar(query)

    async def get_producer_tags(self, producer_id: int, offset: int = 0, limit: int = 10) -> TagsResponseDTO:
        query = select(ProducerProfile.tags).filter_by(id=producer_id).offset(offset).limit(limit).order_by(Tag.name.desc())
        tags = list(await self.scalars(query))
        return TagsResponseDTO(tags=models_to_dto(models=tags, dto=_Tag))

    async def get_producer_tags_count(self, producer_id: int) -> int:
        query = select(func.count(ProducerProfile.id)).filter_by(id=producer_id)
        return await self.scalar(query)

    async def get_artist_tags(self, artist_id: int, offset: int = 0, limit: int = 10) -> TagsResponseDTO:
        query = select(ArtistProfile.tags).filter_by(id=artist_id).offset(offset).limit(limit).order_by(Tag.name.desc())
        tags = list(await self.scalars(query))
        return TagsResponseDTO(tags=models_to_dto(models=tags, dto=_Tag))

    async def get_artist_tags_count(self, artist_id: int) -> int:
        query = select(func.count(ArtistProfile.id)).filter_by(id=artist_id)
        return await self.scalar(query)


def init_tags_repository() -> TagsRepository:
    return TagsRepository()