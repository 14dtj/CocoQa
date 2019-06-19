import json
import math
import copy
import random
def getPreviewJson(rf, wf, preNum=3, tail = False):
    with open(rf, "r") as load_f:
        load_dict = json.load(load_f)
        print(type(load_dict))
        if tail:
            load_dict["data"] = load_dict["data"][-preNum:]
        else:
            load_dict["data"] = load_dict["data"][:preNum]
        with open(wf, "w") as write_f:
            json.dump(load_dict, write_f)

def addHead(rf, wf):
    with open(rf, "r") as load_f:
        load_list = json.load(load_f)
        save_dict = {}
        save_dict["data"] = load_list
        save_dict["version"] = "1.1"
        with open(wf, "w") as write_f:
            json.dump(save_dict, write_f)

def addDomainTag(rf, wf, tag):
    with open(rf, "r") as load_f1:
        load_dict = json.load(load_f1)
        for doc in load_dict["data"]:
            for paragraph in doc["paragraphs"]:
                paragraph["domain_tag"] = tag
    with open(wf, "w") as write_f1:
        json.dump(load_dict, write_f1)

def searchQuestionID(rf, wf, id):
    with open(rf, "r") as load_f:
        load_dict = json.load(load_f)
        for doc in load_dict["data"]:
            for paragraph in doc["paragraphs"]:
                for qa in paragraph["qas"]:
                    if qa["id"] == id:
                        with open(wf, "w") as write_f:
                            json.dump(paragraph, write_f)
                            return
def filterEmptyAnswer(rf, wf):
    with open(rf, "r") as load_f:
        load_dict = json.load(load_f)
        remove_doc = []
        for doc in load_dict["data"]:
            if doc["paragraphs"][0]["qas"][0]["answers"][0]["text"] == "":
               remove_doc.append(doc)
        print(remove_doc)
        for r_doc in remove_doc:
            #print("remove: " + str(i))
            if r_doc in load_dict["data"]:
                print("remove: "+str(r_doc))
                load_dict["data"].remove(r_doc)
    with open(wf, "w") as write_f:
        json.dump(load_dict, write_f)


def concatData(rf1, rf2, wf1, tag=False):
    with open(rf1, "r") as load_f1:
        load_dict = json.load(load_f1)
        if tag:
            for doc in load_dict["data"]:
                for paragraph in doc["paragraphs"]:
                    paragraph["domain_tag"] = 0
        with open(rf2, "r") as load_f2:
            load_dict2 = json.load(load_f2)
            if tag:
                for doc in load_dict2["data"]:
                    for paragraph in doc["paragraphs"]:
                        paragraph["domain_tag"] = 1

            write_dict = copy.deepcopy(load_dict2)
            write_dict["data"].extend(load_dict["data"])

    print(len((load_dict["data"])))
    print(len((load_dict2["data"])))
    print(len((write_dict["data"])))
    with open(wf1,"w") as write_f1:
        json.dump(write_dict, write_f1)

def concatData3(rf1, rf2, rf3, wf1, tag=False):
    with open(rf1, "r") as load_f1:
        load_dict = json.load(load_f1)
        if tag:
            for doc in load_dict["data"]:
                for paragraph in doc["paragraphs"]:
                    paragraph["domain_tag"] = 0
        with open(rf2, "r") as load_f2:
            load_dict2 = json.load(load_f2)
            if tag:
                for doc in load_dict2["data"]:
                    for paragraph in doc["paragraphs"]:
                        paragraph["domain_tag"] = 1
        with open(rf3, "r") as load_f3:
            load_dict3 = json.load(load_f3)
            if tag:
                for doc in load_dict3["data"]:
                    for paragraph in doc["paragraphs"]:
                        paragraph["domain_tag"] = 2

            write_dict = copy.deepcopy(load_dict2)
            write_dict["data"].extend(load_dict3["data"])
            write_dict["data"].extend(load_dict["data"])

    print(len((load_dict["data"])))
    print(len((load_dict2["data"])))
    print(len((load_dict3["data"])))
    print(len((write_dict["data"])))
    with open(wf1,"w") as write_f1:
        json.dump(write_dict, write_f1)

def randSplitData(rf, wf1, wf2, rate=0.7):
    with open(rf, "r") as load_f1:
        load_dict = json.load(load_f1)
        write_dict1 = copy.deepcopy(load_dict)
        write_dict2 = copy.deepcopy(load_dict)
        write_dict1["data"] = []
        write_dict2["data"] = []
        for i in range(len(load_dict["data"])):
            if random.random() < rate:
                write_dict1["data"].append(load_dict["data"][i])
            else:
                write_dict2["data"].append(load_dict["data"][i])
    print(len(write_dict1["data"]))
    print(len(write_dict2["data"]))
    with open(wf1, "w") as write_f1:
        json.dump(write_dict1, write_f1)
    with open(wf2, "w") as write_f2:
        json.dump(write_dict2, write_f2)

def resample(rf, wf, rate = 10):
    with open(rf, "r") as load_f1:
        load_dict = json.load(load_f1)
        write_dict = copy.deepcopy(load_dict)
        for i in range(rate-1):
            tmp_add = copy.deepcopy(load_dict["data"])
            write_dict["data"].extend(tmp_add)
        print(len(load_dict["data"]))
        print(len(write_dict["data"]))
        with open(wf, "w") as write_f1:
            json.dump(write_dict, write_f1)

if __name__ == '__main__':
    #getPreviewJson("../data/SQuAD/squad+1sample_tag.json","squad_preview_tag.json", tail = True)
    #getPreviewJson("../data/SQuAD/sentence_train.json","sentence_train_preview.json")
    #getPreviewJson("../MRC-data/marco/transfer-head.json", "../MRC-data/marco/transfer_preview.json")
     # concatData("../data/ccbase/100ccbase_train.json","../MRC-data/marco/transfer-filtered.json",
     #            "../MRC-data/marco/marco+100sample_tag.json", True)
     concatData("../data/ccbase/100ccbase_train.json", "../data/SQuAD/train-v1.1.json",
                "../data//SQuAD/squad+100sample.json",False)
    #addDomainTag("../data/ccbase/ccbase_dev.json","../data/ccbase/ccbase_dev_tag.json", 0)
    #addHead("../MRC-data/marco/transfer.json","../MRC-data/marco/transfer-head.json")
    #filterEmptyAnswer("../MRC-data/marco/transfer-head.json", "../MRC-data/marco/transfer-filtered.json")
    #randSplitData("../data/ccbase/ccbase_train.json","../data/ccbase/ccbase_train_v2.json","../data/ccbase/ccbase_dev.json",0.71)
    #resample("../data/ccbase/ccbase_train.json","../data/ccbase/100ccbase_train.json",50)