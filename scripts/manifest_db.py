"""Builds the package manifest DB from an extracted image tree.
Usage: manifest_db.py <extracted_root> <manifests.json>
<extracted_root> holds the partition directories (system/, vendor/, product/). Every *.apk below it is read
with aapt2 (AAPT2 env var, default from tools/env.sh). Each entry's `file` is the APK path relative to
<extracted_root>. A directory of pre-dumped `<path with / as __>.apk.txt` files is also accepted (legacy)."""
import os,re,json,sys,glob,subprocess
rx=re.compile(r'^(\s*)(E|A): (.*)$')
def parse(p):
    root={'tag':'root','attrs':{},'kids':[]};stack=[(-1,root)]
    for line in open(p,errors='ignore'):
        m=rx.match(line.rstrip('\n'))
        if not m: continue
        ind=len(m.group(1));k=m.group(2);t=m.group(3)
        if k=='E':
            tag=t.split(' ')[0];n={'tag':tag,'attrs':{},'kids':[]}
            while stack[-1][0]>=ind: stack.pop()
            stack[-1][1]['kids'].append(n);stack.append((ind,n))
        else:
            mm=re.match(r'(?:\S+:)?(\w+)(?:\(0x[0-9a-f]+\))?=(.*)$',t.split('android:')[-1] if 'android:' in t else t)
            if mm:
                v=mm.group(2);v2=re.match(r'"([^"]*)"',v);v=v2.group(1) if v2 else v.split(' ')[0]
                stack[-1][1]['attrs'][mm.group(1)]=v
    return root
def walk(n):
    yield n
    for k in n['kids']: yield from walk(k)
def dump_text(apk):
    aapt2=os.environ.get('AAPT2') or os.path.expanduser('~/Library/Android/sdk/build-tools/36.0.0/aapt2')
    r=subprocess.run([aapt2,'dump','xmltree','--file','AndroidManifest.xml',apk],capture_output=True,text=True)
    return r.stdout if r.returncode==0 else None
def parse_text(text,tmp):
    open(tmp,'w').write(text); return parse(tmp)
def entry(man,file):
    e={'file':file,'sharedUserId':man['attrs'].get('sharedUserId'),
     'uses_perm':[],'decl_perm':{},'uses_lib':[],'uses_feature':[],'components':[],'authorities':[],'actions':set(),'home':False,'persistent':False,'targets':set()}
    for n in walk(man):
        a=n['attrs'];t=n['tag']
        if t=='uses-permission': e['uses_perm'].append(a.get('name'))
        elif t=='permission': e['decl_perm'][a.get('name')]=a.get('protectionLevel')
        elif t in('uses-library','uses-static-library'): e['uses_lib'].append((a.get('name'),a.get('required','true')))
        elif t=='uses-feature' and a.get('name','').startswith('com.'): e['uses_feature'].append(a.get('name'))
        elif t=='application': e['persistent']=a.get('persistent')=='0xffffffff'
        elif t in('activity','service','receiver','provider','activity-alias'):
            ex=a.get('exported');hasf=any(k['tag']=='intent-filter' for k in n['kids'])
            e['components'].append((t,a.get('name'),'exp' if ex=='0xffffffff' or (ex is None and hasf) else '',a.get('permission')))
            if t=='provider' and a.get('authorities'): e['authorities']+=a['authorities'].split(';')
        elif t=='action': e['actions'].add(a.get('name'))
        elif t=='category' and a.get('name')=='android.intent.category.HOME': e['home']=True
        elif t=='meta-data' or t=='queries' or t=='package':
            for v in a.values():
                if isinstance(v,str) and re.match(r'^com\.amazon\.[\w.]+$',v): e['targets'].add(v)
    e['actions']=sorted(x for x in e['actions'] if x);e['targets']=sorted(e['targets'])
    return e
def main(apk_root,out_json):
    import tempfile
    out={}
    with tempfile.TemporaryDirectory() as td:
        tmp=os.path.join(td,'m.txt')
        if glob.glob(apk_root+'/*.txt'):   # legacy: pre-dumped text files
            items=[(os.path.basename(f)[:-4].replace('__','/'),open(f,errors='ignore').read()) for f in sorted(glob.glob(apk_root+'/*.txt'))]
        else:
            apks=sorted(os.path.join(d,f) for d,_,fs in os.walk(apk_root) for f in fs if f.endswith('.apk'))
            items=[(os.path.relpath(a,apk_root),dump_text(a)) for a in apks]
        for file,text in items:
            if not text: continue
            r=parse_text(text,tmp);man=next((n for n in walk(r) if n['tag']=='manifest'),None)
            if not man: continue
            out.setdefault(man['attrs'].get('package'),[]).append(entry(man,file))
    json.dump(out,open(out_json,'w'),indent=1,default=list)
    return len(out)
if __name__=='__main__':
    if len(sys.argv)!=3: sys.exit(__doc__)
    print(main(sys.argv[1],sys.argv[2]))
