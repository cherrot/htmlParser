#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
from lxml import etree
import urllib

import csv

def parse1(i, e):
    print(
        '{}({}),'.format(
            pq(this).find('td#BuyerEmail>div>a').text(),
            pq(this).find('td#BuyerEmail>div>span:last').text()
            ),
        pq(this).children('#PurchasedQty').text()
        )

def parse2(i, e):
    print(
            pq(this).find('#BuyerEmail>div>a').attr('title'),
            pq(this).find('#BuyerEmail>div>div:first').text()
        )

doc = pq(filename='test/ebay.html')

#userName
print('User: ', doc('#AreaNavigation div.mbg>a>span.mbg-nw').text())

#content
records1 = doc('#tbl_mu_active_tbl_id').find('tbody.dt-rs>tr')
#records.each(lambda i, e: pq(this).find('td#BuyerEmail').text())
records1.each(parse1)

records2 = doc('#tbl_mu_active_tbl_id').find('tbody.dt-nsb>tr')
records2.each(parse2)

