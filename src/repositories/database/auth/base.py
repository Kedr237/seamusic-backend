from abc import ABC, abstractmethod
from dataclasses import dataclass

from pydantic import EmailStr

from src.dtos.database.auth import (
    ArtistResponseDTO,
    ArtistsResponseDTO,
    CreateArtistRequestDTO,
    CreateProducerRequestDTO,
    CreateUserRequestDTO,
    ProducerResponseDTO,
    ProducersResponseDTO,
    UpdateUserRequestDTO,
    UpdateArtistRequestDTO,
    UpdateProducerRequestDTO,
    UserResponseDTO,
    UsersResponseDTO,
)


@dataclass
class BaseUsersRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> UserResponseDTO | None:
        ...

    @abstractmethod
    async def get_user_by_email(self, email: EmailStr) -> UserResponseDTO | None:
        ...

    @abstractmethod
    async def get_users(self, offset: int = 0, limit: int = 10) -> UsersResponseDTO:
        ...

    @abstractmethod
    async def get_users_count(self) -> int:
        ...

    @abstractmethod
    async def create_user(self, user: CreateUserRequestDTO) -> int:
        ...

    @abstractmethod
    async def update_user(self, user: UpdateUserRequestDTO) -> int:
        ...

    @abstractmethod
    async def delete_user(self, user_id: int) -> None:
        ...


@dataclass
class BaseArtistsRepository(ABC):
    @abstractmethod
    async def get_artist_id_by_user_id(self, user_id: int) -> int | None:
        ...

    @abstractmethod
    async def get_artist_by_id(self, artist_id: int) -> ArtistResponseDTO | None:
        ...

    @abstractmethod
    async def get_artists(self, offset: int = 0, limit: int = 10) -> ArtistsResponseDTO:
        ...

    @abstractmethod
    async def get_artists_count(self) -> int:
        ...

    @abstractmethod
    async def create_artist(self, artist: CreateArtistRequestDTO) -> int:
        ...

    @abstractmethod
    async def update_artist(self, artist: UpdateArtistRequestDTO) -> int:
        ...


@dataclass
class BaseProducersRepository(ABC):
    @abstractmethod
    async def get_producer_id_by_user_id(self, user_id: int) -> int | None:
        ...

    @abstractmethod
    async def get_producer_by_id(self, producer_id: int) -> ProducerResponseDTO | None:
        ...

    @abstractmethod
    async def get_producers(self, offset: int = 0, limit: int = 10) -> ProducersResponseDTO:
        ...

    @abstractmethod
    async def get_producers_count(self) -> int:
        ...

    @abstractmethod
    async def create_producer(self, producer: CreateProducerRequestDTO) -> int:
        ...

    @abstractmethod
    async def update_producer(self, producer: UpdateProducerRequestDTO) -> int:
        ...
