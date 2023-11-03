import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import config


def show_most_popular_groups():
    """Returns the value of the most_popular_groups config setting.
    
    To enable showing the most popular groups, add this line to the
    [app:main] section of your CKAN config file::
        ckan.lshtm_theme.show_most_popular_groups = True
        
    Returns ``False`` by default, if the setting is not in the config file.
    
    :rtype: bool
    """
    value = config.get('ckan.lshtm_theme.show_most_popular_groups', False)
    value = toolkit.asbool(value)
    return value


def most_popular_groups():
    """Returns a sorted list of the groups with the most datasets."""
    groups = toolkit.get_action('group_list')(data_dict={'sort': 'package_count desc', 'all_fields': True})

    groups = groups[:10]

    return groups


class LSHTMThemePlugin(plugins.SingletonPlugin):
    """An example theme plugin."""
    plugins.implements(plugins.IConfigurer)

    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'lshtm_theme')
        
    def get_helpers(self):
        """Register the most_popular_groups() 
        function above as a template helper function."""

        return {
            'lshtm_theme_most_popular_groups': most_popular_groups,
            'lshtm_theme_show_most_popular_groups': show_most_popular_groups
        }
