import tensorflow as tf
import time
from models.losses import loss_function
import  numpy as np

def train_model(model, dataset, params, ckpt_manager,vocab):
    print(vocab)
    start_index = vocab.word_to_id('[START]')
    pad_index = vocab.word_to_id('[PAD]')

    #设置优化器,学习率使用衰减的学习率效果会更好
    optimizer = tf.keras.optimizers.Adam(name='Adam', learning_rate=params["learning_rate"])
    #在colab中用@tf.function()加速会报错
    # @tf.function()
    def train_step(enc_inp, dec_tar,pad_index):
        #开启会话：session
        with tf.GradientTape() as tape:
            # print('enc_inp shape is final for model :', enc_inp.get_shape())
            enc_output, enc_hidden = model.encoder(enc_inp)
            # 第一个decoder输入 开始标签
            # dec_input (batch_size, 1)
            # dec_input = tf.expand_dims([start_index], 1)
            dec_input = tf.expand_dims([start_index] * params["batch_size"], 1)
            dec_hidden = enc_hidden
            #即调用model(SequenceToSequence)的call函数
            predictions, _ = model(dec_input, dec_hidden, enc_output, dec_tar)
            loss = loss_function(dec_tar[:,1:], predictions,pad_index)

        #梯度回传,基本为固定写法
        variables = model.trainable_variables
        gradients = tape.gradient(loss, variables)
        optimizer.apply_gradients(zip(gradients, variables))
        return loss

    #第一层循环为epoch循环
    for epoch in range(params['epochs']):
        t0 = time.time()
        step = 0
        total_loss = 0
        # print(len(dataset.take(params['steps_per_epoch'])))
        #第二层循环为batch循环
        for step, batch in enumerate(dataset.take(params['steps_per_epoch'])):
            #假设样本数是1000，batch size为10,一个epoch，我们一共有100次，200， 500， 40，20等取法
            #batch[0]:output_types
            #batch[1]:output_shapes
            batch_loss = train_step(batch[0]["enc_input"],       # shape=(16, 200)
                              batch[1]["dec_target"],pad_index)  # shape=(16, 50)
            total_loss += batch_loss
            step += 1
            if step % 100 == 0:
                print('Epoch {} Batch {} Loss {:.4f}'.format(epoch + 1, step, batch_loss.numpy()))

        if epoch % 1 == 0:
            ckpt_save_path = ckpt_manager.save()
            print('Saving checkpoint for epoch {} at {} ,best loss {}'.format(epoch + 1, ckpt_save_path, total_loss/step))
            print('Epoch {} Loss {:.4f}'.format(epoch + 1, total_loss/step))
            print('Time taken for 1 epoch {} sec\n'.format(time.time() - t0))
            #学习率的衰减，按照训练的次数来更新学习率（tf1.x）
            lr = params['learning_rate'] * np.power(0.9,epoch+1)    #按0.9的幂衰减
            optimizer = tf.keras.optimizers.Adam(name='Adam', learning_rate=lr)
            print("learning_rate=", optimizer.get_config()["learning_rate"])