# -*- coding: utf-8 -*-
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
"""	@version	19.0.1.0.2
	@owner  Hadron for Business
	@author Hadron for Business sp. z o.o.
	@date   2026.10.06

	Generate Missing Reordering Rules
	Wizard that creates a min/max reordering rule for every storable product
	without one, in a chosen warehouse location, optionally limited to a product
	category.
"""
from odoo import _, api, fields, models


class StockOrderpointGenerator(models.TransientModel):
    _name = 'stock.orderpoint.generator'
    _description = "Generate Missing Reordering Rules"

    company_id = fields.Many2one(
        'res.company', string="Company", required=True,
        default=lambda self: self.env.company,
    )
    warehouse_id = fields.Many2one(
        'stock.warehouse', string="Warehouse", required=True,
        domain="[('company_id', '=', company_id)]",
        default=lambda self: self._default_warehouse(),
    )
    location_id = fields.Many2one(
        'stock.location', string="Location", required=True,
        compute='_compute_location_id', store=True, readonly=False,
        default=lambda self: self._default_warehouse().lot_stock_id,
        domain="[('usage', '=', 'internal'), ('warehouse_id', '=', warehouse_id)]",
        help="The rules are created for this location.",
    )
    category_id = fields.Many2one(
        'product.category', string="Product Category",
        help="Only products of this category (and its subcategories). "
             "Leave empty for all storable products.",
    )
    product_min_qty = fields.Float(string="Minimum Quantity", default=0.0)
    product_max_qty = fields.Float(string="Maximum Quantity", default=0.0)
    skip_mode = fields.Selection(
        [
            ('any', "Has a rule in any location"),
            ('location', "Has a rule in the chosen location"),
        ],
        string="Skip Products That", required=True, default='any',
        help="Products matching this condition are not given a new rule.",
    )
    product_count = fields.Integer(
        string="Products to Receive a Rule", compute='_compute_product_count')

    @api.model
    def _default_warehouse(self):
        return self.env['stock.warehouse'].search(
            [('company_id', '=', self.env.company.id)], limit=1)

    @api.depends('warehouse_id')
    def _compute_location_id(self):
        for wizard in self:
            wizard.location_id = wizard.warehouse_id.lot_stock_id

    def _get_products_without_rule(self):
        self.ensure_one()
        domain = [
            ('is_storable', '=', True),
            ('company_id', 'in', [False, self.company_id.id]),
        ]
        if self.category_id:
            domain.append(('categ_id', 'child_of', self.category_id.id))
        products = self.env['product.product'].search(domain)

        rule_domain = [
            ('product_id', 'in', products.ids),
            ('company_id', '=', self.company_id.id),
        ]
        if self.skip_mode == 'location':
            rule_domain.append(('location_id', '=', self.location_id.id))
        with_rule = self.env['stock.warehouse.orderpoint'].with_context(
            active_test=False).search(rule_domain).product_id
        return products - with_rule

    @api.depends('company_id', 'location_id', 'category_id', 'skip_mode')
    def _compute_product_count(self):
        for wizard in self:
            wizard.product_count = len(
                wizard._get_products_without_rule()) if wizard.location_id else 0

    def action_generate(self):
        self.ensure_one()
        products = self._get_products_without_rule()
        if not products:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _("Nothing to do"),
                    'message': _("Every matching product already has a reordering rule."),
                    'type': 'warning',
                    'sticky': False,
                },
            }
        rules = self.env['stock.warehouse.orderpoint'].create([{
            'product_id': product.id,
            'location_id': self.location_id.id,
            'company_id': self.company_id.id,
            'product_min_qty': self.product_min_qty,
            'product_max_qty': self.product_max_qty,
        } for product in products])
        return {
            'type': 'ir.actions.act_window',
            'name': _("Created Reordering Rules"),
            'res_model': 'stock.warehouse.orderpoint',
            'view_mode': 'list,form',
            'domain': [('id', 'in', rules.ids)],
            'target': 'current',
        }

#EoF
