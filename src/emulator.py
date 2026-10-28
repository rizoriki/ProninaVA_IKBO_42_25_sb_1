"""
OS Shell Emulator for Configuration Management Course.
Variant 24: Stages 1-3 implementation.
"""
import os
import sys
import json
import base64
import argparse
import re


class VFSNode:
    """Represents a node in the Virtual File System."""
    def __init__(self, name, is_dir=False, content=None):
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.children = {} if is_dir else None


def load_vfs_from_json(filepath):
    """Loads VFS structure from a JSON file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"VFS file not found: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return build_vfs_tree(data)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in VFS: {filepath}")


def build_vfs_tree(data):
    """Recursively builds VFSNode tree from JSON data."""
    if isinstance(data, dict):
        name = data.get('name', 'root')
        is_dir = data.get('is_dir', False)
        node = VFSNode(name, is_dir=is_dir)
        if is_dir:
            for child in data.get('children', []):
                child_node = build_vfs_tree(child)
                node.children[child_node.name] = child_node
        else:
            if data.get('is_binary', False):
                node.content = base64.b64decode(data.get('content', ''))
            else:
                node.content = data.get('content', '')
        return node
    return None


class Emulator:
    """Main emulator class handling REPL and script execution."""
    def __init__(self, vfs_path=None, script_path=None):
        self.vfs_path = vfs_path
        self.script_path = script_path
        basename = os.path.basename(vfs_path) if vfs_path else "default_vfs"
        self.vfs_name = basename
        self.current_dir = "/"
        self.vfs_root = None

        if vfs_path:
            try:
                self.vfs_root = load_vfs_from_json(vfs_path)
                print(f"[DEBUG] VFS loaded from {vfs_path}")
            except Exception as e:
                print(f"[ERROR] Failed to load VFS: {e}")
                sys.exit(1)
        else:
            print("[DEBUG] No VFS path. Using default in-memory VFS.")
            self.vfs_root = VFSNode("root", is_dir=True)

    def expand_env_vars(self, text):
        """Expands environment variables like $VAR or ${VAR} in text."""
        def replacer(match):
            var_name = match.group(1) or match.group(2)
            return os.environ.get(var_name, match.group(0))
        pattern = r'\$\{([^}]+)\}|\$([A-Za-z_][A-Za-z0-9_]*)'
        return re.sub(pattern, replacer, text)

    def execute_command(self, command_line):
        """Parses and executes a single command line."""
        command_line = self.expand_env_vars(command_line)
        if not command_line.strip():
            return

        if '#' in command_line:
            command_line = command_line.split('#')[0].strip()
            if not command_line:
                return

        parts = command_line.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == 'exit':
            print("Exiting emulator.")
            sys.exit(0)
        elif cmd == 'ls':
            print(f"Executing stub: ls with args {args}")
        elif cmd == 'cd':
            if len(args) != 1:
                print("[ERROR] cd: invalid arguments. Usage: cd <path>")
            else:
                print(f"Executing stub: cd with args {args}")
        else:
            print(f"[ERROR] Unknown command: {cmd}")

    def run_script(self, script_path):
        """Executes commands from a given script file."""
        if not os.path.exists(script_path):
            print(f"[ERROR] Script file not found: {script_path}")
            return

        with open(script_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                print(f"[{self.vfs_name}]$ {line}")
                try:
                    self.execute_command(line)
                except Exception as e:
                    err = f"[ERROR] Error at line {line_num}: {e}"
                    print(err)

    def run_interactive(self):
        """Runs the emulator in interactive REPL mode."""
        print(f"Emulator started. VFS: {self.vfs_name}")
        while True:
            try:
                prompt = f"[{self.vfs_name} {self.current_dir}]$ "
                command_line = input(prompt)
                self.execute_command(command_line)
            except EOFError:
                print("\nExiting emulator.")
                break
            except KeyboardInterrupt:
                print("\nExiting emulator.")
                break


def main():
    """Main entry point for the emulator application."""
    parser = argparse.ArgumentParser(description="OS Shell Emulator")
    parser.add_argument('--vfs', type=str, help="Path to VFS JSON file")
    parser.add_argument('--script', type=str, help="Path to startup script")

    args = parser.parse_args()
    emulator = Emulator(vfs_path=args.vfs, script_path=args.script)

    if args.script:
        emulator.run_script(args.script)
    else:
        emulator.run_interactive()


if __name__ == "__main__":
    main()
