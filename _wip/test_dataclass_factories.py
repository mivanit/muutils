# NOTE: This is a manual test. the tests in this file are not run by pytest.

from typing import Any

from muutils._wip.dataclass_factories import (
    dataclass_loader_factory,
    dataclass_serializer_factory,
)
from muutils.json_serialize import JSONitem


def _test():
    # @augement_dataclass_serializer_loader(
    #     special_serializers=dict(rand_data=lambda self: str(self.rand_data)),
    # )
    @dataclass
    class TestClass:
        a: int
        b: str
        c: float
        rand_data: Any = None

    TestClass.serialize = dataclass_serializer_factory(
        TestClass,
        special_serializers=dict(rand_data=lambda self: str(self.rand_data)),
    )
    TestClass.load = dataclass_loader_factory(TestClass)

    # @augement_dataclass_serializer_loader
    @dataclass
    class OuterTestClass:
        a2: int
        b2: str
        c2: float
        d2: TestClass

    OuterTestClass.serialize = dataclass_serializer_factory(OuterTestClass)
    OuterTestClass.load = dataclass_loader_factory(OuterTestClass)

    item_a: TestClass = TestClass(a=1, b="x", c=3.0)
    item_b: OuterTestClass = OuterTestClass(a2=2, b2="y", c2=4.0, d2=item_a)

    print(f"{item_a = }")
    print(f"{item_a.serialize() = }")
    print(f"{item_b = }")
    print(f"{item_b.serialize() = }")

    item_b_ser: JSONitem = item_b.serialize()

    item_b_loaded: OuterTestClass = OuterTestClass.load(item_b_ser)

    # assert item_b_loaded == item_b
    # assert item_b_loaded.d2 == item_a

    print(f"{item_b_loaded = }")
    print(f"{item_b_loaded.serialize() = }")
