# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, And

__all__ = ['ProjectComponent', 'ProjectComponentCategory',
    'ProjectWorkComponentCategory', 'ProjectWorkComponent', 'Work']
__metaclass__ = PoolMeta


class ProjectComponentCategory(ModelSQL, ModelView):
    'Project Component Category'
    __name__ = 'project.work.component_category'

    name = fields.Char('Name', required=True, select=True)


class ProjectComponent(ModelSQL, ModelView):
    'Project Component'
    __name__ = 'project.work.component'

    name = fields.Char('Name', required=True, select=True)
    owner = fields.Char('Owner', select=True)
    url = fields.Char('Url')
    module = fields.Many2One('ir.module', 'Module')
    category = fields.Many2One('project.work.component_category', 'Category',
        required=False, select=True)
    comment = fields.Text('comment')
    active = fields.Boolean('Active')

    @staticmethod
    def default_active():
        return True


class Work:
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


class ProjectWorkComponentCategory(ModelSQL):
    'Project Work - Component Category'
    __name__ = 'project.work-project.work_component_category'
    _table = 'project_work_component_category_rel'

    work = fields.Many2One('project.work', 'Work',
            ondelete='CASCADE', select=True, required=True)
    component_category = fields.Many2One('project.work.component_category',
            'Category Component', ondelete='RESTRICT', required=True)


class ProjectWorkComponent(ModelSQL):
    'Project Work - Component'
    __name__ = 'project.work-project.work_component'
    _table = 'project_work_component_rel'

    work = fields.Many2One('project.work', 'Work',
            ondelete='CASCADE', select=True, required=True)
    component = fields.Many2One('project.work.component',
            'Component', ondelete='RESTRICT', required=True)
