from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Iterable


# =========================
# Core PDB Domain Objects
# =========================

@dataclass(frozen=True)
class Atom:
    """
    Represents a single atom in a PDB structure.
    """
    serial: int
    name: str
    residue_name: str
    chain_id: str
    residue_seq: int
    x: float
    y: float
    z: float
    occupancy: float = 1.0
    temp_factor: float = 0.0
    element: Optional[str] = None

    def to_pdb_line(self) -> str:
        """
        Convert atom to standard PDB formatted line.
        """
        return (
            f"ATOM  {self.serial:5d} "
            f"{self.name:<4}"
            f"{self.residue_name:>3} "
            f"{self.chain_id:1}"
            f"{self.residue_seq:4d}    "
            f"{self.x:8.3f}"
            f"{self.y:8.3f}"
            f"{self.z:8.3f}"
            f"{self.occupancy:6.2f}"
            f"{self.temp_factor:6.2f}          "
            f"{(self.element or ''):>2}"
        )


@dataclass
class Residue:
    """
    Represents a residue (e.g., nucleotide or amino acid).
    """
    name: str
    sequence_number: int
    atoms: List[Atom] = field(default_factory=list)

    def add_atom(self, atom: Atom) -> None:
        self.atoms.append(atom)

    def __iter__(self) -> Iterable[Atom]:
        return iter(self.atoms)


@dataclass
class Chain:
    """
    Represents a chain in the PDB structure.
    """
    chain_id: str
    residues: List[Residue] = field(default_factory=list)

    def add_residue(self, residue: Residue) -> None:
        self.residues.append(residue)

    def get_or_create_residue(
        self,
        residue_name: str,
        sequence_number: int
    ) -> Residue:
        for res in self.residues:
            if res.sequence_number == sequence_number:
                return res

        new_res = Residue(
            name=residue_name,
            sequence_number=sequence_number
        )
        self.residues.append(new_res)
        return new_res

    def __iter__(self) -> Iterable[Residue]:
        return iter(self.residues)


@dataclass
class PDBStructure:
    """
    Represents a full PDB structure.
    """
    title: Optional[str] = None
    chains: List[Chain] = field(default_factory=list)

    # =========================
    # Chain Operations
    # =========================

    def get_or_create_chain(self, chain_id: str) -> Chain:
        for chain in self.chains:
            if chain.chain_id == chain_id:
                return chain

        new_chain = Chain(chain_id=chain_id)
        self.chains.append(new_chain)
        return new_chain

    def add_atom(self, atom: Atom) -> None:
        """
        Add atom to correct chain/residue hierarchy.
        """
        chain = self.get_or_create_chain(atom.chain_id)
        residue = chain.get_or_create_residue(
            residue_name=atom.residue_name,
            sequence_number=atom.residue_seq
        )
        residue.add_atom(atom)

    # =========================
    # Iterators
    # =========================

    def iter_atoms(self) -> Iterable[Atom]:
        for chain in self.chains:
            for residue in chain:
                for atom in residue:
                    yield atom

    def iter_residues(self) -> Iterable[Residue]:
        for chain in self.chains:
            for residue in chain:
                yield residue

    def iter_chains(self) -> Iterable[Chain]:
        return iter(self.chains)

    # =========================
    # Export
    # =========================

    def to_pdb(self) -> str:
        """
        Export entire structure to PDB formatted string.
        """
        lines = []

        if self.title:
            lines.append(f"TITLE     {self.title}")

        for atom in self.iter_atoms():
            lines.append(atom.to_pdb_line())

        lines.append("END")

        return "\n".join(lines)

    # =========================
    # Utility Methods
    # =========================

    def atom_count(self) -> int:
        return sum(1 for _ in self.iter_atoms())

    def residue_count(self) -> int:
        return sum(1 for _ in self.iter_residues())

    def chain_count(self) -> int:
        return len(self.chains)
