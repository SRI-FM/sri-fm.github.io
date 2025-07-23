# PVS - Specification and Proof Assistent

{{< details title="PVS" >}}

## Description
PVS is an interactive specification and proof assistant
 * Rich specification language based on simply-typed higher-order logic extended with predicate subtyping,
   logical theories, and theory interpretation
 * Interactive theorem prover combines automation based on rewriting, decision procedures (SMT),
   predicate abstraction, model-checking with interaction using powerful and robust proof commands that
   can be combined with  high-level proof strategies such as *grind*  and *induct-and-simplify*
 * Correct-by-construction generation of highly efficient, memory-safe, stand-alone C and Rust code for
   a full functional  fragment of PVS (PVS2C, PVS2RUST)
    
## Purpose
Primarily used for modeling mathematical and computational concepts, including program behavior.

## Use Cases
Microprocessors, separation kernels, cache-coherence protocols, real-time operating systems, distributed fault-tolerance, cryptographic protocols, air-traffic control algorithms, libraries for mathematics and computer science.

## Download
PVS is available under the [GPL v3](https://www.gnu.org/licenses/gpl-3.0.html) license from
    the [PVS website](https://pvs.csl.sri.com) and on the
   [PVS github](github.com/SRI-CSL/PVS).
   
Licenses for commercial usage or specific support are available upon request.

Note that the PVS2C and PVS2Rust extensions of PVS are not part of the publicly released PVS.

{{< /details >}}

# Yices - Decision Procedures

## Description
Powerful automated reasoning tool that determines the satisfiability of formulas in combinations of logical theories
   * Supports linear and nonlinear real and integer arithmetic, bitvectors, scalar types, tuples, extensional arrays, and uninterpreted function symbols with equality
   * Powerful first-order reasoning based on counterexample-guided quantifier instantiation and model interpolation
   * Processes SMT-LIB formulas and offers language bindings for C, Python, Java, Go, and OCaml
   
## Purpose
Robust formal verification backend for other applications that require reasoning about complex logical
constraints over various data types.

## Use Cases
Constraint Solving for Hardware Verification, Extended Type Checking, Program Analysis and Synthesis , Crypto Analysis, Artificial Intelligence, Interactive Proof Assistants, Spreadsheet Debugging.

## Download
The latest Yices2 is available under the [GPL v3](https://www.gnu.org/licenses/gpl-3.0.html) license from the
     [Yices website](yices.csl.sri.com) and on the
     [Yices2 Github](github.com/SRI-CSL/yices2).

Licenses for commercial usage or specific support are available upon request. 


# Sally - Model Checking

## Description
Sally is a model checker for the formal verification of infinite-state systems.
It is the successor to SRI’s earlier SAL (Symbolic Analysis Laboratory)
   * Takes as input a description of transition systems based on  SMT-LIB2, BTOR2, and MOXI, allowing for the definition of state types, initial states, and transition relations using first-order formulas
   * Implements property-directed k-induction, a variant of IC3/PDR, which is particularly effective for generating k-inductive strengthenings
   * Sally heavily relies on the [Yices2 solver](yices.csl.sri.co) for efficient constraint solving for bitvectors and nonlinear real and integer arithmetic

## Purpose
Robust formal verification backend for other applications that require reasoning about complex
logical constraints over various data type.s

## Use Cases
Software and Hardware Verification, Protocol Analysis, Fault-Tolerant Distributed Algorithms.

## Download
Sally is available at [Github](https://github.com/SRI-CSL/sally)  under the [GPL v3](https://www.gnu.org/licenses/gpl-3.0.html) GPL v3 license.

Licenses for commercial usage or specific support are available upon request.

Its predecessor can be downloaded from the [SAL Website](sal.csl.sri.com).



# Radler -  Multi-Rate Integration Architecture

## Description
Radler implements a formally grounded approach to designing, developing, and verifying distributed multi-rate cyber-physical systems,
ensuring robustness, safety, and performance in critical applications.
   * Multi-rate model of computation
   * Publish-subscribe communication architecture
   * Quasi-periodic execution
   * Bounded-latency channels

## Purpose
Radler provides strong architectural guarantees for safety, security, resilience, which are formally proven in PVS.
    * Certifiable to a range of assurance levels
    * Seamless integration with easy SW/HW-in-the-loop testing and debugging, and rapid prototyping.

## Use Cases
Critical cyber-physical systems including drones, robots, medical devices, SCADA, autonomous systems, and agentic AI.

## Download
Radler is available  from the [Radler github](https://github.com/SRI-CSL/radler)  under the 
[GPL v3](https://www.gnu.org/licenses/gpl-3.0.html) license.

Licenses for commercial usage or specific support are available upon request.

# ETB - Evidential Toolbus

## Description
Distributed framework for integrating various software systems analysis and verification tools.
Designed to facilitate the continuous creation and maintenance of assurance cases, automatically updating claims
and evidence as system requirements or components change.

## Purpose
The primary purpose of ETB is to significantly reduce the cost, labor, and *ad hoc* nature of developing and
maintaining assurance cases for critical systems. By automating the evidence generation and argument construction processes,
it aims to:
  * Provide *accountable evidence* that corroborates the safety and other critical properties of software.
  * Enable *continuous assurance* for complex systems, where traditional manual processes are unsustainable.
  * Improve *rigor and trustworthiness* of assurance cases by grounding them in formal logic and verifiable evidence.

## Use Cases
Automated Driving, Flight-Control Systems, Software System Certification, AI/ML Assurance, Continuous Authority to Operate,
Software Understanding.

## Download
The latest ETB2 is available from the [ETB2 github]  https://github.com/SRI-CSL/etb2  under the
[GPL v3](https://www.gnu.org/licenses/gpl-3.0.html) license.

Licenses for commercial usage or specific support are available upon request.

# Assurance 2.0 - Rigorous Assurance Cases

## Description
Modern approach to the development and assessment of assurance cases, which are structured arguments backed by evidence to demonstrate that a system possesses certain critical properties (e.g., safety, security).
[Assurance 2.0](https://arxiv.org/pdf/2409.10665) builds upon the established Claims, Arguments, Evidence methodology but introduces a higher degree of rigor and systematic evaluation:
  * Logical Soundness  of the decomposition of claims into subclaims
  * Identification, analysis, and refutation of potential defeaters (challenges or doubts) to the argument
  * Probabilistic assessment of residual risks
  * Confirmation theory:  does evidence support a claim?  how well does it discriminate against alternative claims?

## Purpose
Provide a robust framework for justified confidence in the deployment of complex, critical systems,
especially those incorporating new technologies like AI and autonomous capabilities, where traditional testing alone is insufficient.

## Use Cases
Certification of Safety-Critical Systems, Security Assurance, AI Assurance, Regulatory Compliance, Continuous and Incremental Assurance.

## Tool Support
The Assurance 2.0 methodology is usually implemented in industry-specific development frameworks, with 
[ETB](https://github.com/SRI-CSL/etb2) used for curating evidence in CI/CD pipelines. We have been cooperating
with Adelard (now part of [NCC group](https://www.nccgroup.com/) in developing *Clarissa*, which directly
supports Assurance 2.0.




# PCE - Probabilistic Consistency Engine

## Description
Probabilistic inference for  Markov Logic Networks, which combine first-order logic with Markov networks.
PCE relies on sampling-based methods such as Gibbs sampling to approximate marginal and conditional probabilities
and it uses maximum a posterior inference, allowing it to achieve scalability for larger problems.

## Purpose
Enable logical reasoning about systems where uncertainty and probabilities are inherent.
This is crucial for analyzing and verifying systems where components might fail with a certain probability,
or where decisions are based on uncertain inputs. It helps in modeling and analyzing probabilistic systems,
consistency checking of probabilistic statements, and probabilistic inference.

## Use Cases
Probabilistic program analysis, information extraction and integration, knowledge base construction, natural language processing, semantic parsing, social network analysis, computer vision, computational biology, robotics and autonomous systems, fraud detection, cybersecurity.

## Download.
PCE is available from the [PCE Github](https://github.com/SRI-CSL/pce) under the
[LGPL v3](https://www.gnu.org/licenses/lgpl-3.0.html) license.


