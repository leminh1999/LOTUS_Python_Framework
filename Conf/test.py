import logging

# Định nghĩa một lớp filter tạm bỏ qua log
class IgnoreSpecificLogFilter(logging.Filter):
    def __init__(self, name_to_ignore):
        super().__init__()
        self.name_to_ignore = name_to_ignore

    def filter(self, record):
        # Kiểm tra tên của logger, nếu trùng với tên muốn bỏ qua thì trả về False
        return record.name != self.name_to_ignore

# Tạo một đối tượng logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# Tạo một đối tượng StreamHandler để in log ra màn hình console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Tạo định dạng cho log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Thêm StreamHandler vào logger
logger.addHandler(console_handler)

# Thêm filter vào logger để tạm bỏ qua log có tên là 'ignored_logger'
ignored_logger_filter = IgnoreSpecificLogFilter(name_to_ignore='ignored_logger')
logger.addFilter(ignored_logger_filter)

# Giả sử bạn có 3 dòng logger.debug như sau:
logger.debug('Dòng 1 - Sẽ được in')
logger.debug('Dòng 2 - Sẽ được in')
logger.debug('Dòng 3 - Sẽ được in')

# Bạn có thể tạo một logger khác có tên là 'ignored_logger' để bỏ qua log của logger này.
ignored_logger = logging.getLogger('ignored_logger')
ignored_logger.debug('Dòng 4 - Sẽ được bỏ qua')

# Để xóa filter và cho phép logger in bình thường:
logger.filters.remove(ignored_logger_filter)

# Dòng logger tiếp theo sẽ lại được in
logger.debug('Dòng 5 - Sẽ được in')
