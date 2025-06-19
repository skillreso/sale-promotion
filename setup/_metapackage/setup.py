import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-sale-promotion",
    description="Meta package for oca-sale-promotion Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-loyalty_criteria_multi_product>=17.0dev,<17.1dev',
        'odoo-addon-loyalty_incompatibility>=17.0dev,<17.1dev',
        'odoo-addon-loyalty_initial_date_validity>=17.0dev,<17.1dev',
        'odoo-addon-loyalty_limit>=17.0dev,<17.1dev',
        'odoo-addon-loyalty_multi_gift>=17.0dev,<17.1dev',
        'odoo-addon-loyalty_partner_applicability>=17.0dev,<17.1dev',
        'odoo-addon-sale_loyalty_criteria_multi_product>=17.0dev,<17.1dev',
        'odoo-addon-sale_loyalty_incompatibility>=17.0dev,<17.1dev',
        'odoo-addon-sale_loyalty_initial_date_validity>=17.0dev,<17.1dev',
        'odoo-addon-sale_loyalty_limit>=17.0dev,<17.1dev',
        'odoo-addon-sale_loyalty_multi_gift>=17.0dev,<17.1dev',
        'odoo-addon-sale_loyalty_order_line_link>=17.0dev,<17.1dev',
        'odoo-addon-sale_loyalty_order_suggestion>=17.0dev,<17.1dev',
        'odoo-addon-sale_loyalty_order_suggestion_multi_gift>=17.0dev,<17.1dev',
        'odoo-addon-sale_loyalty_order_suggestion_multi_product>=17.0dev,<17.1dev',
        'odoo-addon-sale_loyalty_partner_applicability>=17.0dev,<17.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 17.0',
    ]
)
