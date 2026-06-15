import asyncio
import random
import concurrent.futures
from interop import call_native_validator
from evaluator import StatisticalGuardrailEvaluator

guardrail_engine = StatisticalGuardrailEvaluator(
    min_bound=-100.0, 
    max_bound=100.0,
    expected_mean=0.0,
    std_dev_threshold=3.0
)

def validate_single_seed(seed: int) -> str | None:
    """
    Worker task executed across parallel process pool nodes.
    Generates non-deterministic data and validates it against statistical
    and native memory subsystems.
    """
    random.seed(seed)
    vertex_bounds = [random.uniform(-110.0, 110.0) for _ in range(5)]
    
    audit_report = guardrail_engine.run_full_pipeline_audit(vertex_bounds)
    
    if not audit_report["audit_passed"]:
        if audit_report["spatial_anomalies"]:
            return f"[Seed {seed}] {audit_report['spatial_anomalies'][0]}"
        return f"[Seed {seed}] Guardrail Violation: Distribution variance drift anomaly detected."
            
    is_native_valid = call_native_validator(vertex_bounds)
    if not is_native_valid:
        return f"[Seed {seed}] Native Runtime Memory Corruption Detected."
        
    return None

async def run_parallel_validation(total_tasks: int):
    """
    Orchestration engine managing asynchronous task scheduling across 
    multi-core CPU processing nodes.
    """
    print(f"--- Starting Distributed Task Routing for {total_tasks} Tasks ---")
    
    loop = asyncio.get_running_loop()
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        tasks = [
            loop.run_in_executor(executor, validate_single_seed, seed)
            for seed in range(total_tasks)
        ]
        
        results = await asyncio.gather(*tasks)
        
    errors = [res for res in results if res is not None]
    
    print(f"\n--- Validation Completed. Failures Detected: {len(errors)}/{total_tasks} ---")
    for err in errors:
        print(f"\033[91m{err}\033[0m")

if __name__ == "__main__":
    asyncio.run(run_parallel_validation(total_tasks=100))