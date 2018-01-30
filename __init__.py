# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import work


def register():
    Pool.register(
        work.ProjectComponentCategory,
        work.ProjectComponent,
        work.ProjectWorkComponentCategory,
        work.ProjectWorkComponent,
        work.Work,
        module='project_component', type_='model')
