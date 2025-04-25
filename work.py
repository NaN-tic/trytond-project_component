# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from collections import defaultdict
from trytond.model import ModelView, ModelSQL, fields, Unique, DeactivableMixin
from trytond.wizard import Button, StateAction, StateView, Wizard
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.modules.widgets import tools


class Version(ModelSQL, ModelView):
    'Project Component Version'
    __name__  = 'project.work.component.version'
    name = fields.Char('Name', required=True)
    release_date = fields.Date('Release Date')
    deprecation_date = fields.Date('Deprecation Date')

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls._order = [
            ('name', 'DESC'),
            ('id', 'DESC'),
            ]


class Feature(ModelSQL, ModelView):
    'Project Component Feature'
    __name__ = 'project.work.component.feature'
    component = fields.Many2One('project.work.component', 'Component',
        required=True)
    version = fields.Many2One('project.work.component.version', 'Version',
        required=True)
    date = fields.Date('Date')
    name = fields.Char('Name', required=True)
    description = fields.Text('Description')

    @classmethod
    def __register__(cls, module_name):
        sql_table = cls.__table__()
        super().__register__(module_name)

        # Migrate description to EditorJS
        tools.migrate_field(sql_table, sql_table.description, 'text')


class FeatureImportStart(ModelView):
    "Feature Import Start"
    __name__ = 'project.work.component.feature.import.start'
    file_ = fields.Binary("File", required=True)
    version = fields.Many2One('project.work.component.version', 'Version',
        required=True)
    component = fields.Many2One('project.work.component', 'Component',
        required=True, help='Default componet to assign all new features')


class FeatureImport(Wizard):
    "Feature Import"
    __name__ = 'project.work.component.feature.import'
    start = StateView('project.work.component.feature.import.start',
        'project_component.project_work_component_feature_import_start_view_form', [
            Button("Cancel", 'end', 'tryton-cancel'),
            Button("Import", 'import_', 'tryton-ok', default=True),
            ])
    import_ = StateAction('project_component.act_feature')

    def do_import_(self, action):
        pool = Pool()
        Feature = pool.get('project.work.component.feature')

        if not self.start.file_:
            return 'end'

        result = defaultdict(str)
        current_title = None
        version = self.start.version
        component = self.start.component
        content = self.start.file_.decode('utf-8')

        for line in content.splitlines():
            if line == '':
                continue
            elif line.startswith('###'):
                current_title = line.replace('### ', '').strip()
            elif current_title:
                result[current_title] += line.strip() + "\n"

        features = []
        for key, value in result.items():
            feature = Feature()
            feature.name = key
            feature.version = version
            feature.component = component
            feature.date = None
            feature.description = value
            features.append(feature)

        Feature.save(features)
        data = {'res_id': [c.id for c in features]}

        if len(features) == 1:
            action['views'].reverse()
        return action, data


class ComponentCategory(ModelSQL, ModelView):
    'Project Component Category'
    __name__ = 'project.work.component_category'

    name = fields.Char('Name', required=True)


class Component(DeactivableMixin, ModelSQL, ModelView):
    'Project Component'
    __name__ = 'project.work.component'

    name = fields.Char('Name', required=True)
    owner = fields.Char('Owner')
    url = fields.Char('URL')
    category = fields.Many2One('project.work.component_category', 'Category',
        required=False)
    comment = fields.Text('Comment')

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
