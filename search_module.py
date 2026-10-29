import time


def get_id_lower(res):
    return res.resource_id.lower()


def linear_search_by_id(resources, target_id):
    target = str(target_id).strip().lower()
    start = time.time()
    found = None

    for r in resources:
        if r.resource_id.lower() == target:
            found = r
            break

    time_taken_ms = (time.time() - start) * 1000
    return found, time_taken_ms


def binary_search_by_id(resources, target_id):
    sorted_list = sorted(resources, key=get_id_lower)
    target = str(target_id).strip().lower()

    start = time.time()
    low = 0
    high = len(sorted_list) - 1
    found = None

    while low <= high:
        mid = (low + high) // 2
        mid_id = sorted_list[mid].resource_id.lower()

        if mid_id == target:
            found = sorted_list[mid]
            break
        elif mid_id < target:
            low = mid + 1
        else:
            high = mid - 1

    time_taken_ms = (time.time() - start) * 1000
    return found, time_taken_ms


def search_by_type(resources, res_type):
    target = str(res_type).strip().lower()
    results = []
    for r in resources:
        if target in r.resource_type.lower():
            results.append(r)
    return results


def search_by_min_capacity(resources, min_cap):
    results = []
    for r in resources:
        if r.capacity >= min_cap:
            results.append(r)
    return results
