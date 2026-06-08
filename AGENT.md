# SmartLogicComputSciPlatform Coding Guidelines

## 1. File Structure Guidelines

### 1.1 Module Docstrings
- **Every file must start with a docstring** explaining the module's purpose
- May include references, usage instructions, etc.
- Example:
```python
'''
Utils for the classical forcefields

References:
https://ambermd.org/antechamber/ac.html
'''
```

### 1.2 Import Order
Organize imports in the following order:
1. Standard library
2. Third-party libraries
3. Local project modules

Example:
```python
import re
import os
from pathlib import Path
from typing import List, Optional

import numpy as np
from ase.io import read, write

from slcsp.ui.utils import find_available_port
```

### 1.3 Special Variable Definitions
- Use `here = Path(__file__).parent` to get the current file's directory
- Module-level constants use uppercase letters

---

## 2. Type Annotation Guidelines

### 2.1 Function Signatures
- **All functions must have complete type annotations**
- Include parameter types and return types
- Use composite types from the `typing` module

Example:
```python
def calculate_charges(
    atoms: Atoms,
    charge_method: str = 'bcc',
    fmol2: Optional[str | Path] = None,
    with_atoms: bool = False,
) -> List[float] | Tuple[List[float], Atoms]:
```

### 2.2 Type Aliases
- Use type aliases for complex types to improve readability
- Type aliases use PascalCase naming

Example:
```python
LammpsBlockRegion = Tuple[float, float, float, float, float, float]
Serialized = Dict[str, Any]
```

---

## 3. Docstring Guidelines

All docstrings must in **English**, no matter what language the prompt is in.

### 3.1 Function Docstrings
**Must include**:
- Brief description of function functionality
- Parameters section (all parameters)
- Returns section (return values)

Example:
```python
def modify_residual_name(
    atoms: Atoms,
    fres: Callable[[Atom], str],
) -> Atoms:
    '''
    Modify the residual name in the pdb file.
    
    Parameters
    ----------
    atoms : Atoms
        The atoms object to modify the residual name in.
    fres : Callable[[Atom], str]
        The function to modify the residual name.
    
    Returns
    -------
    Atoms
        The modified atoms object.
    '''
```

### 3.2 Class Docstrings
- Describe the class's purpose
- List main attributes (Attributes)

---

## 4. Naming Guidelines

### 4.1 Variables and Functions
- Use **snake_case** (lowercase + underscore)
- Boolean variables use `is_`, `has_`, `with_` prefixes

Example:
```python
with_atoms: bool
is_valid: bool
has_error: bool
```

### 4.2 Class Names
- Use **PascalCase** (Upper Camel Case)

Example:
```python
class Trench2DGeom:
class JobStatus(Enum):
```

### 4.3 Constants
- Use **UPPER_CASE**

Example:
```python
PSI4_BASISSETS = [...]
DEFAULT_METHOD = "DFT"
```

### 4.4 Temporary File/Path Variables
- Use `f` prefix for file paths
- Use `_dir` suffix for directories

Example:
```python
fmol2: str  # mol2 file path
ftopol: Path  # top file path
cache_dir: Path  # cache directory
tmpl_dir: Path  # template directory
```

---

## 5. Code Style Guidelines

### 5.1 Assertion Checks
- **Use `assert` at the beginning of functions for parameter validation**
- Check types and necessary conditions first

Example:
```python
def process(atoms: Atoms, charge: int):
    assert isinstance(atoms, Atoms)
    assert isinstance(charge, int)
    assert charge >= 0
```

### 5.2 Conditional Expressions
- Use chained `if-elif-else` for multiple branches
- Use dictionary mapping for complex conditions

Example:
```python
# Chained conditions
if axis == 'x':
    pos[:, 1], pos[:, 2] = pos[:, 2], -pos[:, 1]
elif axis == 'y':
    pos[:, 0], pos[:, 2] = pos[:, 2], -pos[:, 0]
elif axis == 'z':
    pos[:, 0], pos[:, 1] = pos[:, 1], -pos[:, 0]

# Dictionary mapping
choices = {
    'psi4': ['DFT', 'HF'],
    'gaussian': ['DFT', 'MP2'],
}[software]
```

### 5.3 Unpacking and Multiple Assignment
- Use Python's unpacking features to simplify code

Example:
```python
xlo, xhi = np.min(pos[:, 0]), np.max(pos[:, 0])
a, b, c = cellpar[:3]
```

### 5.4 List Comprehensions
- Prefer list comprehensions over loops

Example:
```python
elem = [re.match(r'([A-Z][a-z]?)', a[1]).group(1) for a in atoms]
resname = ['UNK' for _ in atoms]
```

