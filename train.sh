

#python3 train.py --batch-size 8 --img 768 768 --data data/obj.yaml --cfg models/yolor-ssss-s2d.yaml --weights '' --device 0 --name yolor_small --hyp hyp.scratch.1280.yaml --epochs 300


python3 train.py --batch-size 16 --img 1380 1380 --data data/obj.yaml --cfg models/yolor-d6-rotated-1c.yaml --weights '' --device 0 --name yolor-d6 --hyp hyp.scratch.dota.4096.yaml --epochs 30
