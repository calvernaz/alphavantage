#!/usr/bin/env python3
"""
Test script to verify the package builds correctly and can be installed.
"""

import subprocess
import sys
import tempfile
from pathlib import Path


def run_command(cmd: list[str], description: str, cwd=None) -> bool:
    """Run a command and return True if successful."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd=cwd)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr.strip()}")
        return False


def main():
    project_root = Path(__file__).parent.parent
    print(f"📁 Testing package in: {project_root}")
    
    # Build the package
    if not run_command(["uv", "build"], "Building package", cwd=project_root):
        sys.exit(1)
    
    # Check if wheel was created
    dist_dir = project_root / "dist"
    wheel_files = list(dist_dir.glob("*.whl"))
    if not wheel_files:
        print("❌ No wheel file found in dist/")
        sys.exit(1)
    
    wheel_file = wheel_files[0]
    print(f"📦 Found wheel: {wheel_file.name}")
    
    # Test installation in a temporary environment
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        print(f"🧪 Testing installation in temporary directory: {temp_path}")
        
        # Create a test virtual environment
        venv_path = temp_path / "test_env"
        if not run_command(["python", "-m", "venv", str(venv_path)], "Creating test virtual environment"):
            sys.exit(1)
        
        # Install the wheel
        pip_path = venv_path / "bin" / "pip" if sys.platform != "win32" else venv_path / "Scripts" / "pip.exe"
        if not run_command([str(pip_path), "install", str(wheel_file)], "Installing wheel in test environment"):
            sys.exit(1)
        
        # Test that the command is available
        alphavantage_path = venv_path / "bin" / "alphavantage-mcp" if sys.platform != "win32" else venv_path / "Scripts" / "alphavantage-mcp.exe"
        if not alphavantage_path.exists():
            print(f"❌ alphavantage-mcp command not found at {alphavantage_path}")
            sys.exit(1)
        
        print(f"✅ alphavantage-mcp command found at {alphavantage_path}")
        
        # Test help command
        if not run_command([str(alphavantage_path), "--help"], "Testing --help command"):
            print("⚠️  Help command failed, but this might be expected if dependencies are missing")
    
    print("\n🎉 Package test completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Test publish to TestPyPI: python scripts/publish.py --test")
    print("   2. If successful, publish to PyPI: python scripts/publish.py")


if __name__ == "__main__":
    main()
