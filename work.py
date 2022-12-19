# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import ModelView, ModelSQL, fields, Unique
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

    name = fields.Char('Name', required=True)


class Component(ModelSQL, ModelView):
    'Project Component'
    __name__ = 'project.work.component'

    name = fields.Char('Name', required=True)
    owner = fields.Char('Owner')
    url = fields.Char('Url')
    category = fields.Many2One('project.work.component_category', 'Category',
        required=False)
    comment = fields.Text('comment')

    @classmethod
    def __setup__(cls):
        super(Component, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints += [
            ('name_uniq', Unique(t, t.name), 'project_component.msg_name_unique')
        ]

    @classmethod
    def copy(cls, components, default=None):
        new_components = []
        for component in components:
            default['name'] = '%s-copy' % component.name
            new_component, = super(Component, cls).copy([component], default=default)
            new_components.append(new_component)
        return new_components


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
            ondelete='CASCADE', required=True)
    component_category = fields.Many2One('project.work.component_category',
            'Category Component', ondelete='RESTRICT', required=True)


class WorkComponent(ModelSQL):
    'Project Work - Component'
    __name__ = 'project.work-project.work_component'
    _table = 'project_work_component_rel'

    work = fields.Many2One('project.work', 'Work',
            ondelete='CASCADE', required=True)
    component = fields.Many2One('project.work.component',
            'Component', ondelete='RESTRICT', required=True)
