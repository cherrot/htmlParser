#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as pq
from lxml import etree
import urllib

import csv
import sys, getopt

records = []

def parse(doc):
    #userName
    user = doc('#AreaNavigation div.mbg>a>span.mbg-nw').text()
    
    #selector.each(lambda i, e: pq(this).find('td#BuyerEmail').text())
    selector = doc('#tbl_mu_active_tbl_id').find('tbody.dt-rs')
    selector.each(parseEach)

    for r in records:
        r.update({'user': user})

    return records

def parseEach(i, e):
    global records
    content = parseOdd(pq(this).children('tr'))
    detail = parseEven(pq(this).nextAll('tbody.dt-nsb').eq(0).children('tr'))
    content.update(detail)
    records.append(content)

def parseOdd(this):
    return {'record number':int(this.children('#RecordNumber').text()),
             'email': '{}({}),'.format( #email
                this.find('td#BuyerEmail>div>a').text(),
                this.find('td#BuyerEmail>div>span:last').text()
                ),
             'quantity': int(this.children('#PurchasedQty').text()), # quantity
             'price': this.children('#SalePrice').text(), #price
             'sale date': this.children('#SaleDate').text(), #sale date
             'paid date': this.children('#PaidDate').text(), #paid date
             'email sent': this.children('#EmailSent').text(),#email sent num
             }

def parseEven(this):
    return({'title': this.find('#BuyerEmail>div>a').attr('title'),
        'detail': this.find('#BuyerEmail>div>div:first').text()
        })

def write2csv(filename, fields, records):
    #export to csv file
    dict_writer = csv.DictWriter(file(filename, 'wb'), fieldnames=fields)
    #dict_writer.writerow(head)
    dict_writer.writeheader()
    #print records
    dict_writer.writerows(records)

def usage():
    print \
'''USAGE: 
{0} {-u|--url} url file.csv     :download url to an html document and parse it to file.csv
{0} file1.html file.csv         :parse file1.html to file.csv
{0} -h                          :print this
'''


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hu:', ['help','url='])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ('--help', '-h'):
            usage()
            sys.exit()
        elif opt in ('--url', '-u'):
            #TODO
            sys.exit()

    if not opts:
        fields = ['user', 'record number', 'email', 'quantity', 'price', 'sale date', 'paid date', 'email sent', 'title', 'detail']

        records = parse( pq(filename=args[0]) )
        write2csv(args[1], fields, records)
