#!/usr/bin/env python3
"""
JWT Token Generator

Creates a JWT token with custom header, payload, and secret.
Supports human-readable expiration date formats.
"""

import jwt
import json
from datetime import datetime


def parse_expiration(exp_input: str) -> int:
    """
    Parse human-readable expiration date into Unix timestamp.
    
    Supported formats:
    - "2026-12-31 23:59:59"
    - "2026-12-31"
    - "31/12/2026 23:59:59"
    - "31/12/2026"
    - Unix timestamp as string (e.g., "1770702900")
    """
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d",
    ]
    
    # Try parsing as Unix timestamp first
    try:
        return int(exp_input)
    except ValueError:
        pass
    
    # Try different date formats
    for fmt in formats:
        try:
            dt = datetime.strptime(exp_input, fmt)
            return int(dt.timestamp())
        except ValueError:
            continue
    
    raise ValueError(
        f"Could not parse expiration date: '{exp_input}'\n"
        f"Supported formats: YYYY-MM-DD HH:MM:SS, YYYY-MM-DD, DD/MM/YYYY, or Unix timestamp"
    )


def create_jwt(header: dict, payload: dict, secret: str) -> str:
    """Create a JWT token with the given header, payload, and secret."""
    return jwt.encode(
        payload,
        secret,
        algorithm=header.get("alg", "HS256"),
        headers={"typ": header.get("typ", "JWT")}
    )


def main():
    print("=" * 50)
    print("         JWT Token Generator")
    print("=" * 50)
    
    # Get algorithm
    print("\n[Header Configuration]")
    alg = input("Algorithm (default: HS256): ").strip() or "HS256"
    typ = input("Type (default: JWT): ").strip() or "JWT"
    
    header = {
        "alg": alg,
        "typ": typ
    }
    
    # Get payload
    print("\n[Payload Configuration]")
    broker = input("Broker name: ").strip()
    
    # IAT - default to current time
    iat_input = input("Issued At (iat) - press Enter for current time, or provide timestamp: ").strip()
    if iat_input:
        try:
            iat = int(iat_input)
        except ValueError:
            iat = int(parse_expiration(iat_input))
    else:
        iat = int(datetime.now().timestamp())
    
    # Expiration - human readable
    print("\nExpiration date formats: YYYY-MM-DD HH:MM:SS, YYYY-MM-DD, DD/MM/YYYY, or Unix timestamp")
    exp_input = input("Expiration (exp): ").strip()
    exp = parse_expiration(exp_input)
    
    payload = {
        "broker": broker,
        "iat": iat,
        "exp": exp
    }
    
    # Get secret
    print("\n[Secret]")
    secret = input("Enter your secret key: ").strip()
    
    if not secret:
        print("Error: Secret cannot be empty!")
        return
    
    # Generate JWT
    try:
        token = create_jwt(header, payload, secret)
        
        print("\n" + "=" * 50)
        print("         Generated JWT Token")
        print("=" * 50)
        print(f"\nHeader: {json.dumps(header, indent=2)}")
        print(f"\nPayload: {json.dumps(payload, indent=2)}")
        print(f"\nExpiration: {datetime.fromtimestamp(exp).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n🔑 JWT Token:\n{token}")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nError creating JWT: {e}")


if __name__ == "__main__":
    main()
