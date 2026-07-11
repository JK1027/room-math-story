import os
import glob

base_dir = r'c:\Coding_Notebook\Projects\school\room-math-story\stories'
output_file = r'c:\Coding_Notebook\Projects\school\room-math-story\all_problems.txt'

files = glob.glob(os.path.join(base_dir, '**', '*.txt'), recursive=True)
files.sort()

with open(output_file, 'w', encoding='utf-8') as out_f:
    for fpath in files:
        with open(fpath, 'r', encoding='utf-8') as in_f:
            content = in_f.read()
            
            try:
                # Some files might have different headings. Let's try to extract loosely if strict fails.
                q_sec = content.split('## 3.')[1].split('## 4.')[0]
                a_sec = content.split('## 5.')[1].split('## 6.')[0]
                out_f.write(f'--- {os.path.basename(fpath)} ---\n')
                out_f.write('QUESTIONS:\n' + q_sec.strip() + '\n')
                out_f.write('ANSWERS:\n' + a_sec.strip() + '\n\n')
            except IndexError:
                out_f.write(f'--- {os.path.basename(fpath)} ---\nERROR PARSING\n\n')
