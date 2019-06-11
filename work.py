# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Version', 'Component', 'ComponentCategory',
    'WorkComponentCategory', 'WorkComponent', 'Work']


class Version(ModelSQL, ModelView):
    'Project Component Version'
    __name__  = 'project.work.component.version'
    name = fields.Char('Name', required=True)
    release_date = fields.Date('Release Date')
    deprecation_date = fields.Date('Deprecation Date')


class Feature(ModelSQL, ModelView):
    'Project Component Feature'
    __name__ = 'project.work.component.feature'
    version = fields.Many2One('project.work.component.version', 'Version', required=True)
    component = fields.Many2One('project.work.component', 'Component', required=True)
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')


class ComponentCategory(ModelSQL, ModelView):
    'Project Component Category'
    __name__ = 'project.work.component_category'

    name = fields.Char('Name', required=True, select=True)


class Component(ModelSQL, ModelView):
    'Project Component'
    __name__ = 'project.work.component'

    name = fields.Char('Name', required=True, select=True)
    owner = fields.Char('Owner', select=True)
    url = fields.Char('Url')
    module = fields.Many2One('ir.module', 'Module')
    category = fields.Many2One('project.work.component_category', 'Category',
        required=False, select=True)
    comment = fields.Text('comment')


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'
    component_categories = fields.Many2Many(
        'project.work-project.work_component_category', 'work',
        'component_category', 'Component Category',
        states={
                 'invisible': Eval('type') != 'task',
                }, depends=['type'])

    components = fields.Many2Many(
        'project.work-project.work_component', 'work',
        'component', 'Components',
        states={
                 'invisible': Eval('type') != 'task',
                }, depends=['type'])


class WorkComponentCategory(ModelSQL):
    'Project Work - Component Category'
    __name__ = 'project.work-project.work_component_category'
    _table = 'project_work_component_category_rel'

    work = fields.Many2One('project.work', 'Work',
            ondelete='CASCADE', select=True, required=True)
    component_category = fields.Many2One('project.work.component_category',
            'Category Component', ondelete='RESTRICT', required=True)


class WorkComponent(ModelSQL):
    'Project Work - Component'
    __name__ = 'project.work-project.work_component'
    _table = 'project_work_component_rel'

    work = fields.Many2One('project.work', 'Work',
            ondelete='CASCADE', select=True, required=True)
    component = fields.Many2One('project.work.component',
            'Component', ondelete='RESTRICT', required=True)
