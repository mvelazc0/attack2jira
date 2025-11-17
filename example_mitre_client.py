#!/usr/bin/env python3
"""
Example usage of the MITRE ATT&CK client.

This script demonstrates how to use the MitreClient to fetch and process
MITRE ATT&CK techniques, tactics, and data sources.
"""

import asyncio
import logging
from src.mitre.client import MitreClient, MitreAPIError


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def main():
    """Main example function."""
    print("=" * 80)
    print("MITRE ATT&CK Client Example")
    print("=" * 80)

    try:
        # Create client using async context manager
        async with MitreClient() as client:

            # Example 1: Get all techniques
            print("\n1. Fetching all techniques...")
            techniques = await client.get_techniques()
            print(f"   Total techniques: {len(techniques)}")
            print(f"   First 3 techniques:")
            for tech in techniques[:3]:
                print(f"   - {tech}")

            # Example 2: Filter by tactic
            print("\n2. Fetching techniques for 'initial-access' tactic...")
            initial_access = await client.get_techniques(tactic="initial-access")
            print(f"   Found {len(initial_access)} techniques")
            for tech in initial_access[:3]:
                print(f"   - {tech}")

            # Example 3: Get a specific technique
            print("\n3. Fetching a specific technique...")
            technique = await client.get_technique_by_id("T1566")
            if technique:
                print(f"   {technique}")
                print(f"   Description: {technique.description[:100]}...")
                print(f"   Data sources: {', '.join(technique.data_sources[:3])}")

            # Example 4: Get parent techniques only
            print("\n4. Fetching parent techniques...")
            parents = await client.get_parent_techniques()
            print(f"   Total parent techniques: {len(parents)}")

            # Example 5: Get sub-techniques
            print("\n5. Fetching sub-techniques...")
            subtechniques = await client.get_subtechniques()
            print(f"   Total sub-techniques: {len(subtechniques)}")
            if subtechniques:
                print(f"   First sub-technique: {subtechniques[0]}")
                print(f"   Parent: {subtechniques[0].parent_id}")

            # Example 6: Get all tactics
            print("\n6. Fetching all tactics...")
            tactics = await client.get_tactics()
            print(f"   Total tactics: {len(tactics)}")
            print(f"   Tactics: {', '.join(t.name for t in tactics)}")

            # Example 7: Get all data sources
            print("\n7. Fetching data sources...")
            data_sources = await client.get_data_sources()
            print(f"   Total data sources: {len(data_sources)}")
            print(f"   First 5: {', '.join(ds.name for ds in data_sources[:5])}")

            # Example 8: Using cache
            print("\n8. Demonstrating cache (second call should be instant)...")
            import time
            start = time.time()
            await client.get_techniques()
            elapsed = time.time() - start
            print(f"   Second call took {elapsed:.4f} seconds (cached)")

    except MitreAPIError as e:
        print(f"\n❌ Error: {e}")
        return 1

    print("\n" + "=" * 80)
    print("✅ All examples completed successfully!")
    print("=" * 80)
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
