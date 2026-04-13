from __future__ import annotations

from pathlib import Path
from typing import List

from app.models.sequence import DNASequence


class SequenceReader:
    """
    Repository for reading DNA sequences from different sources.

    Supports:
    - Raw string input
    - Plain text files
    - FASTA files
    """

    VALID_BASES = {"A", "T", "C", "G", "N"}

    # =========================
    # Public API
    # =========================

    @staticmethod
    def from_string(sequence: str) -> DNASequence:
        """
        Create DNASequence from raw string.
        """
        cleaned = SequenceReader._clean(sequence)
        SequenceReader._validate(cleaned)
        return DNASequence(sequence=cleaned)

    @staticmethod
    def from_file(path: Path) -> DNASequence:
        """
        Auto-detect file type and parse.
        """
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        if path.suffix.lower() in {".fa", ".fasta"}:
            return SequenceReader._read_fasta(path)

        return SequenceReader._read_text(path)

    @staticmethod
    def read_multiple_fasta(path: Path) -> List[DNASequence]:
        """
        Read multiple sequences from a FASTA file.
        """
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        sequences = []
        current_seq = []

        with path.open("r") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                if line.startswith(">"):
                    if current_seq:
                        seq = "".join(current_seq)
                        cleaned = SequenceReader._clean(seq)
                        SequenceReader._validate(cleaned)
                        sequences.append(DNASequence(sequence=cleaned))
                        current_seq = []
                else:
                    current_seq.append(line)

            # last sequence
            if current_seq:
                seq = "".join(current_seq)
                cleaned = SequenceReader._clean(seq)
                SequenceReader._validate(cleaned)
                sequences.append(DNASequence(sequence=cleaned))

        return sequences

    # =========================
    # Internal Methods
    # =========================

    @staticmethod
    def _read_text(path: Path) -> DNASequence:
        """
        Read plain text sequence file.
        """
        with path.open("r") as f:
            content = f.read()

        cleaned = SequenceReader._clean(content)
        SequenceReader._validate(cleaned)

        return DNASequence(sequence=cleaned)

    @staticmethod
    def _read_fasta(path: Path) -> DNASequence:
        """
        Read single-sequence FASTA file.
        """
        sequence_lines = []

        with path.open("r") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith(">"):
                    continue

                sequence_lines.append(line)

        if not sequence_lines:
            raise ValueError("No sequence found in FASTA file")

        sequence = "".join(sequence_lines)

        cleaned = SequenceReader._clean(sequence)
        SequenceReader._validate(cleaned)

        return DNASequence(sequence=cleaned)

    @staticmethod
    def _clean(sequence: str) -> str:
        """
        Normalize sequence:
        - Remove whitespace
        - Uppercase
        """
        return "".join(sequence.split()).upper()

    @staticmethod
    def _validate(sequence: str):
        """
        Validate DNA sequence.
        """
        invalid_chars = set(sequence) - SequenceReader.VALID_BASES

        if invalid_chars:
            raise ValueError(
                f"Invalid DNA bases found: {invalid_chars}"
            )

        if len(sequence) == 0:
            raise ValueError("Sequence is empty")
