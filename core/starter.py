
def start(once: bool):

    from tools.config import Config
    config = Config.read('config.json')

    from logging import basicConfig
    # noinspection PyArgumentList
    basicConfig(style=str().join(filter(
        lambda x: x in config.log_record_format, '%{$')),
        format=config.log_record_format,
        level=config.log_level.upper(),
        datefmt=config.log_date_format,
        filename=config.log_file_name)

    from .trader import Trader
    Trader(config).go(1 if once else None)
