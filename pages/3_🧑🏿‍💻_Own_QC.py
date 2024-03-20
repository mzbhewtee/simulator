import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import cirq

from PIL import Image

# Set page title and icon
img = Image.open("logo192.png")

st.set_page_config(page_icon=img, layout="wide")

# Function to execute user-defined Python code
def execute_user_code(user_code):
    try:
        exec(user_code, globals())
        return result
    except Exception as e:
        st.error(f"An error occurred: {e}")

st.title("Quantum Simulation for Renewable Energy")
# Text area for user to input their own quantum circuit code in Python
st.header("Write Your Own Quantum Circuit in Python")

# Explanation of how to write the quantum circuit code
st.write("""
### Instructions:
1. Write your custom quantum circuit code in the Python syntax in the text area below.
2. Ensure that the result of your quantum circuit execution is assigned to the variable 'result'.
3. If your code requires plotting a graph, make sure to include the necessary code for plotting.
4. Click the 'Run Code' button to execute your quantum circuit.
5. You can also write an python code that you wish, just make sure you assign your result to the variable named 'result'.
""")

user_code = st.text_area("Write your Python quantum circuit code here:", """
# Example code:
# Create a custom quantum circuit with 2 qubits and apply a Hadamard gate on each qubit
circuit = cirq.Circuit()
qubits = cirq.LineQubit.range(2)
for qubit in qubits:
    circuit.append(cirq.H(qubit))
result = circuit
""", height=300)  # Specify the height of the text area

# Button to execute user-defined Python code
if st.button("Run Code"):
    result = execute_user_code(user_code)
    st.write("Result of User Code Execution:")
    st.text(result)

    # Check if the user's result requires plotting a graph
    if isinstance(result, cirq.Circuit):
        st.header("Simulation Results (Graph)")
        # Plot a random energy landscape for demonstration
        num_points = 100
        energies = np.random.rand(num_points)
        plt.plot(energies)
        plt.xlabel('Iterations')
        plt.ylabel('Energy')
        st.pyplot(plt)
