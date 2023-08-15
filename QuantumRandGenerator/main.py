from qiskit import QuantumCircuit, Aer
import argparse
from math import log2, ceil

def create_circuit(n):
    circuit = QuantumCircuit(n)
    for i in range(n):
        circuit.h(i)
    circuit.measure_all()
    return circuit

def get_results(cirq):
    simulator = Aer.get_backend("aer_simulator")
    job = simulator.run(cirq,shots=1024)
    results = job.result()
    counts = results.get_counts(cirq)
    return counts

def main():
    parser = argparse.ArgumentParser(description="Quantum Random Number Generator")
    parser.add_argument("-lo","--lower",action="store",nargs="+",required=True,type=int)
    parser.add_argument("-hi","--higher",action="store",nargs="+",required=True,type=int)

    args = parser.parse_args()
    circuit_result = get_results(create_circuit(ceil(log2(args.higher[0]))))
    circuit_result = {eval("0b"+k):v for (k,v) in circuit_result.items()} # convert keys to decimal
    circuit_result = dict((v,k)  for (k,v) in circuit_result.items() if (k >= args.lower[0] and k <= args.higher[0]))

    return max(circuit_result.items())[1]