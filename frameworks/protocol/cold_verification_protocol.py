"""
Cold Verification Protocol Framework
Used by Claude Opus 5 for mathematical proof verification in AI Village.

The cold verification protocol establishes rigorous verification standards:
1. Independent agent execution
2. SHA256 checksum matching
3. Exact check count verification (0 failures)
4. Comprehensive timing and result reporting
"""

import hashlib
import subprocess
import json
import datetime
import tempfile
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class ColdVerificationResult:
    """Results from cold verification protocol"""
    verification_id: str
    verification_timestamp: str
    command_executed: str
    sha256_expected: str
    sha256_actual: str
    checks_expected: int
    checks_executed: int
    checks_passed: int
    checks_failed: int
    execution_time_real: float  # seconds
    execution_time_user: float  # seconds
    verification_passed: bool
    findings_summary: str
    output_directory: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "verification_id": self.verification_id,
            "verification_timestamp": self.verification_timestamp,
            "command_executed": self.command_executed,
            "sha256_match": self.sha256_expected == self.sha256_actual,
            "sha256_expected": self.sha256_expected,
            "sha256_actual": self.sha256_actual,
            "checks_expected": self.checks_expected,
            "checks_executed": self.checks_executed,
            "checks_passed": self.checks_passed,
            "checks_failed": self.checks_failed,
            "execution_time_real": self.execution_time_real,
            "execution_time_user": self.execution_time_user,
            "verification_passed": self.verification_passed,
            "findings_summary": self.findings_summary,
            "output_directory": self.output_directory
        }

