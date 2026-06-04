import asyncio
import random
import concurrent.futures
from interop import call_native_validator

MAX_BOUNDARY = 100.0
MIN_BOUNDARY = -100.0

def validate_single_seed(seed: int) -> str | None:
    random.seed(seed)
    vertex_bounds = [random.uniform(-110.0, 110.0) for _ in range(5)]
    
    for val in vertex_bounds:
        if val > MAX_BOUNDARY or val < MIN_BOUNDARY:
            return f"[Seed {seed}] Guardrail Violation: Value {val:.2f} out of bounds."
            
    is_native_valid = call_native_validator(vertex_bounds)
    if not is_native_valid:
        return f"[Seed {seed}] Native Runtime Memory Corruption Detected."
        
    return None

async def run_parallel_validation(total_tasks: int):
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