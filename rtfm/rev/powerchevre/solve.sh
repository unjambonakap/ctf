
for f in til xpo ut mst ast wst lst; do 
  strings -el $f.exe  | grep -E '.{50}' | base64 -d >> t1
done


