#CHIPSEC: Platform Security Assessment Framework
#Copyright (c) 2018, Intel Corporation
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; Version 2.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#Contact information:
#chipsec@intel.com
#

import json
import time

import chipsec.file
from chipsec.logger import logger

def get_json_results(json_file):
    file_data = chipsec.file.read_file(json_file)
    if file_data == 0:
        return None
    try:
        json_data = json.loads(file_data)
    except:
        logger().error("Unable to load JSON file: {}".format(json_file))
        return None
    return json_data

def compute_result_deltas(previous, current):
    deltas = {}
    all_tests = set(current)
    all_tests.update(previous)
    for test in all_tests:
        new_res = prev_res = "-------"
        try:
            new_res = current[test]["result"]
        except:
            pass
        try:
            prev_res = previous[test]["result"]
        except:
            pass
        if new_res != prev_res:
            deltas[test] = {'previous': prev_res, 'current': new_res}
    return deltas

def display_deltas(deltas, hide_time, start_time):
    logger().log( "" )
    logger().log( "[CHIPSEC] **********************  TEST DELTA SUMMARY  *********************" )
    if not hide_time:
        logger().log( "[CHIPSEC] Time elapsed          %.3f" % (time.time()-start_time) )
    if deltas:
        logger().log( "[*] {:46}| {:10} | {:10}".format("Test", "Previous", "Current") )
        logger().log( "[*] {}".format('-' * 71) )
        for test in deltas:
            logger().log_bad("{:46}| {:10} | {:10}".format(test, deltas[test]['previous'], deltas[test]['current']))
    else:
        logger().log_good( "No changes detected." )
    logger().log( "[CHIPSEC] *****************************************************************" )


def log_deltas_json(deltas, outfile):
    deltas_json = json.dumps(deltas, sort_keys=True, indent=2, separators=(',', ': '))
    chipsec.file.write_file(outfile, deltas_json)

def log_deltas_xml(deltas, outfile):
    logger().error('XML delta log support not implemented.')
