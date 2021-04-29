import PropTypes from 'prop-types';
import CircularProgress from '@material-ui/core/CircularProgress';
import Box from '@material-ui/core/Box';
import { useState } from 'react';
//var fetch = require('node-fetch');
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

const Output = () => {

    var running = true;
    var finished = true;
    const [progress, updateProgress] = useState(0);
    const [output, updateOutput] = useState({probeF: 'ATGC', probeQ: 'ATGC', sink: 'ATGC', sinkC: 'ATGC'});
    /*var probeF = 'ATGC'
    var probeQ = 'ATGC'
    var sink = 'ATGC'
    var sinkC = 'ATGC'*/
    console.log(progress);
    const getProgress = () => {
        NodeFetch('http://127.0.0.1:5000/get_progress', 
		{headers: {'Content-Type': 'application/json'},
		method: 'POST',
        body: ''
        }).then(function (response) {
            return response.json();
        }).then(function (json) {
            updateProgress(parseInt(json.progress));
        })
    }

    const getOutput = () => {
        NodeFetch('http://127.0.0.1:5000/get_output', 
		{headers: {'Content-Type': 'application/json'},
		method: 'POST',
        body: ''
        }).then(function (response) {
            return response.json();
        }).then(function (json) {
            updateOutput(json);
        })
    }

    if(running) {
        var progInterval = setInterval(function() {
            //updateProgress(parseInt('45'));
            getProgress();
            console.log(progress);
        }, 5000);
        
        if(progress >= 100) {
            finished = true;
        }
        return (
            <div className="progress">
                <h2>Optimization in Progress...</h2>
                <CircularProgressWithLabel variant="determinate" size='150px' value={progress} className="progressbar"/>
            </div>
        );
    }
    else if (finished) {
        //clearInterval(progInterval);
        getOutput();
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
        //clearInterval(progInterval);
        return (
            <div className="emptyoutput">
                <h2>Output</h2>
            </div>
        );
    }

};

export default Output;