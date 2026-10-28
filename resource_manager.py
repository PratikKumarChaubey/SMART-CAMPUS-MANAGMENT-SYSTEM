from validation_module import check_resource_data, InvalidInputError


class Resource:
    def __init__(self, resource_id, name, resource_type, capacity, location, availability="Available"):
        clean_status = check_resource_data(resource_id, name, resource_type, capacity, location, availability)
        self.resource_id = str(resource_id).strip()
        self.name = str(name).strip()
        self.resource_type = str(resource_type).strip()
        self.capacity = int(capacity)
        self.location = str(location).strip()
        self.availability = clean_status

    def to_dict(self):
        return {
            "resource_id": self.resource_id,
            "name": self.name,
            "resource_type": self.resource_type,
            "capacity": self.capacity,
            "location": self.location,
            "availability": self.availability
        }


class Classroom(Resource):
    def __init__(self, resource_id, name, capacity, location, availability="Available"):
        super().__init__(resource_id, name, "Classroom", capacity, location, availability)


class Laboratory(Resource):
    def __init__(self, resource_id, name, capacity, location, availability="Available"):
        super().__init__(resource_id, name, "Laboratory", capacity, location, availability)


class SeminarHall(Resource):
    def __init__(self, resource_id, name, capacity, location, availability="Available"):
        super().__init__(resource_id, name, "Seminar Hall", capacity, location, availability)


class Auditorium(Resource):
    def __init__(self, resource_id, name, capacity, location, availability="Available"):
        super().__init__(resource_id, name, "Auditorium", capacity, location, availability)


def make_resource_object(res_id, name, res_type, capacity, location, availability):
    t = res_type.strip().lower()
    if t == "classroom":
        return Classroom(res_id, name, capacity, location, availability)
    elif t == "laboratory":
        return Laboratory(res_id, name, capacity, location, availability)
    elif t == "seminar hall":
        return SeminarHall(res_id, name, capacity, location, availability)
    elif t == "auditorium":
        return Auditorium(res_id, name, capacity, location, availability)
    else:
        return Resource(res_id, name, res_type, capacity, location, availability)


class ResourceManager:
    def __init__(self, file_handler):
        self.file_handler = file_handler
        self.resources = []
        self.used_ids = set()
        self.res_dict = {}
        self.load_from_file()

    def load_from_file(self):
        self.resources = []
        self.used_ids = set()
        self.res_dict = {}

        rows = self.file_handler.load_resources()
        for r in rows:
            obj = make_resource_object(
                r["resource_id"],
                r["name"],
                r["resource_type"],
                r["capacity"],
                r["location"],
                r["availability"]
            )
            self.resources.append(obj)
            self.used_ids.add(obj.resource_id)
            self.res_dict[obj.resource_id] = obj

    def save_to_file(self):
        dict_list = []
        for r in self.resources:
            dict_list.append(r.to_dict())
        self.file_handler.save_resources(dict_list)

    def add_resource(self, res_id, name, res_type, capacity, location, availability="Available"):
        clean_id = str(res_id).strip()
        if clean_id in self.used_ids:
            raise InvalidInputError("Resource ID already exists. Duplicate IDs are not allowed.")

        new_res = make_resource_object(clean_id, name, res_type, capacity, location, availability)
        self.resources.append(new_res)
        self.used_ids.add(clean_id)
        self.res_dict[clean_id] = new_res
        self.save_to_file()
        return new_res

    def remove_resource(self, res_id):
        clean_id = str(res_id).strip()
        if clean_id not in self.used_ids:
            return False

        self.used_ids.remove(clean_id)
        del self.res_dict[clean_id]

        new_list = []
        for r in self.resources:
            if r.resource_id != clean_id:
                new_list.append(r)
        self.resources = new_list
        self.save_to_file()
        return True

    def update_status(self, res_id, new_status):
        clean_id = str(res_id).strip()
        if clean_id not in self.res_dict:
            raise InvalidInputError("Resource ID not found.")

        res = self.res_dict[clean_id]
        valid_status = check_resource_data(
            res.resource_id, res.name, res.resource_type, res.capacity, res.location, new_status
        )
        res.availability = valid_status
        self.save_to_file()
        return res

    def get_by_id(self, res_id):
        clean_id = str(res_id).strip()
        if clean_id in self.res_dict:
            return self.res_dict[clean_id]
        return None
