import streamlit as st
import cirq
import sympy as sp
from PIL import Image

# Set page title and icon
img = Image.open("logo192.png")

st.set_page_config(page_icon=img, layout="wide")

# Function to generate a Grover iteration circuit
def grover_iteration(qubits):
    circuit = cirq.Circuit()
    if len(qubits) >= 2:
        circuit.append(cirq.H(q) for q in qubits)
        # Apply X gate to flip the target qubit (optional)
        circuit.append(cirq.X(qubits[-1]))
        circuit.append(cirq.CZ(qubits[0], qubits[1]))
        circuit.append(cirq.X(qubits[-1]))
        circuit.append(cirq.H(q) for q in qubits)
        circuit.append(cirq.measure(*qubits, key='result'))  # Measurement
    else:
        st.warning("Grover's algorithm requires at least two qubits.")
    return circuit

# Function to generate a VQE circuit
def vqe_circuit(qubits, hamiltonian, theta_values):
    circuits = []
    
    for theta in theta_values:
        circuit = cirq.Circuit()
        
        # Define ansatz circuit (Variational form)
        for qubit in qubits:
            circuit.append(cirq.H(qubit))  # Apply Hadamard gate to each qubit
            circuit.append(cirq.rx(theta).on(qubit))  # Apply X-rotation gate with parameter theta

        # Apply entangling gates (e.g., CNOT)
        for i in range(len(qubits) - 1):
            circuit.append(cirq.CNOT(qubits[i], qubits[i + 1]))  # Apply CNOT gate between neighboring qubits

        # Measure qubits to perform classical processing
        circuit.append(cirq.measure(*qubits, key='result'))
        
        circuits.append(circuit)

    return circuits


# Function to generate a QAOA circuit
def qaoa_circuit(qubits, mixer_hamiltonian, problem_hamiltonian, gamma_values, beta_values):
    circuit = cirq.Circuit()

    # Apply initial Hadamard gates
    circuit.append(cirq.H.on_each(*qubits))

    # Apply QAOA alternating layers
    for gamma, beta in zip(gamma_values, beta_values):
        # Apply problem Hamiltonian
        for term in problem_hamiltonian:
            gate = cirq.PauliString([cirq.X(q) if s == 'X' else cirq.Y(q) if s == 'Y' else cirq.Z(q) for q, s in zip(qubits, term)])
            circuit += gate ** (-gamma)

        # Apply mixer Hamiltonian
        for term in mixer_hamiltonian:
            gate = cirq.PauliString([cirq.X(q) if s == 'X' else cirq.Y(q) if s == 'Y' else cirq.Z(q) for q, s in zip(qubits, term)])
            circuit += gate ** beta

    # Measurement
    circuit.append(cirq.measure(*qubits, key='result'))
    
    return circuit


# Function to apply an energy transition gate
def apply_energy_transition(qubits):
    circuit = cirq.Circuit()
    if len(qubits) >= 2:
        circuit.append(cirq.X(qubits[0]))
        circuit.append(cirq.CNOT(qubits[0], qubits[1]))
        circuit.append(cirq.X(qubits[0]))
        circuit.append(cirq.measure(*qubits, key='result'))
    else:
        st.warning("Energy transition requires at least two qubits.")
    return circuit

# Function to apply a Hadamard gate to qubits
def apply_hadamard(qubits):
    circuit = cirq.Circuit()
    circuit.append(cirq.H(q) for q in qubits)
    circuit.append(cirq.measure(*qubits, key='result'))
    return circuit

# Function to apply Pauli gates to qubits
def apply_pauli_gate(qubits):
    circuit = cirq.Circuit()
    circuit.append(cirq.X(q) for q in qubits)
    circuit.append(cirq.Y(q) for q in qubits)
    circuit.append(cirq.Z(q) for q in qubits)
    circuit.append(cirq.measure(*qubits, key='result'))
    return circuit

# Function to apply a CNOT gate to qubits
def apply_cnot(qubits):
    circuit = cirq.Circuit()
    if len(qubits) >= 2:
        circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    else:
        st.warning("CNOT gate requires at least two qubits.")
    return circuit


def main():
    st.title('Quantum Circuit Generator')

    # Number of qubits selection
    num_qubits = st.slider('Number of Qubits:', min_value=1, max_value=10, value=2, step=1)

    # Algorithm selection
    algorithm = st.selectbox('Select Algorithm:', ['Grover', 'VQE', 'QAOA'])

    # Operation selection
    operation = st.selectbox('Select Operation:', ['Hadamard', 'Energy Transition', 'Pauli Gate', 'CNOT'])

    # Define qubits
    qubits = cirq.LineQubit.range(num_qubits)

    # Generate circuit based on user selections
    circuit = cirq.Circuit()
    if algorithm == 'Grover':
        circuit += grover_iteration(qubits)
    elif algorithm == 'VQE':
        vqe_hamiltonian = []
        for i in range(3):
            op = st.sidebar.selectbox(f'Select operation for qubit {i+1}:', ['X', 'Y', 'Z'])
            coeff = st.sidebar.number_input(f'Enter coefficient for qubit {i+1}:', value=0.0)
            vqe_hamiltonian.append((op, coeff))
        
        # Generate VQE circuit with a list of theta values
        theta_values = [0.1, 0.2, 0.3]  # Example values, you can change it as needed
        if st.sidebar.button("Run VQE"):
            circuit += vqe_circuit(qubits, vqe_hamiltonian, theta_values)
    elif algorithm == 'QAOA':
        st.sidebar.markdown('## QAOA Parameters')
        gamma_values = [st.sidebar.number_input(f'Enter gamma_{i+1}:', value=0.0) for i in range(num_qubits)]
        beta_values = [st.sidebar.number_input(f'Enter beta_{i+1}:', value=0.0) for i in range(num_qubits)]
        mixer_hamiltonian = []
        problem_hamiltonian = []
        if st.sidebar.button("Run QAOA"):
            circuit += qaoa_circuit(qubits, mixer_hamiltonian, problem_hamiltonian, gamma_values, beta_values)

    if operation == 'Hadamard':
        circuit += apply_hadamard(qubits)
    elif operation == 'Energy Transition':
        circuit += apply_energy_transition(qubits)
    elif operation == 'Pauli Gate':
        circuit += apply_pauli_gate(qubits)
    elif operation == 'CNOT':
        circuit += apply_cnot(qubits)

    # Display the generated circuit
    st.text('Generated Circuit:')
    st.text(circuit)

    # Visualize the steps of the circuit
    st.text('Circuit Diagram:')
    st.text(circuit.to_text_diagram(transpose=True))

    # Execute the circuit
    st.text('Simulation Results:')
    result = cirq.Simulator().simulate(circuit)
    st.text(result)

    # Display measurement results
    if 'result' in result.measurements:
        st.text('Measurement Results:')
        st.text(result.measurements['result'])
    else:
        st.text("No measurements performed.")

if __name__ == "__main__":
    main()