class ColdVerificationProtocol:
    """Implements the cold verification protocol"""
    
    def __init__(self, protocol_version: str = "v1.0"):
        """Initialize protocol with version"""
        self.protocol_version = protocol_version
        self.verification_seed = f"cold-verification-{protocol_version}"
    
    def execute_cold_verification(self,
                                repository_url: str,
                                verification_script: str,
                                expected_sha256: str,
                                expected_checks: int,
                                clone_directory: Optional[str] = None) -> ColdVerificationResult:
        """
        Execute cold verification protocol:
        1. Clone repository fresh
        2. Verify SHA256 of script
        3. Execute verification
        4. Compare results against expectations
        
        Args:
            repository_url: Git repository URL to clone
            verification_script: Path to verification script within repository
            expected_sha256: Expected SHA256 checksum of script
            expected_checks: Expected number of checks to execute
            clone_directory: Optional directory to clone into (temp if None)
            
        Returns:
            ColdVerificationResult with verification details
        """
        verification_id = self._generate_verification_id()
        timestamp = datetime.datetime.utcnow().isoformat()
        
        # Setup working directory
        if clone_directory is None:
            work_dir = tempfile.mkdtemp(prefix=f"cold_verify_{verification_id}_")
        else:
            work_dir = clone_directory
            os.makedirs(work_dir, exist_ok=True)
        
        Path(work_dir).mkdir(parents=True, exist_ok=True)
        
        # Step 1: Fresh clone
        clone_command = f"cd {work_dir} && git clone {repository_url} repo"
        clone_result = self._execute_command(clone_command, work_dir)
        
        if clone_result.returncode != 0:
            return self._create_failed_result(
                verification_id, timestamp,
                f"Clone failed: {clone_result.stderr[:200]}",
                work_dir
            )
        
        repo_path = os.path.join(work_dir, "repo")
        script_path = os.path.join(repo_path, verification_script)
        
        # Step 2: Verify SHA256
        actual_sha256 = self._calculate_file_sha256(script_path)
        
        if actual_sha256 != expected_sha256:
            return self._create_failed_result(
                verification_id, timestamp,
                f"SHA256 mismatch: expected {expected_sha256[:16]}..., got {actual_sha256[:16]}...",
                work_dir
            )
        
        # Step 3: Execute verification with timing
        verification_command = f"cd {repo_path} && time python3 {verification_script}"
        start_time = datetime.datetime.now()
        
        verification_result = self._execute_command(verification_command, repo_path)
        
        end_time = datetime.datetime.now()
        execution_time_real = (end_time - start_time).total_seconds()
        
        # Parse timing from output (time command output)
        execution_time_user = self._parse_execution_time(verification_result.stdout)
        
        # Step 4: Parse verification results
        checks_executed, checks_passed, checks_failed = self._parse_verification_output(
            verification_result.stdout
        )
        
        # Step 5: Verify against expectations
        verification_passed = (
            actual_sha256 == expected_sha256 and
            checks_failed == 0 and
            checks_executed == expected_checks and
            checks_passed == expected_checks
        )
        
        # Step 6: Generate findings summary
        findings_summary = self._generate_findings_summary(
            verification_result.stdout,
            verification_passed,
            checks_failed,
            checks_executed,
            expected_checks
        )
        
        # Create final command string for reporting
        command_executed = f"cd /tmp && git clone {repository_url} repo && cd repo && sha256sum {verification_script} && time python3 {verification_script}"
        
        return ColdVerificationResult(
            verification_id=verification_id,
            verification_timestamp=timestamp,
            command_executed=command_executed,
            sha256_expected=expected_sha256,
            sha256_actual=actual_sha256,
            checks_expected=expected_checks,
            checks_executed=checks_executed,
            checks_passed=checks_passed,
            checks_failed=checks_failed,
            execution_time_real=execution_time_real,
            execution_time_user=execution_time_user,
            verification_passed=verification_passed,
            findings_summary=findings_summary,
            output_directory=work_dir
        )
    
    def _execute_command(self, command: str, cwd: str) -> subprocess.CompletedProcess:
        """Execute shell command and return result"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            return result
        except subprocess.TimeoutExpired:
            return subprocess.CompletedProcess(
                args=command,
                returncode=124,
                stdout="",
                stderr="Command timed out after 300 seconds"
            )
    
    def _calculate_file_sha256(self, filepath: str) -> str:
        """Calculate SHA256 checksum of file"""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def _parse_execution_time(self, output: str) -> float:
        """Parse user time from time command output"""
        import re
        
        # Look for time command output patterns
        time_patterns = [
            r"user\s+(\d+m\d+\.\d+s)",  # time command format
            r"real\s*\d+m\d+\.\d+s.*user\s+(\d+m\d+\.\d+s)",
            r"CPU\s+(\d+\.\d+)s"  # Alternative format
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, output)
            if match:
                time_str = match.group(1)
                # Parse m:ss.ff format
                if 'm' in time_str:
                    minutes, seconds = time_str.split('m')
                    seconds = seconds.replace('s', '')
                    return float(minutes) * 60 + float(seconds)
                else:
                    return float(time_str.replace('s', ''))
        
        return 0.0  # Default if not found
    
    def _parse_verification_output(self, output: str) -> Tuple[int, int, int]:
        """Parse verification results from output"""
        import re
        
        # Look for common verification output patterns
        check_patterns = [
            r"(\d+)\s+checks?\s+run",
            r"(\d+)\s+passed,\s+(\d+)\s+failed",
            r"Tests:\s+(\d+)\s+passed,\s+(\d+)\s+failed",
            r"(\d+)\s+/\s+(\d+)\s+tests\s+passed"
        ]
        
        checks_executed = 0
        checks_passed = 0
        checks_failed = 0
        
        for pattern in check_patterns:
            matches = re.findall(pattern, output)
            for match in matches:
                if isinstance(match, tuple):
                    if len(match) == 1:
                        checks_executed = int(match[0])
                    elif len(match) == 2:
                        checks_passed = int(match[0])
                        checks_failed = int(match[1])
                        checks_executed = checks_passed + checks_failed
        
        # Fallback: count "PASSED" and "FAILED" lines
        if checks_executed == 0:
            checks_passed = output.count("PASSED") + output.count("passed") + output.count("OK")
            checks_failed = output.count("FAILED") + output.count("failed") + output.count("ERROR")
            checks_executed = checks_passed + checks_failed
        
        return checks_executed, checks_passed, checks_failed
    
    def _generate_findings_summary(self,
                                 output: str,
                                 verification_passed: bool,
                                 checks_failed: int,
                                 checks_executed: int,
                                 expected_checks: int) -> str:
        """Generate human-readable findings summary"""
        if verification_passed:
            return f"Verification successful: {checks_executed}/{expected_checks} checks passed, 0 failed"
        
        summary_parts = []
        
        if checks_failed > 0:
            summary_parts.append(f"{checks_failed} check(s) failed")
        
        if checks_executed != expected_checks:
            summary_parts.append(f"Checks executed ({checks_executed}) ≠ expected ({expected_checks})")
        
        # Extract key findings from output
        lines = output.split('\n')
        key_lines = [line for line in lines if any(
            keyword in line.lower() for keyword in 
            ['disproof', 'counterexample', 'failed', 'error', 'incorrect']
        )][:3]
        
        if key_lines:
            summary_parts.append("Key findings: " + "; ".join(key_lines))
        
        return "; ".join(summary_parts) if summary_parts else "Verification failed (no details extracted)"
    
    def _generate_verification_id(self) -> str:
        """Generate unique verification ID"""
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        random_part = hashlib.md5(str(datetime.datetime.utcnow().timestamp()).encode()).hexdigest()[:8]
        return f"cold_verify_{timestamp}_{random_part}"
    
    def _create_failed_result(self,
                            verification_id: str,
                            timestamp: str,
                            failure_reason: str,
                            work_dir: str) -> ColdVerificationResult:
        """Create result for failed verification"""
        return ColdVerificationResult(
            verification_id=verification_id,
            verification_timestamp=timestamp,
            command_executed="",
            sha256_expected="",
            sha256_actual="",
            checks_expected=0,
            checks_executed=0,
            checks_passed=0,
            checks_failed=1,
            execution_time_real=0.0,
            execution_time_user=0.0,
            verification_passed=False,
            findings_summary=f"Verification failed: {failure_reason}",
            output_directory=work_dir
        )
    
    def generate_protocol_report(self, result: ColdVerificationResult) -> Dict:
        """Generate comprehensive protocol report"""
        return {
            "protocol": {
                "name": "Cold Verification Protocol",
                "version": self.protocol_version,
                "origin": "AI Village collaboration with Claude Opus 5 (mathematical proof verification)",
                "standards": [
                    "Independent agent execution",
                    "SHA256 checksum matching",
                    "Exact check count verification (0 failures required)",
                    "Comprehensive timing reporting"
                ]
            },
            "verification_summary": {
                "status": "PASSED" if result.verification_passed else "FAILED",
                "verification_id": result.verification_id,
                "timestamp": result.verification_timestamp,
                "sha256_match": result.sha256_expected == result.sha256_actual,
                "checks_passed": f"{result.checks_passed}/{result.checks_expected}",
                "execution_time": f"{result.execution_time_real:.1f}s real, {result.execution_time_user:.1f}s user"
            },
            "technical_details": result.to_dict(),
            "integration_points": {
                "ci_cd": "Can be integrated as CI/CD verification stage",
                "quality_gate": "Can serve as quality gate for publication",
                "reproducibility": "Enables exact reproducibility of verification"
            },
            "recommended_practices": [
                "Always provide exact SHA256 checksums for verification scripts",
                "Specify exact expected check counts",
                "Use fresh clones to avoid state contamination",
                "Report both real and user time for performance benchmarking"
            ]
        }

# Example based on actual AGX thesis verification with Claude Opus 5
def example_agx_thesis_verification():
    """Example based on actual AGX thesis A.350/A.352 verification with Claude Opus 5"""
    protocol = ColdVerificationProtocol()
    
    # Simulate AGX thesis verification parameters
    result = protocol.execute_cold_verification(
        repository_url="https://gitlab.com/ai-village-agents/village/graffiti-verification.git",
        verification_script="verify/verify_agx_thesis_A350.py",
        expected_sha256="51d08d42c89b9d497c1d446fcb663e76844e558996dfd5b5bcc1aa718e6bab70",
        expected_checks=121
    )
    
    report = protocol.generate_protocol_report(result)
    
    print(f"Cold Verification Protocol - Example AGX Thesis Verification:")
    print(f"  Verification ID: {result.verification_id}")
    print(f"  Status: {'PASSED' if result.verification_passed else 'FAILED'}")
    print(f"  SHA256 Match: {result.sha256_expected == result.sha256_actual}")
    print(f"  Checks: {result.checks_passed}/{result.checks_expected} passed")
    print(f"  Time: {result.execution_time_real:.1f}s real, {result.execution_time_user:.1f}s user")
    print(f"  Findings: {result.findings_summary[:100]}...")
    
    return result, report

if __name__ == "__main__":
    # Run example verification (simulated - won't actually clone/execute)
    print("Note: This is a simulation of the cold verification protocol.")
    print("Actual execution requires network access and appropriate permissions.")
    
    # Create simulated result for demonstration
    protocol = ColdVerificationProtocol()
    result = ColdVerificationResult(
        verification_id="cold_verify_20261006_143000_abc123de",
        verification_timestamp="2026-10-06T14:30:00Z",
        command_executed="cd /tmp && git clone https://gitlab.com/... && cd repo && sha256sum verify/verify_agx_thesis_A350.py && time python3 verify/verify_agx_thesis_A350.py",
        sha256_expected="51d08d42c89b9d497c1d446fcb663e76844e558996dfd5b5bcc1aa718e6bab70",
        sha256_actual="51d08d42c89b9d497c1d446fcb663e76844e558996dfd5b5bcc1aa718e6bab70",
        checks_expected=121,
        checks_executed=121,
        checks_passed=121,
        checks_failed=0,
        execution_time_real=32.5,
        execution_time_user=20.2,
        verification_passed=True,
        findings_summary="Verification successful: 121/121 checks passed, 0 failed; A.352 false at every even n≥4 (exceeds by exactly 1/8), A.350 sharp, cycle Cₙ omitted from caption",
        output_directory="/tmp/cold_verify_20261006_143000_abc123de"
    )
    
    report = protocol.generate_protocol_report(result)
    print("\nExample Report:")
    print(json.dumps(report, indent=2))
