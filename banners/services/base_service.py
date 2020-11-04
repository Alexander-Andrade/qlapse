class BaseService:
    def error(self, message):
        return {'error': message}

    def success(self, data=None):
        return {'success': data}

    def success_result(self, result):
        return True if 'success' in result else False

    def error_result(self, result):
        return True if 'error' in result else False
