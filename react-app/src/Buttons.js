import Button from '@material-ui/core/Button';
import { useState } from 'react';
import { useEffect } from 'react';
import NodeFetch from 'node-fetch';


const Buttons = () => {

    const [running, setRunning] = useState(false);

    const getProgress = () => {
        NodeFetch('http://127.0.0.1:5000/get_progress',
            {
                headers: { 'Content-Type': 'application/json' },
                method: 'POST',
                body: ''
            }).then(function (response) {
                return response.json();
            }).then(function (json) {
                setRunning(json.running);
            })
    }

    const getOutput = () => {
        NodeFetch('http://127.0.0.1:5000/get_output',
            {
                headers: { 'Content-Type': 'application/json' },
                method: 'POST',
                body: ''
            }).then(function (response) {
                return response.json();
            }).then(function (json) {
                if(running && json.finished) {
                    setRunning(false);
                }
            })
    }

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

    useEffect(() => {
        const interval = setInterval(() => {
            getProgress();
            getOutput();
        }, 1000);
        return () => {
          clearInterval(interval);
        };
    }, []);

    return (
        <div className="startstopbuttons">
            <Button className='startbutton' variant="contained" disabled={running} color="primary" onClick={handleStart}>
                Optimize
            </Button>
            <Button className='stopbutton' variant="contained" disabled={!running} color="default" onClick={handleStop}>
                Stop
            </Button>
        </div>
    );
};

export default Buttons;