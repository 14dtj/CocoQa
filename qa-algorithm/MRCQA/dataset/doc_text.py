# -*- coding: utf-8 -*-

import re
import logging
import torch
import numpy as np
import time

logger = logging.getLogger(__name__)


class DocText:
    """
    define one sample text, like one context or one question
    """

    def __init__(self, nlp, text, config):
        doc = nlp(text)
        self.config = config
        self.token = []
        self.lemma = [] #basic form of words, no plural suffixes or verb derivation
        self.pos = []
        self.ent = []
        self.em = [] #exact match
        self.em_lemma = [] #exact match on lemma features

        self.right_space = []   # record whether the right side of every token is a white space

        for t in doc:
            if t.is_space:
                continue

            self.token.append(t.text)
            end_idx = t.idx + len(t.text)
            if end_idx < len(text) and text[end_idx] in Space.WHITE_SPACE:
                self.right_space.append(1)
            else:
                self.right_space.append(0)

            if config['use_em_lemma']:
                self.lemma.append(t.lemma_)
                self.em_lemma.append(0)

            if config['use_pos']:
                self.pos.append(t.tag_)  # also be t.pos_

            if config['use_ent']:
                self.ent.append(t.ent_type_)

            if config['use_em']:
                self.em.append(0)

    def __len__(self):
        return len(self.token)

#判断self的单词及其lemma是否在doc_text2中，提取exact match feature
    def update_em(self, doc_text2):
        """
        set the exact mach and exact match on lemma features
        :param doc_text2: the doc text to match
        :return:
        """
        for i in range(len(self.em)):
            if self.config['use_em'] and self.token[i] in doc_text2.token:
                self.em[i] = 1

            if self.config['use_em_lemma'] and self.lemma[i] in doc_text2.lemma:
                self.em_lemma[i] = 1

#Use this to translate doc to feature_dict(domain_tag)

    def to_id_dict(self, feature_dict):
        sentence = {'token': [], 'pos': [], 'ent': [], 'right_space': self.right_space}

        for i in range(len(self.token)):
            word = self.token[i]
            if word in feature_dict['id2word']:
                sentence['token'].append(feature_dict['id2word'].index(word))
            else:
                sentence['token'].append(0)
            pos = self.pos[i]
            if pos in feature_dict['id2pos']:
                sentence['pos'].append(feature_dict['id2pos'].index(pos))
            else:
                sentence['pos'].append(0)
            ent = self.ent[i]
            if ent in feature_dict['id2ent']:
                sentence['ent'].append(feature_dict['id2ent'].index(ent))
            else:
                sentence['ent'].append(0)

        sentence['em'] =self.em
        sentence['em_lemma'] = self.em_lemma
        sentence['right_space'] = self.right_space

        return sentence


    def to_id(self, feature_dict):
        """
        transform raw text to feature vector representation.
        it's slow, only used for interactive mode.
        :param feature_dict: ['id2word', 'id2char' 'id2pos', 'id2ent']
        :return:
        """
        #t1 = time.monotonic()
        sen_id = []
        add_features = {}
        #feature_dict = {k: v.tolist() for k, v in feature_dict.items()}
        seq_len = len(self.token)
        #t2 = time.monotonic()

        if self.config['use_pos']:
            add_features['pos'] = torch.zeros((seq_len, len(feature_dict['id2pos'])), dtype=torch.float)
        if self.config['use_ent']:
            add_features['ent'] = torch.zeros((seq_len, len(feature_dict['id2ent'])), dtype=torch.float)
        if self.config['use_em']:
            add_features['em'] = torch.tensor(self.em, dtype=torch.float).unsqueeze(-1)
        if self.config['use_em_lemma']:
            add_features['em_lemma'] = torch.tensor(self.em_lemma, dtype=torch.float).unsqueeze(-1)
        if self.config['use_domain_tag']:
            add_features['domain_tag'] = torch.tensor(self.domain_tag, dtype=torch.float).unsqueeze(-1)

        #t3 = time.monotonic()

        #intervals = [0,0,0]
        for i in range(seq_len):
            # word
            word = self.token[i]
            if word in feature_dict['id2word']:
                #t11 = time.monotonic()
                sen_id.append(feature_dict['id2word'].index(word))
                #t21 = time.monotonic()
                #intervals[0] += t21-t11
                #logger.info("index word time: "+str(t2-t1))
            else:
                sen_id.append(0)   # id=0 means padding value in preprocess
                logger.warning("word '%s' out of vocabulary" % word)

            # pos
            if self.config['use_pos']:
                pos = self.pos[i]
                if pos in feature_dict['id2pos']:
                    #t31 = time.monotonic()
                    add_features['pos'][i][feature_dict['id2pos'].index(pos)] = 1
                    #t41 = time.monotonic()
                    #intervals[1] += t41 - t31
                    #logger.info("index pos time: " + str(t2 - t1))
                else:
                    logging.warning("pos '%s' out of vocabulary" % pos)

            # ent
            if self.config['use_ent']:
                ent = self.ent[i]
                if ent in feature_dict['id2ent']:
                    #t51 = time.monotonic()
                    add_features['ent'][i][feature_dict['id2ent'].index(ent)] = 1
                    #t61 = time.monotonic()
                    #intervals[2] += t61 - t51
                    #logger.info("index ent time: " + str(t2 - t1))
                else:
                    logging.warning("ent '%s' out of vocabulary" % ent)
        #t4 = time.monotonic()
        rtn_features = None
        if len(add_features) > 0:
            rtn_features = torch.cat(list(add_features.values()), dim=-1)

        rtn_sen_id = torch.tensor(sen_id, dtype=torch.long)

        #t5 = time.monotonic()
        #logger.info("docid time: " + str(t2-t1)+" "+str(t3-t2)+" "+str(t4-t3)+" "+str(t5-t4)+" "+str(t5-t1))
        #logger.info("index time: " + str(intervals[0])+ " "+str(intervals[1])+" "+ str(intervals[2]))
        return rtn_sen_id, rtn_features


class Space:
    WHITE_SPACE = ' \t\n\r\u00A0\u1680​\u180e\u2000\u2001\u2002\u2003\u2004\u2005\u2006\u2007\u2008\u2009\u200a' \
                  '​​\u200b\u202f\u205f​\u3000\u2028\u2029'

    @staticmethod
    def is_white_space(c):
        return c in Space.WHITE_SPACE

    @staticmethod
    def remove_white_space(s):
        return re.sub('['+Space.WHITE_SPACE+']', '', s)
