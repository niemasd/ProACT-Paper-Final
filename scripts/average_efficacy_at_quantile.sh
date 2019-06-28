#!/usr/bin/env bash
if [ "$#" -ne 2 ]; then
    echo "USAGE: $0 <ordering> <quantile>"; exit 1
fi
q=$2
proact=$1
dir=$(echo $1 | rev | cut -d'/' -f2- | rev)
r=$(echo $1 | rev | cut -d'/' -f1 | rev | cut -d'.' -f1)
trans="$dir/$r.transmissions.txt.gz"
opt=$(echo $proact | sed 's/random/optimal/g' | sed 's/ft\.mv\.proact/optimal/g' | sed 's/tn93\.hivtrace\.growth\.ordering/optimal/g')
rand=$(echo $opt | sed 's/optimal/random/g')

L=$(zcat $proact | wc -l | numlist -mul$q | numlist -ceil)
avg_proact=$(~/siavash_research/ProACT-Paper-Final/scripts/individual_efficacy.py $proact $trans 9 | head -$L | cut -f2 | numlist -avg)
avg_opt=$(~/siavash_research/ProACT-Paper-Final/scripts/individual_efficacy.py $opt $trans 9 | head -$L | cut -f2 | numlist -avg)
avg_rand=$(~/siavash_research/ProACT-Paper-Final/scripts/individual_efficacy.py  $rand $trans 9 | head -$L | cut -f2 | numlist -avg)

numerator=$(echo $avg_proact | numlist -sub$avg_rand)
denominator=$(echo $avg_opt | numlist -sub$avg_rand)
echo $numerator | numlist -div$denominator
