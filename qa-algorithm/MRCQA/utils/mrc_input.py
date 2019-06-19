#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'han'

import os
import torch
import logging
import spacy
import numpy as np
import matplotlib.pyplot as plt
from models import *
from dataset.squad_dataset import SquadDataset
from dataset.preprocess_data import DocText
from utils.load_config import init_logging, read_config
from utils.functions import to_long_tensor, count_parameters, draw_heatmap_sea
import json
import time
from utils.functions import pad_sequences

init_logging()
logger = logging.getLogger(__name__)

class mrc:
    def __init__(self, config_file = "/mnt/sdb/cjm/Match-LSTM/config/id19.yaml"):
        logger.info('------------MODEL TEST INPUT--------------')
        logger.info('loading config file...')
        #self.global_config = read_config("config/id19.yaml")
        self.global_config = read_config(config_file)

        # set random seed
        seed = self.global_config['global']['random_seed']
        torch.manual_seed(seed)

        torch.set_grad_enabled(False)  # make sure all tensors below have require_grad=False

        # set default gpu
        os.environ["CUDA_VISIBLE_DEVICES"] = str(self.global_config['test']["gpu_id"])

        enable_cuda = self.global_config['test']['enable_cuda']
        self.device = torch.device("cuda" if enable_cuda else "cpu")
        if torch.cuda.is_available() and not enable_cuda:
            logger.warning("CUDA is avaliable, you can enable CUDA in config file")
        elif not torch.cuda.is_available() and enable_cuda:
            raise ValueError("CUDA is not abaliable, please unable CUDA in config file")

        logger.info('reading squad dataset...')
        self.dataset = SquadDataset(self.global_config)

        logger.info('constructing model...')
        model_choose = self.global_config['global']['model']
        dataset_h5_path = self.global_config['data']['dataset_h5']
        if model_choose == 'base':
            model = BaseModel(dataset_h5_path,
                              model_config=read_config('config/base_model.yaml'))
        elif model_choose == 'match-lstm':
            model = MatchLSTM(dataset_h5_path)
        elif model_choose == 'match-lstm+':
            model = MatchLSTMPlus(dataset_h5_path, self.global_config['preprocess']['use_domain_tag'])
        elif model_choose == 'r-net':
            model = RNet(dataset_h5_path)
        elif model_choose == 'm-reader':
            model = MReader(dataset_h5_path)
        else:
            raise ValueError('model "%s" in config file not recoginized' % model_choose)
        model = model.to(self.device)
        model.eval()  # let training = False, make sure right dropout
        logging.info('model parameters count: %d' % count_parameters(model))

        # load model weight
        logger.info('loading model weight...')
        model_weight_path = self.global_config['data']['model_path']
        is_exist_model_weight = os.path.exists(model_weight_path)
        assert is_exist_model_weight, "not found model weight file on '%s'" % model_weight_path

        weight = torch.load(model_weight_path, map_location=lambda storage, loc: storage)
        if enable_cuda:
            weight = torch.load(model_weight_path, map_location=lambda storage, loc: storage.cuda())
        model.load_state_dict(weight, strict=False)
        self.model = model

        self.nlp = spacy.load('en')
        self.metadata = {k: v.tolist() for k, v in self.dataset.meta_data.items()}

    def mrcqa_batch(self, contexts, question, single_question = True):
        if single_question:
            questions = []
            for i in range(len(contexts)):
                questions.append(question)
            data_nopad = self.build_data(contexts, questions)
        else:
            data_nopad = self.build_data(contexts, question)
        data_pad = {
            'context': self.dict2array(data_nopad['context']),
            'question': self.dict2array(data_nopad['question']),
            'answer_range': pad_sequences(data_nopad['answer_range'],
                                          padding='post',
                                          value=-1),
            'samples_id': np.array(data_nopad['samples_id'])
        }
        batch_data = self.dataset.get_input_dataloader(self.global_config['test']['batch_size'],
                                                  self.global_config['global']['num_data_workers'],
                                                  shuffle=False, input_data=data_pad)
        # batch_data = dataset.get_dataloader_test(32, 5)

        batch_cnt = len(batch_data)
        answer = []

        cdict = data_pad['context']
        right_space = cdict['right_space']

        cnt = 0
        for bnum, batch in enumerate(batch_data):
            batch = [x.to(self.device) if x is not None else x for x in batch]
            bat_context = batch[0]
            bat_answer_range = batch[-1]

            # forward
            batch_input = batch[:len(batch) - 1]
            _, tmp_ans_range, _ = self.model.forward(*batch_input)

            tmp_context_ans = zip(bat_context.cpu().data.numpy(),
                                  tmp_ans_range.cpu().data.numpy())

            # generate initial answer text
            i = 0
            for c, a in tmp_context_ans:
                cur_no = cnt + i
                tmp_ans = self.dataset.sentence_id2word(c[a[0]:(a[1] + 1)])
                cur_space = right_space[cur_no][a[0]:(a[1] + 1)]

                cur_ans = ''
                for j, word in enumerate(tmp_ans):
                    cur_ans += word
                    if cur_space[j]:
                        cur_ans += ' '
                answer.append(cur_ans.strip())
                i += 1
            cnt += i
            logging.info('batch=%d/%d' % (bnum, batch_cnt))

            # manual release memory, todo: really effect?
            del bat_context, bat_answer_range, batch, batch_input
            del tmp_ans_range
            # torch.cuda.empty_cache()
        return answer

    def build_data(self, contexts, question):
        contexts_ids = []
        questions_ids = []
        answers_range_wid = []  # each answer use the [start,end] representation, all the answer horizontal concat
        samples_id = []
        cnt = 0
        for i, context in enumerate(contexts):
            context_doc = DocText(self.nlp, context, self.global_config['preprocess'])
            question_doc = DocText(self.nlp, question[i], self.global_config['preprocess'])

            context_doc.update_em(question_doc)
            question_doc.update_em(context_doc)

            context_f = context_doc.to_id_dict(self.metadata)
            question_f = question_doc.to_id_dict(self.metadata)

            contexts_ids.append(context_f)
            questions_ids.append(question_f)
            samples_id.append(str(cnt))
            answers_range_wid.append([0, 1])
            cnt += 1
        return {'context': contexts_ids,
                'question': questions_ids,
                'answer_range': answers_range_wid,
                'samples_id': samples_id
                }

    def dict2array(self, data_doc, use_domain_tag=False):
        """
        transform dict to numpy array
        :param data_doc: [{'token': [], 'pos': [], 'ent': [], 'em': [], 'em_lemma': [], 'right_space': [], 'domain_tag':[]]
        :return:
        """
        data = {'token': [], 'pos': [], 'ent': [], 'em': [], 'em_lemma': [], 'right_space': []}
        if use_domain_tag:
            data['domain_tag'] = []
        max_len = 0

        for ele in data_doc:
            assert ele.keys() == data.keys()

            if len(ele['token']) > max_len:
                max_len = len(ele['token'])

            for k in ele.keys():
                if len(ele[k]) > 0:
                    data[k].append(ele[k])

        for k in data.keys():
            if len(data[k]) > 0:
                data[k] = pad_sequences(data[k],
                                        maxlen=max_len,
                                        padding='post',
                                        value=0)

        return data

