from __future__ import annotations
from pydantic.dataclasses import dataclass
from pydantic import TypeAdapter
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any

import os
import json

# ===== Enums ===== #


class Classification(str, Enum):
    Confirmed = "LNG_REFERENCE_DATA_CATEGORY_CASE_CLASSIFICATION_CONFIRMED"
    Suspect = "LNG_REFERENCE_DATA_CATEGORY_CASE_CLASSIFICATION_SUSPECT"
    Descartado = "LNG_REFERENCE_DATA_CATEGORY_CASE_CLASSIFICATION_NOT_A_CASE_DISCARDED"

class Hospitalization(str, Enum):
    Isolation = "LNG_REFERENCE_DATA_CATEGORY_PERSON_DATE_TYPE_ISOLATION"
    Hospitalization = "LNG_REFERENCE_DATA_CATEGORY_PERSON_DATE_TYPE_HOSPITALIZATION"


# ===== Subestruturas ===== #

@dataclass
class DocumentObject:
    type: str
    number: str


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


# ===== Estrutura principal ===== #

@dataclass
class DefaultCase:
    firstName: str
    lastName: str
    gender: str
    wasContact: bool
    outcomeId: str
    safeBurial: bool
    classification: Classification
    riskLevel: str
    transferRefused: bool
    questionnaireAnswers: Dict[str, List[Dict[str, Any]]]
    vaccinesReceived: List[Any]
    pregnancyStatus: str
    outbreakId: Optional[str]
    dob: Optional[datetime]
    occupation: str
    documents: List[DocumentObject]
    addresses: List[Address]
    duplicateKeys: DuplicateKeys
    dateOfReporting: datetime
    dateOfOnset: Optional[datetime]
    dateRanges: List[Any]
    classificationHistory: List[Any]
    age: Optional[Dict[str, int]] = None
    dateOfOutcome: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    hasRelationships: Optional[bool] = None
    locations: Optional[List[Any]] = None
    address: Optional[Dict[str, Any]] = None
    numberOfContacts: Optional[int] = None
    numberOfExposures: Optional[int] = None


# default_case = DefaultCase(
#     firstName="",
#     lastName="",
#     gender=Gender.Empty,
#     wasContact=False,
#     outcomeId="",
#     safeBurial=False,
#     classification=Classification.Confirmed,
#     riskLevel="",
#     transferRefused=False,
#     questionnaireAnswers={},
#     vaccinesReceived=[],
#     pregnancyStatus=PregnancyStatus.None_,
#     outbreakId=os.getenv("OUTBREAK_ID"),
#     dob=None,
#     occupation="",
#     documents=[DocumentObject(type=DocumentType.Empty, number="")],
#     addresses=[
#         Address(
#             typeId="LNG_REFERENCE_DATA_CATEGORY_ADDRESS_TYPE_USUAL_PLACE_OF_RESIDENCE",
#             addressLine1="",
#             locationId="a042112a-518e-4414-bcc1-5a187da0e47b",
#             geoLocationAccurate=False,
#             date=None,
#         )
#     ],
#     duplicateKeys=DuplicateKeys(document=[], name=[]),
#     dateOfReporting=actual_date,
#     dateOfOnset=None,
#     dateRanges=[],
#     classificationHistory=[],
#     age=None
# )


# ===== Exportar para JSON ===== #

# adapter = TypeAdapter(DefaultCase)
# json_str = adapter.dump_json(default_case, indent=4).decode()

# print(json_str)