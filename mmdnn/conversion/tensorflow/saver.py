import tensorflow as tf


def save_model(MainModel, network_filepath, weight_filepath, dump_filepath, dump_tag = 'SERVING'):
    if dump_tag == 'SERVING':
        tag_list = [tf.saved_model.SERVING]
    else:
        tag_list = [tf.saved_model.TRAINING]
    res = MainModel.KitModel(weight_filepath)
    input = res[0]
    model = res[1:]
    with tf.compat.v1.Session() as sess:
        sess.run(tf.compat.v1.global_variables_initializer())

        builder = tf.compat.v1.saved_model.builder.SavedModelBuilder(dump_filepath)

        tensor_info_input = tf.compat.v1.saved_model.utils.build_tensor_info(input)
        outputs = {'output{}'.format(i): tf.compat.v1.saved_model.utils.build_tensor_info(model[i]) for i in range(len(model))}
        prediction_signature = (
            tf.compat.v1.saved_model.signature_def_utils.build_signature_def(
                inputs={'input': tensor_info_input},
                outputs=outputs,
                method_name=tf.saved_model.PREDICT_METHOD_NAME
            )
        )

        builder.add_meta_graph_and_variables(
            sess,
            tag_list,
            signature_def_map={
                tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY: prediction_signature
            }
        )

        save_path = builder.save()

    print('Tensorflow file is saved as [{}], generated by [{}.py] and [{}].'.format(
        save_path, network_filepath, weight_filepath))
