# noinspection PyInterpreter
import time
import stub_config_updation.helper_functions.stub_helpers as stub

if __name__ == '__main__':
    print("CUSTOM INFO: Script Started...")
    # Start Time of Code
    start_time = time.time()

    # NOTE: This is just for example purpose - to understand, how one can use helpers

    # Update PlanCode
    stub.make_plan_code_global()

    # Update MemberId/Transaction Ids
    stub.make_member_and_transaction_id_global()

    # Remove Request Body for all requests
    stub.remove_request_body_for_all_requests()

    # Remove Request Query for all requests
    stub.remove_request_query_for_all_requests()

    # Create APIs Collection
    stub.create_final_stub_api_collection()

    # Update Responses of required APIs
    stub.update_response_of_required_apis()

    # Print Time taken to execute script
    print("CUSTOM INFO: --- Script Execution Time: %s seconds ---" % (time.time() - start_time))
