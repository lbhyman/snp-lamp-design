import PropTypes from 'prop-types';
import CircularProgress from '@material-ui/core/CircularProgress';
import Box from '@material-ui/core/Box';
import { useState } from 'react';
import { useEffect } from 'react';
import NodeFetch from 'node-fetch';
function CircularProgressWithLabel(props) {
    return (
        <Box position="relative" display="inline-flex">
            <CircularProgress variant="determinate" {...props} />
            <Box
                top={0}
                left={130}
                bottom={0}
                right={0}
                position="absolute"
                display="flex"
                alignItems="center"
                justifyContent="center"
            >
                <label for='progress label' className='proglabel'>{props.value}%</label>
            </Box>
        </Box>
    );
}
CircularProgressWithLabel.propTypes = {
    value: PropTypes.number.isRequired,
};

// Kill all running intervals
var killId = setTimeout(function () {
    for (var i = killId; i > 0; i--) {
        clearInterval(i);
    }
}, 3000);

const Output = () => {
    const [running, setRunning] = useState(false);
    const [finished, setFinished] = useState(false);
    const [progress, updateProgress] = useState(0);
    const [output, updateOutput] = useState({ finished: false});

    const getProgress = () => {
        NodeFetch('http://127.0.0.1:5000/get_progress',
            {
                headers: { 'Content-Type': 'application/json' },
                method: 'POST',
                body: ''
            }).then(function (response) {
                return response.json();
            }).then(function (json) {
                updateProgress(parseInt(json.progress));
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
                updateOutput(json);
                if (output.hasOwnProperty('sinkC')) {
                    var output_copy = output;
                    if (output_copy['sinkC'].length < 7 || output_copy['sinkC'] === 'None Required') {
                        output_copy['sinkC'] = 'None Required';
                        updateOutput(output_copy);
                    }
                }
                setFinished(json.finished);
            })
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

    if (running) {
        return (
            <div className="progress">
                <h2>Optimization in Progress...</h2>
                <CircularProgressWithLabel variant="determinate" size='150px' value={progress} className="progressbar" />
            </div>
        );
    }
    else if (finished) {
        return (
            <div className="outputsequences">
                <h2>Output</h2>
                <div className="sequencelabels">
                    <p>ProbeF: </p>
                    <p>ProbeQ: </p>
                    <p>Sink: </p>
                    <p>Sink*: </p>
                </div>
                <div className="outsequences">
                    <p>{output['probeF']}</p>
                    <p>{output['probeQ']}</p>
                    <p>{output['sink']}</p>
                    <p>{output['sinkC']}</p>
                </div>
            </div>
        );
    }
    else {
        return (
            <div className="emptyoutput">
                <h2>Output</h2>
            </div>
        );
    }

};

export default Output;