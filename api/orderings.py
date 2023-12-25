from rest_framework.request import Request


class MovieOrdering:
    _ordering_param = 'ordering'
    _ordering_default = '-id'
    _ordering_valid_fields = ['id', '-id', 'name', '-name', 'year', '-year']

    @classmethod
    def get_ordering_fields(cls, request: Request) -> list[str]:
        ordering = request.query_params.get(cls._ordering_param, cls._ordering_default)
        ordering_fields = ordering.split(',')
        processed_ordering_fields = [field for field in ordering_fields if field in cls._ordering_valid_fields]

        if not processed_ordering_fields:
            return [cls._ordering_default]

        return processed_ordering_fields
