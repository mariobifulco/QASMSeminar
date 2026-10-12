# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "qiskit==2.5.2",
#   "matplotlib==3.11.2",
#   "pylatexenc==2.10",
# ]
# ///
"""Regenerate the teaching circuits with `uv run generate-circuits.py`."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


circuits = {
    "not": QuantumCircuit(1),
    "h": QuantumCircuit(1),
    "cnot": QuantumCircuit(2),
}
circuits["not"].x(0)
circuits["h"].h(0)
circuits["cnot"].cx(0, 1)

# Verify the gate behavior before exporting the diagrams.
assert Statevector.from_instruction(circuits["not"]).probabilities_dict() == {"1": 1.0}
assert all(
    abs(probability - 0.5) < 1e-12
    for probability in Statevector.from_instruction(circuits["h"]).probabilities()
)
for input_bits, output_bits in {"00": "00", "01": "11", "10": "10", "11": "01"}.items():
    output = Statevector.from_label(input_bits).evolve(circuits["cnot"])
    assert output.probabilities_dict() == {output_bits: 1.0}

image_dir = Path(__file__).resolve().parent / "img"
for name, circuit in circuits.items():
    figure = circuit.draw(
        output="mpl",
        fold=-1,
        style={
            "name": "iqp",
            "backgroundcolor": "#ffffff",
            "displaycolor": {
                "x": ("#002d9c", "#ffffff"),
                "h": ("#002d9c", "#ffffff"),
                "cx": ("#002d9c", "#ffffff"),
            },
        },
    )
    output_path = image_dir / f"{name}.png"
    figure.savefig(output_path, dpi=400, bbox_inches="tight", pad_inches=0.15)
    plt.close(figure)
    print(output_path)
