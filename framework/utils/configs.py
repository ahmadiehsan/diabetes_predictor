from framework.utils.config_tools import ConfigLoader, ConfigItemGetter

_config_loader = ConfigLoader()

c = ConfigItemGetter('base', _config_loader.base_configs)
c_custom = ConfigItemGetter('custom', _config_loader.custom_configs)
