import { useState } from 'react';
import NodeFetch from 'node-fetch';

const ConditionEntry = () => {

    const [temperature, setTemperature] = useState('21');
    const [sodium, setSodium] = useState('65');
    const [magnesium, setMagnesium] = useState('8');

    const sendUpdate = () => {
        var data = {'temperature': parseFloat(temperature), 'sodium': parseFloat(sodium) / 1000.0, 
        'magnesium': parseFloat(magnesium) / 1000.0};

        NodeFetch('http://127.0.0.1:5000/send_input', 
		{headers: {'Content-Type': 'application/json'},
		method: 'POST',
		body: JSON.stringify(data)
        }).then(function (response) {
            return response.text();
        })
    }

    const handleTemperature = (event, newValue) => {
        setTemperature(newValue);
        sendUpdate();
    };
    const handleSodium = (event, newValue) => {
        setSodium(newValue);
        sendUpdate();
    };
    const handleMagnesium = (event, newValue) => {
        setMagnesium(newValue);
        sendUpdate();
    };

    return (
        <div className="conditionentry">
            <div class="condition-form" id="temperature-form">
                <label for="temperature">Temperature (C)</label>
                <input type="text" id="temperature" name="temperature" onChange={handleTemperature} />
            </div>
            <div class="condition-form" id="sodium-form">
                <label for="sodium">[Sodium] (mM)</label>
                <input type="text" id="sodium" name="sodium" onChange={handleSodium} />
            </div>
            <div class="condition-form" id="magnesium-form">
                <label for="magnesium">[Magnesium] (mM)</label>
                <input type="text" id="magnesium" name="magnesium" onChange={handleMagnesium} />
            </div>
        </div>
    );
};

export default ConditionEntry;