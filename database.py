results_db = []

def save_result(result: dict):
    results_db.append(result)

def get_results(job_id: str):
    return [res for res in results_db if res["job_id"] == job_id]
