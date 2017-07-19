#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-18 14:47:58
# @Author  : Li Hao (howardlee_h@outlook.com)
# @Link    : https://github.com/SAmmer0
# @Version : $Id$

from .. import database
from . import basicfactors
from . import derivativefactors
from ..const import FACTOR_FILE_PATH, SUFFIX

# --------------------------------------------------------------------------------------------------
# 常量
FACTOR_MODULES = [derivativefactors, basicfactors]


# --------------------------------------------------------------------------------------------------
# 函数


def get_factor_dict():
    '''
    获取模块内部的因子字典
    '''
    factors = dict()
    for mod in FACTOR_MODULES:
        factors.update(mod.get_factor_dict())
    return factors


def query(factor_name, time, codes=None):
    '''
    接受外部的请求，从数据库中获取对应因子的数据

    Parameter
    ---------
    factor_name: str
        需要查询的因子名称
    time: type that can be converted by pd.to_datetime or tuple of that
        单一的参数表示查询横截面的数据，元组（start_time, end_time）表示查询时间序列数据
    codes: list, default None
        需要查询数据的股票代码，默认为None，表示查询所有股票的数据

    Return
    ------
    out: pd.DataFrame
        查询结果数据，index为时间，columns为股票代码，如果未查询到符合要求的数据，则返回None
    '''
    all_factors = get_factor_dict()
    assert factor_name in all_factors, \
        'Error, factor name "{pname}" is'.format(pname=factor_name) +\
        ' not valid, valid names are {vnames}'.format(pname=list(all_factors.keys()))
    factor_msg = all_factors[factor_name]
    abs_path = FACTOR_FILE_PATH + '\\' + factor_msg['rel_path'] + SUFFIX
    db = database.DBConnector(abs_path)
    data = db.query(time, codes)
    return data
