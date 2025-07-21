
def format_task(task):
    task_name = task['description']
    task_id = task['id']
    task_status = task['status']
    task_created = task['createdAt']
    task_updated = task['updatedAt']
    task_string = f"Task: {task_name} ID: {task_id} Status: {task_status} Created: {task_created} Updated: {task_updated}"
    task_string = f'''\
    Task:"{task_name}"
        ID: {task_id} Status: {task_status}
        Created: {task_created}
        Updated: {task_updated}'''
    return task_string

def filter_tasks(tasks, status):
    filtered_tasks = filter(lambda task: task['status'] == status, tasks )
    return list(filtered_tasks)

