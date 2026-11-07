OPENQASM 3.0;
include "stdgates.inc";
gate ornop a,b,c {
  x a; x b; ccx a,b,c; x a; x b; x c; id c;
}
def main() {
  qubit[3] q; bit[3] c;
  h q[0]; cx q[0],q[1]; cx q[0],q[2];
  ornop q[0],q[1],q[2];
  c = measure q;
}
main();
