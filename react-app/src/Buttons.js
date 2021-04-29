import Button from '@material-ui/core/Button';
import { useState } from 'react';
//var fetch = require('node-fetch');
import NodeFetch from 'node-fetch';


const Buttons = () => {

    const [running, setRunning] = useState(false);

    const sendStart = () => {
        NodeFetch('http://127.0.0.1:5000/start_optimizer', 
		{headers: {'Content-Type': 'application/json'},
		method: 'POST'
        }).then(function (response) {
            return response.text();
        })
    }

    const sendStop = () => {
        NodeFetch('http://127.0.0.1:5000/stop_optimizer', 
		{headers: {'Content-Type': 'application/json'},
		method: 'POST'
        }).then(function (response) {
            return response.text();
        })
    }

    const handleStart = () => {
        setRunning(true);
        sendStart();
    }

    const handleStop = () => {
        setRunning(false);
        sendStop();
    }

    return (
        <div className="startstopbuttons">
            <Button className='startbutton' variant="contained" color="primary" onClick={handleStart}>
                Optimize
            </Button>
            <Button className='stopbutton' variant="contained" disabled={!running} color="default" onClick={handleStop}>
                Stop
            </Button>
        </div>
    );
};

export default Buttons;