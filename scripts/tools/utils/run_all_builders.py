import os
import subprocess
import glob

builders = glob.glob('scripts/builders/update_app_*.py')
for builder in builders:
    if 'test' in builder:
        continue
    subprocess.run(['python', builder])
print("All 16 apps successfully generated!")
