# Non-Deterministic Pipeline Validator (POC)

A high-performance, asynchronous test automation and validation framework designed for next-generation, AI-driven creative tools and procedural content pipelines. This Proof of Concept (POC) demonstrates how to transform volatile, non-deterministic outputs into reliable, metric-driven telemetry using a Python-orchestrated distributed dispatch architecture and a low-level C++ memory/data integrity verification layer.

## Project Objective

In modern gaming architectures, integrating generative AI and procedural systems introduces a paradigm shift. QA engineering must move away from rigid binary assertions ("Expected vs. Actual") and adapt to **non-deterministic validation, statistical boundaries, and massive data pipelines**.

This project provides a reference architecture for:
1. **Shift-Left Quality Engineering:** Catching algorithmic drifts, boundary violations, and runtime memory anomalies early in the CI/CD phase.
2. **Distributed Dispatch & Task Routing:** Maximizing hardware efficiency by dynamically scheduling heavy validation workloads across distributed nodes using Python's asynchronous event loops and multi-processing pools.
3. **Cross-Environment Interoperability:** Bridging the gap between high-level AI research pipelines (Python) and low-level AAA runtime game engines (C++).

---

## Key Technical Features

### 1. Asynchronous Task Routing (`dispatcher.py`)
Utilizes Python’s `asyncio` coupled with `concurrent.futures.ProcessPoolExecutor` to model a high-throughput distributed dispatch system. It maps validation tasks to available CPU/GPU hardware boundaries dynamically, minimizing execution bottlenecks during large-scale stress tests.

### 2. Property-Based Statistical Guardrails (`evaluator.py`)
Instead of tracking static values, the framework evaluates the output dataset against predefined mathematical and spatial bounds (e.g., vertex boundary constraints or confidence intervals), flagging non-deterministic output anomalies.

### 3. Low-Level C++ Interoperability (`memory_analyzer.cpp`)
Simulates the boundary limits of a core game engine runtime. By exposing a native C-style interface via `extern "C"`, Python pipes raw data buffers directly into compiled C++ memory layers to track floating-point exceptions (`NaN`), data corruption, and alignment drifts before code integration.

---

## 📂 Repository Structure

```text
📂 NonDeterministic-Pipeline-Validator
 ┣ 📂 src
 ┃ ┣ 📂 validator_core           # Python Architecture
 ┃ ┃ ┣ 📜 dispatcher.py          # Async engine, worker management, and orchestration
 ┃ ┃ ┗ 📜 interop.py             # Ctypes mapping layer to native binary
 ┃ ┗ 📂 native_interop           # C++ Core Subsystem
 ┃ ┃ ┣ 📜 memory_analyzer.cpp    # Raw buffer verification & alignment auditing
 ┃ ┃ ┗ 📜 CMakeLists.txt         # Cross-platform build configuration
 ┣ 📜 README.md                  # Technical specification profile
 ┗ 📜 requirements.txt           # Framework dependencies
```

---

## Getting Started

### Prerequisites
* Python 3.10+
* CMake 3.15+
* C++17 compatible compiler (MSVC, GCC, or Clang)

### 1. Build the Native C++ Subsystem
```bash
cd src/native_interop
mkdir build && cd build
cmake ..
cmake --build . --config Release
```
*Note: Ensure the compiled `.dll` (Windows) or `.so` (Linux) artifact is placed within the path recognized by `interop.py`.*

### 2. Initialize Python Environment & Execute
```bash
# Clone and install dependencies
pip install -r requirements.txt

# Run the parallel distributed pipeline simulation
python src/validator_core/dispatcher.py
```

## Scalability and Enterprise Production Impact

* **Reduced Manual Review Overhead:** Automated heuristic testing converts subjective visual/data verification into systematic, continuous integration data points, targeting a **60%+ reduction** in verification cycles.
* **Deterministic Isolation of Volatile Defects:** By running differential data seed streams across Python and C++ environments simultaneously, edge-case model drift is detected prior to deployment into live game production code.
* **Accelerated Research-to-Production Cycles:** Real-time telemetry reporting bridges communication between AI researchers and tools engineering, supporting faster iteration on next-generation features.