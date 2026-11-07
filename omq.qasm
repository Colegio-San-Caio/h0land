OPENQASM 3;
include "stdgates.inc";
// OMQ = OR + Measurement + Qubit cat
gate omq a,b,c {
  h a;
  x b;
  ccx a,b,c;
}
qubit[3] q;
omq q[0], q[1], q[2];
