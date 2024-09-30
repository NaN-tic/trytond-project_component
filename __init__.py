# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import work


def register():
    Pool.register(
        work.Version,
        work.Feature,
        work.FeatureImportStart,
        work.ComponentCategory,
        work.Component,
        work.WorkComponentCategory,
        work.WorkComponent,
        work.Work,
        module='project_component', type_='model')
    Pool.register(
        work.FeatureImport,
        module='project_component', type_='wizard')
