#!/bin/bash
python $2  --config configs/office-train-config_ODA.yaml --source ./txt/source_amazon_obda.txt --target ./txt/target_dslr_obda.txt --gpu $1 --exp_name $3
python $2  --config configs/office-train-config_ODA.yaml --source ./txt/source_amazon_obda.txt --target ./txt/target_webcam_obda.txt --gpu $1 --exp_name $3
python $2  --config configs/office-train-config_ODA.yaml --source ./txt/source_webcam_obda.txt --target ./txt/target_amazon_obda.txt --gpu $1 --exp_name $3
python $2  --config configs/office-train-config_ODA.yaml --source ./txt/source_dslr_obda.txt --target ./txt/target_amazon_obda.txt --gpu $1 --exp_name $3
python $2  --config configs/office-train-config_ODA.yaml --source ./txt/source_dslr_obda.txt --target ./txt/target_webcam_obda.txt --gpu $1 --exp_name $3
python $2  --config configs/office-train-config_ODA.yaml --source ./txt/source_webcam_obda.txt --target ./txt/target_dslr_obda.txt --gpu $1 --exp_name $3
