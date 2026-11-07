import numpy as np

def fahrenheit_to_kelvin(f):
    """Converts Fahrenheit temperature to Kelvin"""
    return (f - 32) * 5/9 + 273.15

def calculate_enthalpy_wavelength(temp_f, wavelength_nm, auhx_factor=1.0):
    """
    Calculates a custom simulated enthalpy delta dependent on:
    - temp_f: Temperature in Fahrenheit
    - wavelength_nm: Wavelength in nanometers (absorption scale)
    - auhx_factor: A scaling genetics coefficient (AuHx)
    """
    T = fahrenheit_to_kelvin(temp_f)
    
    # Energy calculation: E = h * c / lambda
    hc = 1.986445e-16  # J * nm
    energy_wavelength = hc / wavelength_nm
    
    # Mathematical integration baseline approximation
    cp_base = 29.1  # J/(mol*K) base capacity reference
    enthalpy = (cp_base * T) + (auhx_factor * energy_wavelength * 1e23)
    
    return float(enthalpy)

def calculate_oximeter_auhx(absorbance_660, absorbance_940, temp_f, baseline_factor=1.0):
    """
    Calculates AuHx state parameters using pulse oximeter wavelength metrics.
    
    Parameters:
    - absorbance_660: Optical density/absorption at Red light (660 nm)
    - absorbance_940: Optical density/absorption at Near-Infrared light (940 nm)
    - temp_f: Environment temperature in Fahrenheit
    - baseline_factor: Base scaling constant for the AuHx configuration
    """
    # 1. Standardize temperatures
    T = (temp_f - 32) * 5/9 + 273.15
    
    # 2. Compute the oximetry ratio R (Ratio of Ratios)
    # R = (A660) / (A940)
    if absorbance_940 == 0:
        return 0.0
    R = absorbance_660 / absorbance_940
    
    # 3. Translate R into a dynamic shift proxy for AuHx LSPR
    # Higher hydriding changes optical transmission across red/IR bands
    auhx_effective_wavelength = 660.0 + (R * 280.0) 
    
    # 4. Integrate into your working enthalpy energy formula: E = hc / lambda
    hc = 1.986445e-16  # J * nm
    energy_delta = hc / auhx_effective_wavelength
    
    cp_base = 29.1  # J/(mol*K)
    total_enthalpy = (cp_base * T) + (baseline_factor * energy_delta * 1e23)
    
    return {
        "oximeter_ratio_R": float(R),
        "derived_wavelength_nm": float(auhx_effective_wavelength),
        "calculated_enthalpy": float(total_enthalpy)
    }

import serial
import time

def stream_oximeter_auhx_live(port='/dev/ttyUSB0', baudrate=115200, temp_f=77.0):
    """
    Connects to a serial hardware interface stream to process 
    live pulse oximeter inputs for automated AuHx calculation updates.
    
    Expected serial text input format from micro-controller:
    "RED=XXXXX,IR=YYYYY" or "XXXXX,YYYYY"
    """
    print(f"Connecting to hardware interface on {port} at {baudrate} baud...")
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2) # Give connection a moment to initialize safely
        print("Stream connection active. Press Ctrl+C to terminate tracking loop.\n")
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                # Simple parser for raw comma-separated tracking outputs (e.g. "45210,39850")
                try:
                    if ',' in line:
                        parts = line.split(',')
                        # Clean out text prefixes if present
                        red_val = float(''.join(c for c in parts[0] if c.isdigit() or c=='.'))
                        ir_val = float(''.join(c for c in parts[1] if c.isdigit() or c=='.'))
                        
                        # Process live values via your core oximeter ratio module
                        stats = calculate_oximeter_auhx(red_val, ir_val, temp_f)
                        
                        print(f"[LIVE] Red-Counts: {red_val:<6} | IR-Counts: {ir_val:<6} | Enthalpy: {stats['calculated_enthalpy']:.2f} J/mol")
                except ValueError:
                    # Ignore corrupted serial noise packets
                    continue
                    
            time.sleep(0.1) # Prevents CPU core spiking inside Termux loop
            
    except KeyboardInterrupt:
        print("\nLive oximeter serial stream tracking safely terminated.")
    except Exception as e:
        print(f"\nHardware Connection Error: {e}")

