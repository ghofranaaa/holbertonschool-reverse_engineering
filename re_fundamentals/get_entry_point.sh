#!/bin/bash
# get_entry_point.sh
# Usage: ./get_entry_point.sh <elf-file>

set -euo pipefail

# Check argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <elf-file>" >&2
    exit 1
fi

file="$1"

# Check file exists
if [ ! -f "$file" ]; then
    echo "Error: file '$file' does not exist." >&2
    exit 2
fi

# Try to get ELF header via readelf -h. If readelf fails, assume not an ELF file.
header="$(readelf -h "$file" 2>/dev/null)" || {
    echo "Error: '$file' is not a valid ELF file or readelf failed." >&2
    exit 3
}

# Populate variables expected by messages.sh
file_name="$file"

# Magic: capture the bytes after the "Magic:" token (keep spacing as sequence of hex bytes)
magic_number="$(echo "$header" | awk '/Magic:/ { $1=""; sub(/^ +/,""); print }' | tr -s ' ')"

# Class: e.g., ELF64 or ELF32 (take the value after "Class:")
class="$(echo "$header" | awk -F: '/Class:/ { gsub(/^[ \t]+|[ \t]+$/,"",$2); print $2 }')"

# Byte Order: use readelf's "Data:" line (e.g., little endian / big endian)
byte_order="$(echo "$header" | awk -F: '/Data:/ { gsub(/^[ \t]+|[ \t]+$/,"",$2); sub(/.*,\s*/,"",$2); print $2 }')"

# Entry point address: capture the hex address after "Entry point address:"
entry_point_address="$(echo "$header" | awk -F: '/Entry point address:/ { gsub(/^[ \t]+|[ \t]+$/,"",$2); print $2 }')"

# Source messages.sh from same directory (use relative path so no hardcoded absolute paths)
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
messages_sh="$script_dir/messages.sh"

if [ ! -f "$messages_sh" ]; then
    echo "Error: messages.sh not found in script directory ($script_dir)." >&2
    exit 4
fi

# shellcheck source=/dev/null
source "$messages_sh"

# Call the display function provided in messages.sh
display_elf_header_info
