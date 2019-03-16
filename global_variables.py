import os

proj_path = os.path.abspath(os.path.dirname(__file__))
api_collection_latency_csv = os.path.join(proj_path, "data/API_Collection_and_Latency.csv")
api_default_responses_dir = os.path.join(proj_path, "data/default_stub_api_responses")
api_updated_responses_dir = os.path.join(proj_path, "data/updated_stub_api_responses")
middleware_logs_loc = os.path.join(proj_path, "../logs/stub_middleware.log")
backup_folder = os.path.join(proj_path, "backups")
stub_config_path = os.path.join(proj_path, "hoverfly_stub/stub_final_config.json")
hoverfly_stub_folder = os.path.join(proj_path, "hoverfly_stub")

