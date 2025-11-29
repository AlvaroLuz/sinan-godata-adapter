from __future__ import annotations
from pydantic.dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class Document:
    type: str
    number: str

@dataclass
class Age: 
    years: int
    months : Optional[int] = None 

@dataclass
class Address:
    typeId: str
    city: Optional[str] = None
    addressLine1: Optional[str] = None
    postalCode: Optional[str] = None
    locationId: str = ""
    geoLocationAccurate: bool = False
    date: Optional[datetime] = None
    phoneNumber: Optional[str] = None
    geoLocation: Optional[Dict[str, float]] = None


@dataclass
class DuplicateKeys:
    document: List[Any]
    name: List[Any]

#classe meramente simbólica
#será usada para representar IDs do IBGE nos dados dos módulos dos agravos
@dataclass
class IBGEId:
    ...


# ===== Estrutura principal ===== #


@dataclass
class GoDataCase:
    #default do sinan
    visualId: str
    firstName: str
    gender: str
    pregnancyStatus: str
    documents: List[Document]
    addresses: List[Address]
    outcomeId: str
    classification: str
    dateOfReporting: datetime
    updatedAt: datetime
    questionnaireAnswers: Dict[str, List[Dict[str, Any]]]
    dateOfOnset: Optional[datetime]
    outbreakId: Optional[str] = None
    lastName: Optional[str] = None
    age: Optional[Age] = None
    dob: Optional[datetime] = None
    #Opcionais 
    transferRefused: Optional[bool] = False
    duplicateKeys: Optional[DuplicateKeys] = DuplicateKeys(document=[], name=[])
    dateRanges: Optional[List[Any]] = None
    classificationHistory: Optional[List[Any]] = None
    wasContact: Optional[bool] = False
    safeBurial: Optional[bool] = False
    riskLevel: Optional[str] = None
    occupation: Optional[str] = None
    vaccinesReceived: Optional[List[Any]] = None
    dateOfOutcome: Optional[datetime] = None
    hasRelationships: Optional[bool] = None
    locations: Optional[List[Any]] = None
    address: Optional[Dict[str, Any]] = None
    numberOfContacts: Optional[int] = None
    numberOfExposures: Optional[int] = None


@dataclass
class SinanCase:
    nu_notific: str
    #==== dados pessoais ====#
    nm_pacient: str
    dt_nasc: datetime
    cs_sexo: str
    cs_gestant: str
    nu_telefon: str
    #==== endereço ====#
    nu_cep: str
    municipio_residencia: str
    #==== dados clínicos ====#
    evolucao: str
    classificacao_final: str
    dt_notific: datetime
    #==== dados opcionais ====#
    id_cns_sus: Optional[str] = None
    nm_bairro: Optional[str] = None
    nm_logrado: Optional[str] = None
    nu_numero: Optional[str] = None
    nm_complemento: Optional[str] = None
    dt_sin_pri: Optional[datetime] = None

