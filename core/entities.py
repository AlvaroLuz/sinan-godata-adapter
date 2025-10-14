from __future__ import annotations
from pydantic.dataclasses import dataclass
from pydantic import TypeAdapter
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any

import os
import json



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


# ===== Estrutura principal ===== #


@dataclass
class DefaultCase:
    #default do sinan
    visualId: str
    outbreakId: str
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
    lastName: Optional[str] = None
    age: Optional[Age] = None#Optional[Dict[str, int]] = None
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


# ===== Exportar para JSON ===== #

# adapter = TypeAdapter(DefaultCase)
# json_str = adapter.dump_json(default_case, indent=4).decode()

# print(json_str)