# -*- coding: utf-8 -*-
# vim: tabstop=4 softtabstop=0 shiftwidth=4 smarttab expandtab fileformat=unix
#################################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2017-2026 Hadron for Business sp. z o.o. (http://hadronforbusiness.com)
#
# This program is proprietary software, licensed under the Odoo Proprietary
# License v1.0 (OPL-1). Its use is governed by the Odoo Apps terms available
# at https://www.odoo.com/documentation/user/legal/licenses.html and the
# license agreement accepted at purchase / installation.
#
# It is forbidden to publish, distribute, sublicense, or sell copies of the
# Software or modified copies of the Software.
#
# The above copyright notice and this permission notice must be included in
# all copies or substantial portions of the Software.
#
#################################################################################
{
    'name': "Generate Missing Reordering Rules",
    'summary': "One click creates a min/max reordering rule for every stocked product that has none",
    'description': """
Generate Missing Reordering Rules
=================================

Products that have no reordering rule never appear in Odoo's replenishment
report, so nobody notices when they run low. Creating the rules one by one
for a catalogue of hundreds of products is tedious.

This app adds a small wizard (Inventory > Operations > Generate Missing
Reordering Rules). Pick a warehouse and a location, optionally a product
category and the minimum / maximum quantity, and it creates a rule for every
storable product that does not have one yet. Products that already have a
rule are left alone.
""",
    'version': "19.0.1.0.3",
    'author': "Hadron for Business sp. z o.o.",
    'website': "http://hadronforbusiness.com",
    'license': "OPL-1",
    'category': "Inventory/Inventory",
    'depends': [
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/orderpoint_generator_views.xml',
    ],
    'images': [
        'static/description/banner_screenshot.png',
    ],
    'installable': True,
    'application': False,
}
