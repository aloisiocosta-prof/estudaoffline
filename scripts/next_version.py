"""Conventional commits -> SemVer. No version change for unrelated commits."""
import re,subprocess

def next_version(current,messages):
    nums=list(map(int,current.lstrip('v').split('.')))
    if any('BREAKING CHANGE:' in m or re.match(r'^\w+(\([^)]*\))?!:',m) for m in messages): nums=[nums[0]+1,0,0]
    elif any(re.match(r'^feat(\([^)]*\))?:',m) for m in messages):nums=[nums[0],nums[1]+1,0]
    elif any(re.match(r'^fix(\([^)]*\))?:',m) for m in messages):nums[2]+=1
    else:return None
    return '.'.join(map(str,nums))

if __name__=='__main__':
    tags=subprocess.run(['git','describe','--tags','--abbrev=0','--match','v[0-9]*'],capture_output=True,text=True)
    tag=tags.stdout.strip() if tags.returncode==0 else None
    logs=subprocess.check_output(['git','log',*( [f'{tag}..HEAD'] if tag else []),'--format=%B%x00']).decode().split('\0')
    print(next_version(tag or '0.0.0',[m.strip() for m in logs]) or '')
