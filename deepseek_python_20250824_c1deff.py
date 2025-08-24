from flask import Flask, jsonify, request
from flask_cors import CORS
from samsung_mdc import SamsungMDCController
import config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize controller
controller = SamsungMDCController(config.TV_IPS)

@app.route('/api/status')
def get_status():
    """Get status of all displays"""
    try:
        status = controller.get_all_status()
        return jsonify(status)
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/power', methods=['POST'])
def control_power():
    """Control power of displays"""
    data = request.json
    display = data.get('display', 'all')
    power_on = data.get('power_on')
    
    try:
        if power_on:
            result = controller.power_on(display)
        else:
            result = controller.power_off(display)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error controlling power: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/volume', methods=['POST'])
def control_volume():
    """Control volume of displays"""
    data = request.json
    display = data.get('display', 'all')
    volume = data.get('volume')
    mute = data.get('mute')
    
    try:
        if volume is not None:
            result = controller.set_volume(display, volume)
        elif mute is not None:
            if mute:
                result = controller.mute(display)
            else:
                result = controller.unmute(display)
        else:
            return jsonify({"error": "No volume or mute parameter provided"}), 400
            
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error controlling volume: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/input', methods=['POST'])
def control_input():
    """Change input source of displays"""
    data = request.json
    display = data.get('display', 'all')
    input_source = data.get('input_source')
    
    if not input_source:
        return jsonify({"error": "No input_source provided"}), 400
    
    try:
        result = controller.set_input(display, input_source)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error changing input: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/layout', methods=['POST'])
def control_layout():
    """Change layout of video wall"""
    data = request.json
    layout = data.get('layout')
    
    if not layout:
        return jsonify({"error": "No layout provided"}), 400
    
    try:
        result = controller.set_layout(layout)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error changing layout: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)