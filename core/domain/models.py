from __future__ import annotations
from pydantic.dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import field

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
class GodataCase:
    #default do sinan
    addresses: List[Address]
    classification: str
    dateOfOnset: Optional[str]
    dateOfReporting: str
    documents: List[Document]
    firstName: str
    gender: str
    outbreakId: str
    outcomeId: str
    pregnancyStatus: str
    questionnaireAnswers: Dict[str, List[Dict[str, Any]]]
    updatedAt: str
    usualPlaceOfResidenceLocationId: str 
    visualId: str
    #default
    active: bool = True
    #age: Optional[Age] = None
    address: Dict[str, Any] = field(default_factory=dict)
    #classificationHistory: Optional[List[Any]] = None
    dateRanges: Optional[List[Any]] = field(default_factory=list)
    dob: Optional[str] = None
    duplicateKeys: Optional[DuplicateKeys] = DuplicateKeys(document=[], name=[])
    hasRelationships: Optional[bool] = False
    numberOfContacts: Optional[int] = 0
    numberOfExposures: Optional[int] = 0
    transferRefused: Optional[bool] = False
    safeBurial: Optional[bool] = False
    vaccinesReceived: Optional[List[Any]] = field(default_factory=list)
    wasContact: Optional[bool] = False
    wasContactOfContact: Optional[bool] = False



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

