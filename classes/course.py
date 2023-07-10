from dataclasses import dataclass

@dataclass
class Course:
    """A data class used to represent a Couse"""
    subject_code: str
    subject_number: int
    name: str
    has_lab: bool
    lab_units: int
    lec_units: int
    
    total_units: lab_units + lec_units
    code: str = f"{subject_code} {subject_number}"

    @property
    def all_attr(self):
        return [self.subject_code, self.subject_number, self.name, self.has_lab, 
                self.lab_units, self.lec_units]

    def __repr__(self) -> str:
        return f"{self.code}: {self.name}"