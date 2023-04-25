from tqdm import tqdm

file1 = "TAS-query-original/2023-02-10_1629_bert-base-uncased/test_top1000orSomeOtherName-output.txt"
file2 = "TAS-query-original/2023-02-10_1638_albert/test_top1000orSomeOtherName-output.txt"
file3 = "TAS-query-original/2023-02-10_1638_bert_large/test_top1000orSomeOtherName-output.txt"
out_fused = open("../esci-data-main/shopping_queries_dataset/teacher_fused_test.trec", 'w')
files = [file1, file2, file3]
score_dict = {}

for file in tqdm(files):
    with open(file) as f:
        for line in f:
            qid, did, rank, score = line.strip().split()

            if qid not in score_dict:

                score_dict[qid] = {}

            if did not in score_dict[qid]:
                score_dict[qid][did] = 0

            score_dict[qid][did] += float(score)



for qid in score_dict:
    tem_dict = score_dict[qid]
    sorted_temp = sorted(tem_dict.items(), key=lambda kv: kv[1], reverse=True)
    count = 1
    for did, score in sorted_temp:
        out_fused.write(f'{qid} 0 {did} {count} {score} fused\n')
        count +=1



