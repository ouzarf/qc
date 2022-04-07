## Welcome to my Quantum Computing Repo

The various scripts (mostly as Jupyter notebooks) are example scripts
designed as an introduction to Quantum Computing using Qiskit.

Many of the codes are copies or minor adaptations of the example codes
provided in the IBM Q Experience FAQ which is no longer available.

If you have any questions or comments, please email me at:
*stephen_j_jeffrey@yahoo.com.au*

### Tools

|  File/Notebook | Content                                                   |
|----------------|-----------------------------------------------------------|
|notebook_tools.py | Tools that enable functions defined inside notebooks to be imported like any other Python module. These tools were taken from the Jupyter documentation |
| importing_jupyter_functions_part_1.ipynb | Test function defined inside a notebook|
| importing_jupyter_functions_part_2.ipynb | Notebook that imports the test function defined in Part 1|
| tools.py | General tools |
| backend_tools.py | Tools for managing IBM Q Experience devices |

## Qiskit codes (see the Notebooks directory)
|  File/Notebook | Content                                                   |
|----------------|-----------------------------------------------------------|
| classification_using_quantum_SVM_kernel_method.ipynb | Extended discussion of a quantum Support Vector Machine
(please see the LaTeX sub-directory for a PDF copy)|
| transpilation.ipynb | Overview of the transpilation process from gates to pulse schedules

## Deprecated
Please note these are basic tutorials written using early versions of Qiskit, so they
may not run using the current version of Qiskit.

|  File/Notebook | Content                                                   |
|----------------|-----------------------------------------------------------|
| basic_gates_and_measurement.ipynb | Basis gates and measurements along various axes|
| advanced_gates.ipynb | More advanced gates, such as phase rotations        |
| basic_entanglement.ipynb | Simple entangle examples                       |
| state_tomography.ipynb | Measuring a qubit and plotting on the Bloch sphere|
| decoherence-dephasing_echo.ipynb | Measures the T2 dephasing time (echo experiment) on a real device                                     |
| decoherence-dephasing_Ramsey.ipynb | Measures the T2star dephasing time (Ramsey experiment) on a real device                                   |
| decoherence-energy_relaxation.ipynb | Measures the T1 decoherence time on a real device |
| decoherence-simulated.ipynb | Suite of decoherence experiments using the simulator and the decoherence tools in Qiskit Ignis. This script was adapted from the [Qiskit tutorial code](https://github.com/Qiskit/qiskit-tutorials/blob/master/qiskit/ignis/relaxation_and_decoherence.ipynb) |
| decoherence-simulated-with-visualisation.ipynb | Suite of decoherence experiments using the simulator with the result displayed on the Bloch sphere|



