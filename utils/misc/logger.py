from loguru import logger

logger.add("utils/misc/logs.log", level='INFO', colorize=False)

logger.info(f'START LOGGER')
