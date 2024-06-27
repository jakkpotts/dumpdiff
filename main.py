import sys

def compare_dumps(file1, file2, block_size=16):
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE1 = '\033[94m'
    BLUE2 = '\033[96m'
    RESET = '\033[0m'

    def format_block(block, diffs):
        """Format the block to highlight differences with color."""
        result = []
        for i, byte in enumerate(block):
            if i in diffs:
                result.append(RED + f"{byte:02x}" + RESET)
            else:
                result.append(GREEN + f"{byte:02x}" + RESET)
        return ' '.join(result)

    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()

    block_count = max(len(data1), len(data2)) // block_size + 1

    for i in range(block_count):
        block1 = data1[i*block_size:(i+1)*block_size]
        block2 = data2[i*block_size:(i+1)*block_size]

        if block1 != block2:
            diffs = [j for j in range(len(block1)) if j >= len(block2) or block1[j] != block2[j]]
            print(f"{YELLOW}Difference in block {i}:{RESET}")
            print(f"  {BLUE1}{file1}:{RESET} {format_block(block1, diffs)}")
            print(f"  {BLUE2}{file2}:{RESET} {format_block(block2, diffs)}")

    if len(data1) != len(data2):
        print(f"{YELLOW}Files have different lengths: {len(data1)} != {len(data2)}{RESET}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 compare_dumps.py <file1> <file2> [block_size]")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    block_size = int(sys.argv[3]) if len(sys.argv) > 3 else 16

    compare_dumps(file1, file2, block_size)