def mrcqa( nlp, context, question, model, dataset, metadata, global_config,device):


    # preprocess
    context_doc = DocText(nlp, context, global_config['preprocess'])
    question_doc = DocText(nlp, question, global_config['preprocess'])
    context_doc.update_em(question_doc)
    question_doc.update_em(context_doc)


    context_token = context_doc.token
    question_token = question_doc.token
    context_id_char = to_long_tensor(dataset.sentence_char2id(context_token))
    question_id_char = to_long_tensor(dataset.sentence_char2id(question_token))


    context_id, context_f = context_doc.to_id(metadata)
    question_id, question_f = question_doc.to_id(metadata)
    bat_input = [context_id, question_id, context_id_char, question_id_char, context_f, question_f]
    bat_input = [x.unsqueeze(0).to(device) if x is not None else x for x in bat_input]

    out_ans_prop, out_ans_range, vis_param = model.forward(*bat_input)
    out_ans_range = out_ans_range.cpu().data.numpy()
    start = out_ans_range[0][0]
    end = out_ans_range[0][1] + 1

    out_answer_id = context_id[start:end]
    out_answer = dataset.sentence_id2word(out_answer_id)
    space = context_doc.right_space[start:end]

    result_answer = ''
    for i, token in enumerate(out_answer):
        if space[i]:
            result_answer += (token+' ')
        else:
            result_answer += token
    return result_answer.strip()







def main():
    rf = "data/ccbase/ccbase_test.json"
    wf = "ans_test.json"
    write_ans = {}
    contexts = []
    questions = []
    ids = []
    m = mrc("config/id19.yaml")
    with open(rf, "r") as load_f:
        load_dict = json.load(load_f)
        for doc in load_dict["data"]:
            for paragraph in doc['paragraphs']:
                context = paragraph['context']
                for qa in paragraph['qas']:
                    contexts.append(context)
                    questions.append(qa['question'])
                    ids.append(qa['id'])
    ans = m.mrcqa_batch(contexts, questions)
    for i, id in enumerate(ids):
        write_ans[id] = ans[i]
    with open(wf, "w") as write_f:
        json.dump(write_ans, write_f)


if __name__ == '__main__':
    main()