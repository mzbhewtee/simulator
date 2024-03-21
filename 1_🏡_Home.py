import streamlit as st
from PIL import Image

# Set page title and icon
img = Image.open("logo192.png")

st.set_page_config(page_title="Simulator", page_icon=img, layout="wide")

def show_information():
    st.title("Introduction to Quantum Simulation")

    st.header("What is Quantum Simulation?")
    st.write("""
    Quantum simulation involves using a quantum computer or simulator to model and analyze quantum systems. 
    It allows researchers to explore the behavior of quantum systems that may be too complex for classical computers to handle efficiently. 
    Quantum simulation has applications in various fields, including physics, chemistry, materials science (renewable energy material detection), and cryptography.
    """)

    st.header("Qubits: The Building Blocks of Quantum Computing")
    st.write("""
    Qubits (quantum bits) are the basic units of quantum information. 
    Unlike classical bits, which can be either 0 or 1, qubits can exist in a superposition of states, 
    allowing them to represent both 0 and 1 simultaneously. 
    This property enables quantum computers to perform complex calculations much faster than classical computers.
    """)
    st.image("qubits.jpg", caption="Qubits in a superposition of states", width=400)

    st.header("Quantum Algorithms")
    st.write("""
    Quantum algorithms are algorithms designed to run on quantum computers. 
    They take advantage of the unique properties of qubits, such as superposition and entanglement, 
    to solve certain problems more efficiently than classical algorithms. 
    Some well-known quantum algorithms include Grover's algorithm for searching unsorted databases and 
    Shor's algorithm for integer factorization, which can break classical cryptographic protocols.
    """)
    st.write("Common quantum algorithms include:")
    st.write("- Grover's algorithm: for searching unsorted databases in O(√N) time, where N is the number of items in the database")
    st.write("- Shor's algorithm: for integer factorization in polynomial time, breaking classical cryptographic protocols")
    st.write("- Quantum phase estimation: for estimating the eigenvalues of unitary operators")
    st.write("- Variational quantum eigensolver (VQE): for finding the ground state energy of a molecule" )
    st.write("- Quantum approximate optimization algorithm (QAOA): for solving combinatorial optimization problems")

    st.image("quantum_algorithms.jpg", caption="Quantum algorithms taking advantage of qubit properties", width=400)

    st.header("Quantum Operations")
    st.write("""
    Quantum operations are transformations applied to qubits to manipulate their states. 
    These operations include single-qubit gates, which act on individual qubits, and 
    multi-qubit gates, which act on pairs or groups of qubits. 
    Common quantum operations include the Hadamard gate, which creates superposition, 
    and the CNOT gate, which creates entanglement between qubits.
    """)
    st.write("Common quantum operations include:")
    st.write("- Hadamard gate: creates superposition by rotating the qubit state around the X+Z axis")
    st.write("- Pauli gates (X, Y, Z): perform rotations around the X, Y, and Z axes of the Bloch sphere")
    st.write("- CNOT gate: entangles two qubits by flipping the target qubit if the control qubit is |1>")
    st.write("- SWAP gate: swaps the states of two qubits")
    st.write("- Toffoli gate: a controlled-controlled-NOT gate that flips the target qubit if both control qubits are |1>")
    st.write("- Energy transition gate: simulates energy transitions in quantum systems")

    st.image("quantum_operations.jpg", caption="Common quantum operations", width=400)

if __name__ == "__main__":
    show_information()
