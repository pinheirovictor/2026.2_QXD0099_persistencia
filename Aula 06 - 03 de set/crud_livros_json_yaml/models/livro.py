from pydantic import BaseModel, Field


class Livro(BaseModel):
    id: int = Field(
        gt=0,
        description="Identificador único do livro",
    )

    titulo: str = Field(
        min_length=2,
        max_length=150,
    )

    autor: str = Field(
        min_length=2,
        max_length=100,
    )

    ano: int = Field(
        ge=1000,
        le=2100,
    )

    categorias: list[str] = Field(
        min_length=1,
        description="Lista de categorias do livro",
    )

    disponivel: bool = True
