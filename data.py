import os
import SimpleITK
import numpy as np
import pypinyin
import pydicom
from shutil import copyfile, rmtree, copytree
from PIL import Image


def check_path(path):
    if not os.path.exists(path):
        os.mkdir(path)


def pinyin(name):
    """
    将病人姓名转换为拼音
    :param name: 病人姓名的字符串
    :return: 病人姓名拼音的字符串
    """
    chinese = name.split('_')[0]
    s = ""
    for i in pypinyin.pinyin(chinese, style=pypinyin.NORMAL):
        s += "".join(i)
    return s + '_' + name.split('_')[1]


def trans2png(source, target):
    """
    将数据处理为模型能够使用的数据
    :param source: 原始数据的路径
    :param target: 处理后数据的路径
    :return: None
    """

    for i in os.listdir(source):
        i_pinyin = pinyin(i)

        check_path(os.path.join(target, i_pinyin))
        check_path(os.path.join(target, i_pinyin, "PNG"))

        folder_list = os.listdir(os.path.join(source, i))
        copytree(os.path.join(source, i, "DICOM"),
                 os.path.join(target, i_pinyin, "DICOM"))
        copytree(os.path.join(source, i, "LABEL"),
                 os.path.join(target, i_pinyin, "LABEL"))
        if "PNG" in folder_list:
            for filename in os.listdir(os.path.join(source, i, "PNG")):
                if ".png" in filename:
                    copyfile(os.path.join(source, i, "PNG", filename),
                             os.path.join(target, i_pinyin, "PNG", filename))
        else:
            check_path(os.path.join(target, i_pinyin, "RAW"))
            for filename in os.listdir(os.path.join(target, i_pinyin, "DICOM")):
                refDs = pydicom.read_file(os.path.join(target, i_pinyin, "DICOM", filename))

                constPixelSpacing = (
                    float(refDs.PixelSpacing[0]), float(refDs.PixelSpacing[1]), float(refDs.SliceThickness)
                )

                origin = refDs.ImagePositionPatient
                arrDicom = refDs.pixel_array

                img = SimpleITK.GetImageFromArray(arrDicom, isVector=False)
                img.SetOrigin(origin)
                img.SetSpacing(constPixelSpacing)
                SimpleITK.WriteImage(img, os.path.join(target, i_pinyin, "RAW", filename[:-4] + ".mhd"))
                os.remove(os.path.join(target, i_pinyin, "RAW", filename[:-4] + ".mhd"))

            for filename in os.listdir(os.path.join(target, i_pinyin, "RAW")):
                rawData = open(os.path.join(target, i_pinyin, "RAW", filename), 'rb').read()
                imgSize = (512, 512)
                img = Image.frombuffer('L', imgSize, rawData, 'raw')
                img.save(os.path.join(target, i_pinyin, "PNG", filename[:-4] + ".png"))
            rmtree(os.path.join(target, i_pinyin, "RAW"))


if __name__ == '__main__':
    data_path = "data"
    target_path = "process"

    check_path(target_path)
    trans2png(data_path, target_path)

    folder_list = os.listdir("process")

    train = ['fanjunli_CT1201907100565', 'heguolan_CT1202004160116', 'tanglinju_CT1201811090450',
             'zhangshuxian_CT1201811090640', 'mulianfang_CT1201809060512', 'guowenfeng_CT220170920038',
             'zhangzhangping_CT1202011160625', 'cengchunhua_CT1201912300736', 'chenshaohua_CT1202104190471',
             'liyu_CT1201901150141', 'huxianhui_CT1202006300764', 'cengsuxiang_CT1201910080623',
             'zhangzhiying_CT1201808120137', 'yangxiaoping_CT1202003030011', 'wangxuehua_CT1202005170168',
             'zhouqingzhi_CT1202009270345', 'yangqiuhua_CT1202001090823', 'liguoxiu_CT1201911290588',
             'cengxiaoqin_CT1202003240138', 'dongyupei_CT1201810190192', 'bixiaolan_CT1202108020444',
             'luxiaoqin_CT1202004010608', 'xuquanzhen_CT1201909110253', 'wangyu_CT1202008060886',
             'liyalan_CT1201910090438', 'wangli_CT1202004110152', 'hexuemei_CT1201810270202',
             'luoguosu_CT1201908020665', 'guowenzhen_CT1202103230522', 'tiandan_CT1201908200089',
             'yangshunrong_CT1202104020360', 'hexia_CT1202105110781', 'hechunrong_CT1202001140622',
             'duqunfang_CT1201811090680', 'hexiaoying_CT1202005220701', 'hezhengbi_CT1202104190304',
             'liudao_CT1202104210256', 'leiqunhua_CT1202007170568', 'guoshilan_CT1202101170054',
             'zoudeping_CT1202008250768', 'jiangchenggui_CT1202011100951', 'shenjin_CT1201904190426']
    test = ['wangqinyu_CT1202005220507', 'liwenying_CT1202003160044', 'yangmei_CT1202006020667',
            'zhoudaoyu_CT1202010220433', 'chencuilan_CT1202102100223', 'xuchaorong_CT1201901190148',
            'lejunzhi_CT1202004090121', 'lizhenghui_CT1201907300574', 'tanyan_CT1201811180066',
            'zhoulihua_CT1202005210418', 'lishuwen_CT1201909140125']

    check_path("train")
    check_path("test")

    for train_patient in train:
        copytree(os.path.join("process", train_patient, "PNG"),
                 os.path.join("train", train_patient, "PNG"))

        copytree(os.path.join("process", train_patient, "LABEL"),
                 os.path.join("train", train_patient, "LABEL"))

    for test_patient in test:
        copytree(os.path.join("process", test_patient, "PNG"),
                 os.path.join("test", test_patient, "PNG"))

        copytree(os.path.join("process", test_patient, "LABEL"),
                 os.path.join("test", test_patient, "LABEL"))

    rmtree("process")

    check_path("train/LABEL")
    check_path("train/PNG")
    check_path("test/LABEL")
    check_path("test/PNG")

    for folder in os.listdir("train"):
        if folder not in ["LABEL", "PNG"]:
            for filename in os.listdir(os.path.join("train", folder, "LABEL")):
                check_path(os.path.join("train", "LABEL", folder))
                copyfile(os.path.join("train", folder, "LABEL", filename),
                         os.path.join("train", "LABEL", folder, filename))

            for filename in os.listdir(os.path.join("train", folder, "PNG")):
                check_path(os.path.join("train", "PNG", folder))
                copyfile(os.path.join("train", folder, "PNG", filename),
                         os.path.join("train", "PNG", folder, filename))
            rmtree(os.path.join("train", folder))

    for folder in os.listdir("test"):
        if folder not in ["LABEL", "PNG"]:
            for filename in os.listdir(os.path.join("test", folder, "LABEL")):
                check_path(os.path.join("test", "LABEL", folder))
                copyfile(os.path.join("test", folder, "LABEL", filename),
                         os.path.join("test", "LABEL", folder, filename))

            for filename in os.listdir(os.path.join("test", folder, "PNG")):
                check_path(os.path.join("test", "PNG", folder))
                copyfile(os.path.join("test", folder, "PNG", filename),
                         os.path.join("test", "PNG", folder, filename))
            rmtree(os.path.join("test", folder))
