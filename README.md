# Obstructive Classes in Symplectic Embeddings
Code for enumerating possible obstuctions to symplectic embeddings

This repository contains code to accompany the paper "Symplectic Embeddings of Four-Dimensional Ellipsoids into Almost-Cubic Polydiscs", by Cory Colbert and Andrew Lee. The file `tails.py` contains code which searches for candidate solutions  $(d,e;m_1,\dots)$ to the Diophantine system

$$ \sum_i m_i = 2(d+e)-1$$

$$ \sum_i m_i^2 = 2de+1$$

for fixed values of $d,e$. The other accompanying .py files sift through the candidate solutions to find those which satisfy the Diophantine solution above, along with other necessary conditions.

Also included are `.slurm` scripts used to automate the process of running many searches in parallel and identifying only those candidates which are relevant to the problem.

This work used the NCSA Delta CPU at the University of Illinois Urbana-Champaign through allocation MTH230018 from the Advanced Cyberinfrastructure Coordination Ecosystem: Services & Support (ACCESS) program, which is supported by National Science Foundation grants #2138259, #2138286, #2138307, #2137603, and #2138296.