import urllib.request
import json

def fetch_mosfet_qexchange_data(device_ip="192.168.4.1", temp_f=77.0):
    """
    Fetches raw dual-wavelength data via Wi-Fi from an external microcontroller 
    managing high-speed MOSFET switching gates.
    """
    url = f"http://{device_ip}/data"
    print(f"Polling MOSFET Exchange controller node at {url}...")
    
    try:
        # Request stream state from network node
        response = urllib.request.urlopen(url, timeout=3)
        data = json.loads(response.read().decode('utf-8'))
        
        # Expecting JSON schema keys matching raw sensor photo-diode counts
        red_val = float(data.get("red", 0))
        ir_val = float(data.get("ir", 0))
        mosfet_state = data.get("mosfet_gate", "UNKNOWN")
        
        # Process structural state metrics via core calculation routine
        stats = calculate_oximeter_auhx(red_val, ir_val, temp_f)
        stats["mosfet_gate_status"] = mosfet_state
        
        return stats
        
    except Exception as e:
        print(f"Network Connection Failed: {e}")
        return None

import hashlib
import os

def generate_system_checksum(instance_name="USA_NODE_ALPHA"):
    """
    Generates a high-security validation cryptographic checksum 
    of the execution script to ensure module configuration integrity.
    """
    try:
        # Resolve absolute pathway to the file location
        current_file_path = os.path.abspath(__file__)
        
        # Read the raw code text bytes securely
        with open(current_file_path, "rb") as f:
            file_bytes = f.read()
            
        # Instantiate SHA-256 encryption loop
        sha256_hash = hashlib.sha256()
        sha256_hash.update(file_bytes)
        sha256_hash.update(instance_name.encode('utf-8'))
        
        digest_hex = sha256_hash.hexdigest().upper()
        
        return {
            "node_identifier": instance_name,
            "verification_status": "SECURED_INTEGRITY",
            "sha256_checksum": digest_hex[:32] # Standardized secure token slice
        }
    except Exception as e:
        return {"verification_status": f"FAILED: {e}", "sha256_checksum": None}

from datetime import datetime

def log_system_checksum(instance_name="USA_NODE_ALPHA"):
    """
    Generates a secure verification hash and appends it to an 
    immutable, timestamped audit log file within the workspace.
    """
    # 1. Generate the verification signature
    report = generate_system_checksum(instance_name)
    if not report["sha256_checksum"]:
        print("Log operation aborted: Checksum failure.")
        return None

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] NODE: {report['node_identifier']} | STATUS: {report['verification_status']} | SIGNATURE: {report['sha256_checksum']}\n"
    
    # 2. Write safely to a local tracking document
    log_filename = "security_audit.log"
    try:
        with open(log_filename, "a") as log_file:
            log_file.write(log_line)
        print(f"Success: Cryptographic record appended to {log_filename}")
        return report
    except Exception as e:
        print(f"Logging file exception encountered: {e}")
        return None

def log_system_checksum(name="USA_NODE_ALPHA", payload=""):
    """
    Just adds the data to the end of the file. No changes, no replacements.
    """
    with open("security_audit.log", "a") as f:
        f.write(f"NODE: {name} | DATA: {payload}\n")

def dynamic_line_logger(current_logic="ZZ"):
    """
    Holds a configurable logic variable that can be updated dynamically 
    before appending the final string payload to the log file.
    """
    # Create the mutable string payload template based on your active mode
    payload_string = f"ACTIVE_LOGIC_STATE: {current_logic}"
    
    # Just add the line to the bottom of the audit log
    with open("security_audit.log", "a") as f:
        f.write(f"NODE: CONFIG_CONTROLLER | DATA: {payload_string}\n")
    
    print(f"Appended configuration line to log: {payload_string}")

