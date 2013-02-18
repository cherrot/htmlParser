#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
from lxml import etree
import urllib

import csv

#class Parser:
#    def __init__(self):
#        self.

user = ''
records = []
head = ['record number', 'email', 'quantity', 'price', 'sale date', 'paid date',
        'email sent', 'title', 'detail']

def parse(i, e):
    global records
    content = parse1(pq(this).children('tr'))
    detail = parse2(pq(this).next('tbody.dt-nsb').children('tr'))

    records.append(content.update(detail))

def parse1(this):
    return ({'record number':int(this.children('#RecordNumber').text()),
             'email': '{}({}),'.format( #email
                this.find('td#BuyerEmail>div>a').text(),
                this.find('td#BuyerEmail>div>span:last').text()
                ),
             'quantity': int(this.children('#PurchasedQty').text()), # quantity
             'price': this.children('#SalePrice').text(), #price
             'sale date': this.children('#SaleDate').text(), #sale date
             'paid date': this.children('#PaidDate').text(), #paid date
             'email sent': this.children('#EmailSent').text(),#email sent num
             })

def parse2(this):
    return({'title': this.find('#BuyerEmail>div>a').attr('title'),
        'detail': this.find('#BuyerEmail>div>div:first').text()
        })


doc = pq(filename='test/ebay.html')

#userName
user = doc('#AreaNavigation div.mbg>a>span.mbg-nw').text()

#selector.each(lambda i, e: pq(this).find('td#BuyerEmail').text())
selector = doc('#tbl_mu_active_tbl_id').find('tbody.dt-rs')
selector.each(parse)

#records2 = doc('#tbl_mu_active_tbl_id').find('tbody.dt-nsb>tr')
#records2.each(parse2)


#export to csv file
dict_writer = csv.DictWriter(file('output.csv', 'wb'), fieldnames=head)
#dict_writer.writerow(head)
dict_writer.writeheader()
dict_writer.writerows(records)