### 5.5 Line Length
- **Follow PEP 8 guidelines**: Maximum 79 characters per line for code
- **Docstrings and comments**: Maximum 72 characters per line
- **Breaking long lines**: Use parentheses for implicit line continuation
- **Avoid backslashes** for line continuation

Example:
```python
# Good: Implicit line continuation with parentheses
status = (
    JobStatus.SUCCESS
    if slurm_status == 'COMPLETED'
    else JobStatus.FAIL
)

# Good: Breaking long SQL queries
cursor.execute(
    'SELECT exit_code, error_message, output_files '
    'FROM jobs WHERE id = ?',
    (job_id,)
)

# Good: Breaking function definitions
def _mark_job_complete(
    self,
    job_id: int,
    status: JobStatus,
    exit_code: int = 0,
    error_message: str = None
):
    pass
```

---

## 6. Error Handling Guidelines

### 6.1 Exception Handling
- Use specific exception types
- Provide meaningful error messages

Example:
```python
try:
    methods = _get_available_method(software, theory)
except KeyError as e:
    gr.Warning(f'Invalid method for {software}/{theory}: {e}')
    return gr.update()
```

### 6.2 Assertion Messages
- Provide clear error messages when assertions fail

Example:
```python
assert i < j, f'failed to find the ATOM block in {fmol2}'
assert all(t.exists() for t in topologies)
```

---

## 7. File and Temporary Resource Management

### 7.1 Context Managers
- **Always use `with` statements for file management**
- Properly clean up temporary files

Example:
```python
with tempfile.NamedTemporaryFile(suffix='.pdb', delete=False) as fmerged:
    fmerged_path = fmerged.name
    # ... use the file
# Clean up temporary file
Path(fmerged_path).unlink(missing_ok=True)
```

### 7.2 Path Handling
- Use `pathlib.Path` instead of string concatenation
- Use `.as_posix()` to convert to POSIX paths (for command line)

Example:
```python
fpkml = Path('/path/to/file')
subprocess.run(['cmd', fpkml.as_posix()])
```

---

## 8. Testing Guidelines

### 8.1 Test Framework
- Use `unittest` for unit tests
- Use `pytest` for integration tests

Example:
```python
import unittest
import pytest
```

PLEASE ALWAYS ADD TESTS FOR YOUR CODE, to either ensure the proper functionality, catch bugs, verify the performance, and avoid the accidental breaking of existing features, or broken by new features.

### 8.2 Unit Tests
- Use `unittest` framework
- Test classes start with `Test`
- Test methods start with `test_`

Example:
```python
class TestQM(unittest.TestCase):
    def test_get_available_method(self):
        method = _get_available_method('psi4', 'DFT')
        self.assertListEqual(method, ['B3LYP', 'PBE'])

if __name__ == '__main__':
    unittest.main()
```

### 8.3 Integration Tests
- All integration tests must be placed in a separate file and in the folder `tests`
- Test files start with `test_`
- Test the interaction between different components
- Use `pytest` for integration tests

Example:
```python
def test_integration():
    # ... test code
    assert result == expected
```

---

## 9. UI Component Guidelines (Gradio)

### 9.1 Component Construction Pattern
- Use `build_*` functions to create components
- Use `connect_*` functions to define behavior
- Component dictionaries as `inout` parameters

Example:
```python
def build_molecule_builder(components: Dict[str, gr.Component]):
    components.update({
        'smiles': smiles,
        'create': create,
    })
    return builder

def connect_molecule_builder(components: Dict[str, gr.Component]):
    components['create'].click(fn=_on_create_click, ...)
```

### 9.2 Event Handler Functions
- Use `_on_*_change` or `_on_*_click` naming convention
- Return `gr.update()` to update component states

---

## 10. Additional Best Practices

### 10.1 Comment Guidelines
- Use English for comments
- Explain "why" not "what"
- Complex algorithms need detailed explanations

### 10.2 Magic Numbers
- Avoid magic numbers, use named constants

### 10.3 Function Length
- Single responsibility principle
- Split long functions into multiple smaller functions

---

## Quick Check Checklist

- [ ] File starts with docstring
- [ ] All functions have type annotations
- [ ] All functions have docstrings (Parameters + Returns)
- [ ] Use `assert` to validate parameters
- [ ] Use `with` for file management
- [ ] Use `pathlib.Path` for path handling
- [ ] Naming follows snake_case / PascalCase
- [ ] Core functionality covered by unit tests
- [ ] Temporary files properly cleaned up

---

These guidelines are derived from the existing codebase style. Following them ensures code consistency and maintainability.
