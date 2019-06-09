import tfcoreml
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tfcoreml.convert(tf_model_path="optimized_net_best_acc.pb",
                     mlmodel_path="model.mlmodel",
                     output_feature_names=['net_graph/Reshape_1:0'],
                     input_name_shape_dict={'Mul:0'})
