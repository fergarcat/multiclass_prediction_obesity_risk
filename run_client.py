import os
import sys
import logging


from client.app import app

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - FrontendDash - %(message)s')
    print("Attempting to start Dash application via run_client.py using app.run()...")
    logging.info("Starting Dash application from run_client.py with host 0.0.0.0 and port 8050, debug=False.")
    
    try:
        app.run(debug=False, host='0.0.0.0', port=8050)
    except AttributeError as e:
        if "app.run_server has been replaced by app.run" in str(e):
            logging.error("Obsolete Dash method: app.run_server was called. Please use app.run.")
        raise e 
    except Exception as e:
        logging.error(f"An error occurred while starting the Dash server via run_client.py: {e}", exc_info=True)
        raise e