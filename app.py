from flask import Flask, render_template, jsonify, Response, request
import sys
import traceback
from database import get_data_from_table, get_csv_data

# Initialize Flask application
app = Flask(__name__)

# Define route for the root endpoint
@app.route('/')
def index():
    # Render the main page
    return render_template('index.html')

# Define route for fetching data from a database table
@app.route('/data/<path:table_name>')
def data(table_name):
    # Log the data fetch request
    print("fetch request here", file=sys.stderr)
    
    # Get the start and end times from the request arguments
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')
    print(start_time, end_time, file=sys.stderr)
    
    # Fetch the data from the table between the given time range
    df = get_data_from_table(table_name, start_time, end_time)
    
    # Return the data as JSON
    return jsonify(df.to_dict(orient='records'))

# Define route for downloading CSV data
@app.route('/download_csv/<string:table_url_name>', methods=['GET'])
def download_csv(table_url_name):
    # Replace spaces in the table URL name with slashes
    table_url_name = table_url_name.replace(" ", "/")
    
    try:
        # Get the start and end times from the request arguments, if any
        start_time = request.args.get('start_time', None)
        end_time = request.args.get('end_time', None)
        
        # Set the table name from the modified URL
        table_name = table_url_name
        
        # Check if the table name is valid
        if not table_name:
            return Response("Invalid table name", status=400)

        # Fetch the CSV data for the table and time range
        csv_data = get_csv_data(table_name, start_time, end_time)
        
        # Set the content disposition header for downloading the file
        content_disposition = f'attachment; filename={table_name}.csv'
        
        # Return the CSV data as a downloadable file
        return Response(
            csv_data,
            content_type='text/csv',
            headers={'Content-Disposition': content_disposition}
        )
    except Exception as e:
        # Log any exceptions that occur
        print(traceback.format_exc(), file=sys.stderr)
        
        # Return an internal server error response
        return Response("Internal server error", status=500)

# Main function to run the Flask app
def main():
    app.run(host='0.0.0.0', port=8888)

# Run the main function if the script is being run directly
if __name__ == '__main__':
    main()