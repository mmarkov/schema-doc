import os
from jinja2 import Environment, PackageLoader


class DocGenerator(object):
    def __init__(self, db, folder):
        self._db = db
        self._folder = folder
        self._tables_folder = os.path.join(self._folder, 'tables')
        self._env = Environment(loader=PackageLoader('schemadoc', 'static/templates'))
        object.__init__(self)

    def generate_documentation(self):
        table_pages = [];

        if not os.path.exists(self._tables_folder):
            os.makedirs(self._tables_folder)
        # generate pages for each table
        for table in self._db.tables:
            table_url = self._generate_table_page(table)
            table_pages.append({'table': table, 'url': table_url})
        # generate index page
        self._generate_home_page(table_pages)

    def _render_table_page(self, table_name):
        template = self._env.get_template('table_page.html')
        return template.render(table_name=table_name)

    def _generate_table_page(self, table_name):
        table_page = self._render_table_page(table_name)
        table_page_path = os.path.join(self._tables_folder, "%s.html"%table_name)
        with open(table_page_path, "wt") as fh:
            fh.write(table_page)
        url = os.path.relpath(table_page_path, self._folder)
        return url

    def _render_home_page(self, table_pages):
        template = self._env.get_template('home_page.html')
        return template.render(table_pages=table_pages)

    def _generate_home_page(self, table_pages):
        home_page = self._render_home_page(table_pages)
        home_page_path = os.path.join(self._folder, 'index.html')
        with open(home_page_path, "wt") as fh:
            fh.write(home_page)