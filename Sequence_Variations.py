
# opens the file
def read_alignment_file(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content
# 
def parse_alignment(file_content):
    # splits into lines and works out if its a query or subject
    lines = file_content.split('\n')
    seq1, seq2 = "", ""
    for line in lines:
        parts = line.split()
        if line.startswith('Query'):
            seq1 += parts[2]
        elif line.startswith('Sbjct'):
            seq2 += parts[2]
    return seq1, seq2

def analyze_mutations(seq1, seq2):
    mutations = {'substitutions': [], 'insertions': [], 'deletions': []}
    counts = {'substitutions': 0, 'insertions': 0, 'deletions': 0}  # Initialize counts
    gap_seq1, gap_seq2 = False, False
    gap_start = -1

    for i in range(len(seq1)):
        if seq1[i].upper() != seq2[i].upper():
            if seq1[i] == '-' or seq2[i] == '-':
                if not gap_seq1 and seq1[i] == '-':
                    gap_seq1, gap_seq2 = True, False
                    gap_start = i
                elif not gap_seq2 and seq2[i] == '-':
                    gap_seq1, gap_seq2 = False, True
                    gap_start = i
            else:
                if seq1[i].isalpha() and seq2[i].isalpha():
                    mutations['substitutions'].append({'position': i+1, 'from': seq1[i], 'to': seq2[i]})
                    counts['substitutions'] += 1  # Count substitution
        else:
            if gap_seq1 or gap_seq2:
                gap_type = 'insertions' if gap_seq1 else 'deletions'
                mutations[gap_type].append({'start': gap_start+1, 'length': i - gap_start})
                counts[gap_type] += 1  # Count insertion or deletion
                gap_seq1, gap_seq2 = False, False

    return mutations, counts

# Example usage
file_path = '/Users/jessicaeweje/Downloads/34BY7XK9114-Alignment.txt'  # Adjust the file path accordingly
file_content = read_alignment_file(file_path)
seq1, seq2 = parse_alignment(file_content)
mutations, counts = analyze_mutations(seq1, seq2)

print("Counts:")
print("Substitutions:", counts['substitutions'])
print("Insertions:", counts['insertions'])
print("Deletions:", counts['deletions'])
print("\nDetailed Information:")
print("Substitutions:", mutations['substitutions'])
print(