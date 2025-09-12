# Auto generated from simple_test.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-09-12T21:07:52
# Schema: simple_test
#
# id: https://w3id.org/linkml_coral/simple_test
# description: A minimal test schema for verifying package structure
# license: MIT

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Integer, String

metamodel_version = "1.7.0"
version = "1.0.0"

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SIMPLE_TEST = CurieNamespace('simple_test', 'https://w3id.org/linkml_coral/simple_test/')
DEFAULT_ = SIMPLE_TEST


# Types

# Class references
class PersonId(extended_str):
    pass


@dataclass(repr=False)
class Person(YAMLRoot):
    """
    A person entity
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SIMPLE_TEST["Person"]
    class_class_curie: ClassVar[str] = "simple_test:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = SIMPLE_TEST.Person

    id: Union[str, PersonId] = None
    name: Optional[str] = None
    age: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.age is not None and not isinstance(self.age, int):
            self.age = int(self.age)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PersonCollection(YAMLRoot):
    """
    A collection of persons
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SIMPLE_TEST["PersonCollection"]
    class_class_curie: ClassVar[str] = "simple_test:PersonCollection"
    class_name: ClassVar[str] = "PersonCollection"
    class_model_uri: ClassVar[URIRef] = SIMPLE_TEST.PersonCollection

    persons: Optional[Union[dict[Union[str, PersonId], Union[dict, Person]], list[Union[dict, Person]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="persons", slot_type=Person, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=SIMPLE_TEST.id, name="id", curie=SIMPLE_TEST.curie('id'),
                   model_uri=SIMPLE_TEST.id, domain=None, range=URIRef)

slots.name = Slot(uri=SIMPLE_TEST.name, name="name", curie=SIMPLE_TEST.curie('name'),
                   model_uri=SIMPLE_TEST.name, domain=None, range=Optional[str])

slots.age = Slot(uri=SIMPLE_TEST.age, name="age", curie=SIMPLE_TEST.curie('age'),
                   model_uri=SIMPLE_TEST.age, domain=None, range=Optional[int])

slots.persons = Slot(uri=SIMPLE_TEST.persons, name="persons", curie=SIMPLE_TEST.curie('persons'),
                   model_uri=SIMPLE_TEST.persons, domain=None, range=Optional[Union[dict[Union[str, PersonId], Union[dict, Person]], list[Union[dict, Person]]]])

