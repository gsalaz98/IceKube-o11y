from __future__ import annotations

import json
from typing import List

from icekube.models.base import Resource
from icekube.models.policyrule import PolicyRule
from pydantic import root_validator
from pydantic.fields import Field


class ClusterRole(Resource):
    rules: List[PolicyRule] = Field(default_factory=list)

    @root_validator(pre=True)
    def inject_rules(cls, values):
        data = json.loads(values.get("raw", "{}"))

        if "rules" not in values or values["rules"] is None:
            values["rules"] = []

        if "rules" not in data or data["rules"] is None:
            data["rules"] = []

        for rule in data.get("rules", []):
            values["rules"].append(PolicyRule(**rule))

        return values
