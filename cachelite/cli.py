import sys
import argparse
from .store import CacheStore

def main():
    parser = argparse.ArgumentParser(prog="cachelite", description="In-memory cache CLI.")
    parser.add_argument("--wal", default="cache.wal", help="Path to WAL file")
    subparsers = parser.add_subparsers(dest="command")

    set_p = subparsers.add_parser("set", help="Set a key")
    set_p.add_argument("key")
    set_p.add_argument("value")
    set_p.add_argument("--ttl", type=float, help="TTL in seconds")

    get_p = subparsers.add_parser("get", help="Get a key")
    get_p.add_argument("key")

    args = parser.parse_args()
    store = CacheStore(wal_path=args.wal)

    try:
        if args.command == "set":
            store.set(args.key, args.value, ttl_seconds=args.ttl)
            print(f"OK (key '{args.key}' set)")
        elif args.command == "get":
            val = store.get(args.key)
            if val is None:
                print("(nil)")
            else:
                print(val)
        else:
            parser.print_help()
    finally:
        store.close()

if __name__ == "__main__":
    main()
