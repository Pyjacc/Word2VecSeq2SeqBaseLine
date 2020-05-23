# Word2VecSeq2SeqBaseLine
Word2VecSeq2SeqBaseLine

# 一. Homework-week4
利用前三节作业内容，完成自己的seq2seq模型训练，并能够通过Greedy search或者Beam search的方法跑出测试结果。
## 1. 继续优化seq2seq模型训练
## 2. 对baseline模型进行测试
通过Greedy search或者Beam search的方法跑出测试结果

# 二. 功能实现  
1、原始数据AutoMaster_TestSet.csv和AutoMaster_TrainSet.csv都只保留50条，便于快速调试跑通模型  
2、在encoder.py中实现encoder层  
3、在decoder.py中实现decoder层  
4、 在attention.py中实现attention层  
5、在seq2seq.py中实现seq2seq模型  
6、在losses.py中定义loss函数  
7、 实现train和test功能（修改main_activity.py中parse的mode参数实现train还是test）  

# 三. 代码使用说明  
1. 第一步：clean data：执行clean_data.py  
2. 第二步：build vocab.txt：执行build_vocab_dict.py  
3. 第三步：构建embedding_matrix： 执行train_word2vec_model.py  
4. 第四步：修改run.py中params["mode"] == "train"，开始训练  
5. 第五步：修改run.py中params["mode"] == "test"，开始预测  

注：当本次train时改变模型的维度，如vocab_size改变,embed_size改变，都要删除原模型数据后（ckpt下的数据）
再进行训练和测试  


# 四. 下一步计划  
对模型进行微调或调整模型，再次进行训练，提高预测分数  



