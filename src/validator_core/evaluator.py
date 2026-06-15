import numpy as np
import logging
from typing import List, Dict, Any, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StatisticalGuardrailEvaluator:
    """
    Evaluates non-deterministic datasets against mathematical, geometric,
    and statistical bounds to catch variance drift and spatial violations.
    """
    def __init__(self, 
                 min_bound: float = -100.0, 
                 max_bound: float = 100.0, 
                 expected_mean: float = 0.0, 
                 std_dev_threshold: float = 3.0):
        
        self.min_bound = min_bound
        self.max_bound = max_bound
        
        self.expected_mean = expected_mean
        self.std_dev_threshold = std_dev_threshold
        
        self.history_buffer: List[float] = []

    def verify_spatial_bounds(self, vertex_data: List[float]) -> Tuple[bool, List[str]]:
        """
        1. Geometric Boundary Constraints Check.
        Vectorized validation checking if vertices breach absolute physical constraints.
        """
        violations = []
        data_array = np.array(vertex_data)
        
        out_of_min = data_array < self.min_bound
        out_of_max = data_array > self.max_bound
        
        if np.any(out_of_min) or np.any(out_of_max):
            bad_indices = np.where(out_of_min | out_of_max)[0]
            for idx in bad_indices:
                val = vertex_data[idx]
                violations.append(
                    f"Spatial Constraint Breach: Vertex Index {idx} with Value {val:.2f} "
                    f"fell outside allowed [{self.min_bound}, {self.max_bound}] window."
                )
            return False, violations
            
        return True, []

    def evaluate_statistical_drift(self, batch_data: List[float]) -> Dict[str, Any]:
        """
        2. Statistical Variance Guardrails.
        Calculates dynamic statistical metrics to identify distribution anomalies
        and data degradation over time.
        """
        if not batch_data:
            return {"status": "SKIPPED", "reason": "Empty payload input matrix."}
            
        self.history_buffer.extend(batch_data)
        
        current_mean = float(np.mean(batch_data))
        current_std = float(np.std(batch_data)) if len(batch_data) > 1 else 0.0
        
        z_score = abs(current_mean - self.expected_mean) / (current_std if current_std > 0 else 1.0)
        drift_detected = z_score > self.std_dev_threshold
        
        evaluation_report = {
            "status": "FAIL" if drift_detected else "PASS",
            "metrics": {
                "batch_mean": round(current_mean, 4),
                "batch_std_dev": round(current_std, 4),
                "calculated_z_score": round(z_score, 4),
                "drift_anomaly_flag": drift_detected
            }
        }
        
        if drift_detected:
            logging.warning(f"Pipeline Drift Alert: Z-Score ({z_score:.2f}) "
                            f"breached standard deviation tolerance limit ({self.std_dev_threshold}).")
            
        return evaluation_report

    def run_full_pipeline_audit(self, payload: List[float]) -> Dict[str, Any]:
        """
        Orchestration Wrapper. Executes both spatial checks and statistical checks 
        on incoming data packets.
        """
        spatial_pass, spatial_errors = self.verify_spatial_bounds(payload)
        stats_report = self.evaluate_statistical_drift(payload)
        
        audit_passed = spatial_pass and (stats_report.get("status") == "PASS")
        
        return {
            "audit_passed": audit_passed,
            "spatial_anomalies": spatial_errors,
            "statistical_profile": stats_report
        }

if __name__ == "__main__":
    print("--- Executing Isolated Structural Test for StatisticalGuardrailEvaluator ---")
    evaluator = StatisticalGuardrailEvaluator()
    
    safe_mock_data = [12.5, -45.2, 88.0, 0.1, -9.9]
    safe_result = evaluator.run_full_pipeline_audit(safe_mock_data)
    print(f"Safe Payload Result Status Passed? -> {safe_result['audit_passed']}")
    
    corrupted_mock_data = [15.2, 105.7, -120.4, 3.3] # 105.7 and -120.4 are out of bounds
    fail_result = evaluator.run_full_pipeline_audit(corrupted_mock_data)
    print(f"Corrupted Payload Result Status Passed? -> {fail_result['audit_passed']}")
    print(f"Caught Spatial Anomalies: {fail_result['spatial_anomalies']}")
