from dataclasses import dataclass

@dataclass(frozen=True)
class Currency:
    id: int 
    name: str
    code: str
    sign: str

    def to_dict(self):
        return {
                    "id": self.id,
                    "name": self.name,
                    "code": self.code,
                    "sign": self.sign
                }