cat res_init.out | grep -A 1 call  | grep -v call | awk '{ print $3 }' | sort | uniq
