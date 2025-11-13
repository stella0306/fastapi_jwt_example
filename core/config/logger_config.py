import logging

# 전역 로거 처리를 담당하는 클래스
class LoggerConfig:
    LOG_LEVEL: int = logging.INFO
    LOG_FORMAT: str = "[%(asctime)s] [PID:%(process)d] [%(levelname)s] [%(name)s] - %(message)s"
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def _create_formatter() -> logging.Formatter:
        # Formatter 인스턴스 생성
        return logging.Formatter(
            fmt=LoggerConfig.LOG_FORMAT,
            datefmt=LoggerConfig.DATE_FORMAT
        )

    @staticmethod
    def _create_console_handler() -> logging.StreamHandler:
        # 콘솔 출력용 Handler 생성
        handler = logging.StreamHandler()
        handler.setLevel(LoggerConfig.LOG_LEVEL)
        handler.setFormatter(LoggerConfig._create_formatter())
        return handler

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        # 전역 로거 반환
        logger = logging.getLogger(name)
        logger.setLevel(LoggerConfig.LOG_LEVEL)

        if not logger.hasHandlers():
            handler = LoggerConfig._create_console_handler()
            logger.addHandler(handler)

        return logger
