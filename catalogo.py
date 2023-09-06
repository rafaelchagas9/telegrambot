from typing import List
from typing import Any
from dataclasses import dataclass
import json


@dataclass
class Servico:
    nome: str
    descricao: str
    imagem: str
    valor: float

    @staticmethod
    def from_dict(obj: Any) -> 'Servico':
        _nome = str(obj.get("nome"))
        _descricao = str(obj.get("descricao"))
        _imagem = str(obj.get("imagem"))
        _valor = float(obj.get("valor"))
        return Servico(_nome, _descricao, _imagem, _valor)


@dataclass
class Assinatura:
    nome: str
    descricao: str
    imagem: str
    valor: float

    @staticmethod
    def from_dict(obj: Any) -> 'Assinatura':
        _nome = str(obj.get("nome"))
        _descricao = str(obj.get("descricao"))
        _imagem = str(obj.get("imagem"))
        _valor = float(obj.get("valor"))
        return Assinatura(_nome, _descricao, _imagem, _valor)


@dataclass
class Pacote:
    nome: str
    descricao: str
    imagem: str
    valor: float

    @staticmethod
    def from_dict(obj: Any) -> 'Pacote':
        _nome = str(obj.get("nome"))
        _descricao = str(obj.get("descricao"))
        _imagem = str(obj.get("imagem"))
        _valor = float(obj.get("valor"))
        return Pacote(_nome, _descricao, _imagem, _valor)
    

@dataclass
class Catalogo:
    pacotes: List[Pacote]
    assinaturas: List[Assinatura]
    servicos: List[Servico]

    @staticmethod
    def from_dict(obj: Any) -> 'Catalogo':
        _pacotes = [Pacote.from_dict(y) for y in obj.get("pacotes")]
        _assinaturas = [Assinatura.from_dict(y) for y in obj.get("assinaturas")]
        _servicos = [Servico.from_dict(y) for y in obj.get("servicos")]
        return Catalogo(_pacotes, _assinaturas, _servicos)
    

@dataclass
class Root:
    catalogo: Catalogo

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _catalogo = Catalogo.from_dict(obj.get("catalogo"))
        return Root(_catalogo)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
