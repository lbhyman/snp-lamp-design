import Button from '@material-ui/core/Button';
import { useState } from 'react';

const Buttons = () => {

    const [running, setRunning] = useState(false);

    const handleStart = () => {
        setRunning(true);
    }

    const handleStop = () => {
        setRunning(false);
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