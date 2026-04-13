from dataclasses import dataclass


@dataclass
class DNASequence:
    sequence: str

    def validate(self):
        allowed = set("ATCG")
        if not set(self.sequence).issubset(allowed):
            raise ValueError("Invalid DNA sequence")

    def steps(self):
        return [
            self.sequence[i:i+2]
            for i in range(len(self.sequence)-1)
        ]
