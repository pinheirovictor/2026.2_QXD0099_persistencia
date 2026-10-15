from bson import ObjectId

from fastapi import HTTPException

def object_id(value: str) -> ObjectId:
    if not ObjectId.is_valid(value):
        raise HTTPException(status_code=422, detail="ID inválido")
    return ObjectId(value)

def to_api(doc: dict) -> dict:
    result = dict(doc)
    result["id"] = str(result.pop("_id"))
    for item in result.get("itens", []):
        item.pop("_id", None)
    return result