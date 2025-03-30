from pull import load_data, update_cell, add_hour

def lambda_handler(event, context):
    gym_data = load_data()
    update_cell(gym_data)
    add_hour(gym_data)
    return {
        "statusCode": 200,
        "body": "Gym data updated and logged successfully."
    }