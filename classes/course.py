from dataclasses import dataclass
@dataclass
class Course:
    """A data class used to represent a Couse"""
    subject_code: str
    subject_number: str
    name: str
    has_lab: bool
    lab_units: int
    lec_units: int

    @property
    def all_attr(self):
        """Returns all defined attributes"""
        return [self.subject_code, self.subject_number, self.name, self.has_lab, 
                self.lab_units, self.lec_units]

    @property
    def total_units(self) -> int:
        """Returns the total amount of units credited to this course"""
        return self.lab_units + self.lec_units
    
    @property
    def code(self) -> str:
        """Returns the course code"""
        return f"{self.subject_code} {self.subject_number}"

    def __repr__(self) -> str:
        return f"{self.code}: {self.name}"