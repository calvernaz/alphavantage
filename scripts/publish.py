#!/usr/bin/env python3
"""
Script to build and publish the alphavantage-mcp package to PyPI.

Usage:
    python scripts/publish.py --test           # Publish to TestPyPI using twine
    python scripts/publish.py                  # Publish to PyPI using twine
    python scripts/publish.py --test --use-uv  # Publish to TestPyPI using uv publish
    python scripts/publish.py --use-uv         # Publish to PyPI using uv publish
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return True if successful."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr.strip()}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Build and publish alphavantage-mcp package")
    parser.add_argument(
        "--test", 
        action="store_true", 
        help="Publish to TestPyPI instead of PyPI"
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip building and only upload existing dist files"
    )
    parser.add_argument(
        "--use-uv",
        action="store_true",
        help="Use uv publish instead of twine (default: use twine)"
    )
    args = parser.parse_args()

    # Change to project root
    project_root = Path(__file__).parent.parent
    print(f"📁 Working in: {project_root}")
    
    if not args.skip_build:
        # Clean previous builds
        dist_dir = project_root / "dist"
        if dist_dir.exists():
            print("🧹 Cleaning previous builds...")
            import shutil
            shutil.rmtree(dist_dir)

        # Build the package
        if not run_command(
            ["uv", "build"], 
            "Building package"
        ):
            sys.exit(1)

    # Check if dist files exist
    dist_dir = project_root / "dist"
    if not dist_dir.exists() or not list(dist_dir.glob("*.whl")):
        print("❌ No built packages found in dist/")
        print("   Run without --skip-build to build the package first")
        sys.exit(1)

    # Upload to PyPI or TestPyPI
    if args.test:
        repository_name = "testpypi"
        print("🧪 Publishing to TestPyPI...")
        print("   You can install with: pip install -i https://test.pypi.org/simple/ alphavantage-mcp")
    else:
        repository_name = "pypi"
        print("🚀 Publishing to PyPI...")
        print("   After publishing, users can install with: uvx alphavantage-mcp")

    # Choose upload method
    if args.use_uv:
        # Use uv publish
        repository_url = "https://test.pypi.org/legacy/" if args.test else "https://upload.pypi.org/legacy/"
        upload_cmd = [
            "uv", "publish",
            "--publish-url", repository_url,
            str(dist_dir / "*")
        ]
        auth_help = "uv publish --help"
    else:
        # Use twine (default)
        upload_cmd = [
            "uv", "run", "twine", "upload",
            "--repository", repository_name,
            str(dist_dir / "*")
        ]
        auth_help = "~/.pypirc file or environment variables"

    if not run_command(upload_cmd, f"Uploading to {repository_name}"):
        print(f"\n💡 If authentication failed, make sure you have:")
        print(f"   1. Created an account on {repository_name}")
        print(f"   2. Generated an API token")
        print(f"   3. Set up authentication with: {auth_help}")
        sys.exit(1)

    print(f"\n🎉 Package successfully published to {repository_name.upper()}!")

    if args.test:
        print("\n📋 Next steps:")
        print("   1. Test the installation: pip install -i https://test.pypi.org/simple/ alphavantage-mcp")
        print("   2. If everything works, publish to PyPI: python scripts/publish.py")
    else:
        print("\n📋 Users can now install with:")
        print("   uvx alphavantage-mcp")
        print("   or")
        print("   pip install alphavantage-mcp")


if __name__ == "__main__":
    main()
