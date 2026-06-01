

class Utils:
    
    @staticmethod
    def check_for_null_data(data: dict, *args) -> tuple[bool, str]:
        values = []
        has_null = False
        for arg in args:
            value = data.get(arg, None)
            if value is None:
                has_null = True
                values.append(arg)
        return has_null, ", ".join(values)
    
