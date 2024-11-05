#!/usr/bin/env sh
test=2019-10-09
test_coor=107
test_size=20000
train_size=80000
sample_input_size=$((train_size * 4))
i=0
amnt=50
while [ "$i" -lt "$amnt" ]
do
	cat cat_file4.csv | grep "$test" | shuf | sed "$test_size"q > test_file.csv
	cat cat_file4.csv | sed "$sample_input_size"q | sed 's/,/ /g' | awk ' $2 -lt "$test" {print}' | sed 's/ /,/g' | shuf | sed "$train_size"q > train_file.csv
	cat train_file.csv | wc -l
	./random_forest.py train_file.csv test_file.csv | grep -v Warning > "$i".txt
	i=$((i + 1))
	test_coor=$((test_corr - 1))
	test=$(cat cat_file4.csv | cut -d',' -f2 | sort | uniq | sed -n "$test_coor"p)
done
