"""
MITRE ATT&CK data models using Pydantic.

These models represent the core entities from the MITRE ATT&CK framework.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class DataSource(BaseModel):
    """
    Represents a MITRE ATT&CK data source.

    Data sources describe the different types of information that can be collected
    to detect techniques.
    """
    model_config = ConfigDict(frozen=False, validate_assignment=True)

    name: str = Field(..., description="Name of the data source")
    description: Optional[str] = Field(None, description="Description of the data source")


class Tactic(BaseModel):
    """
    Represents a MITRE ATT&CK tactic.

    Tactics represent the "why" of an ATT&CK technique or sub-technique.
    They are the adversary's tactical goal: the reason for performing an action.
    """
    model_config = ConfigDict(frozen=False, validate_assignment=True)

    name: str = Field(..., description="Name of the tactic (e.g., 'initial-access')")
    description: Optional[str] = Field(None, description="Description of the tactic")


class Technique(BaseModel):
    """
    Represents a MITRE ATT&CK technique or sub-technique.

    Techniques represent "how" an adversary achieves a tactical goal by performing an action.
    Sub-techniques are more specific descriptions of the adversarial behavior.
    """
    model_config = ConfigDict(frozen=False, validate_assignment=True)

    external_id: str = Field(..., description="MITRE ATT&CK ID (e.g., 'T1234' or 'T1234.001')")
    name: str = Field(..., description="Name of the technique")
    description: str = Field(..., description="Detailed description of the technique")
    tactic: str = Field(..., description="Primary tactic associated with this technique")
    url: str = Field(..., description="URL to the technique's page on MITRE ATT&CK website")
    data_sources: List[str] = Field(
        default_factory=list,
        description="List of data sources that can be used to detect this technique"
    )
    is_subtechnique: bool = Field(
        default=False,
        description="Whether this is a sub-technique (True) or parent technique (False)"
    )
    parent_id: Optional[str] = Field(
        None,
        description="External ID of the parent technique (only for sub-techniques)"
    )

    @property
    def is_parent(self) -> bool:
        """Check if this technique is a parent technique (not a sub-technique)."""
        return not self.is_subtechnique

    @property
    def technique_id_parts(self) -> tuple:
        """
        Split the external_id into parent and sub-technique parts.

        Returns:
            tuple: (parent_id, sub_id) where sub_id is None for parent techniques

        Examples:
            'T1234' -> ('T1234', None)
            'T1234.001' -> ('T1234', '001')
        """
        if '.' in self.external_id:
            parts = self.external_id.split('.')
            return (parts[0], parts[1])
        return (self.external_id, None)

    def __str__(self) -> str:
        """String representation of the technique."""
        return f"{self.external_id}: {self.name}"

    def __repr__(self) -> str:
        """Detailed representation of the technique."""
        return (
            f"Technique(external_id='{self.external_id}', name='{self.name}', "
            f"tactic='{self.tactic}', is_subtechnique={self.is_subtechnique})"
        )
